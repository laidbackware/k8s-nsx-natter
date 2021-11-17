import requests, urllib3
from urllib.error import HTTPError
import sys, os,json
import utils.utils as utils

urllib3.disable_warnings()

def generate_client() -> dict:
  # Collect environment variables
  manager_fqdn = utils.get_env_var("NSX_MANAGER_FQDN")
  username = utils.get_env_var("NSX_USERNAME")
  password = utils.get_env_var("NSX_PASSWORD").strip()

  # Setup session object and test the connection
  s = requests.Session()
  s.auth = (username, password)
  s.verify = False

  try:
    r = s.get(f"https://{manager_fqdn}/api/v1/node/services/http")
  except HTTPError as e:
    sys.stderr.write(f"Connection to NSX Manager failed with error {str(e)}\nExiting!")
    sys.exit(1)
  
  if r.status_code == 403:
    sys.stderr.write(f"Failed to authenticate with NSX Manager with error: {r.content}\nExiting!")
    sys.exit(1)
  if r.status_code >= 400:
    sys.stderr.write(f"Manager responded with error code {r.status_code}\nExiting!")
    sys.exit(1)

  nsx_client = {'session': s, 'manager_fqdn': manager_fqdn}

  return nsx_client

def json_decode(data):
  try:
    json_object = json.loads(data)
  except ValueError as e:
      return None
  return json_object

def find_object_by_name(nsx_client, object_name, object_type, allow_empty=False):
  # Use the NSX search API to search for single objects
  found_object = nsx_client['session'].get(f"https://{nsx_client['manager_fqdn']}/policy/api/v1/search/query?query=resource_type:{object_type} AND display_name:{object_name}").json()

  if len(found_object['results']) == 0:
    if not allow_empty:
      sys.stderr.write(f"No {object_type}s found with name {object_name}\nExiting!")
      sys.exit(1)
    else:
      found_object['results'].append(None)
  if len(found_object['results']) > 1:
    sys.stderr.write(f"Multiple {object_type}s found with name {object_name}\nExiting!")
    sys.exit(1)

  return found_object['results'][0]
