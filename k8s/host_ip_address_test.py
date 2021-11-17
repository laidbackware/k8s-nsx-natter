import k8s.host_ip_address as svc
from kubernetes import config, client
import ipaddress, os, sys

try:
  pod_name = os.environ['HOSTNAME']
except KeyError:
  sys.stderr.write("You must export HOSTNAME as the name of a pod running in the current namespace")
  sys.exit(1)

config.load_kube_config()
api_client = client.CoreV1Api()

def test_get_hosting_ip():
  ip = svc.get_hosting_ip(api_client)
  assert validate_ip_address(ip)
    
def validate_ip_address(address):
  try:
    ip = ipaddress.ip_address(address)
    return True
  except ValueError:
    return False