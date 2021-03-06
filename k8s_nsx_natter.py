import k8s.host_ip_address
import k8s.service
import nsx.client
import utils.utils as utils
from kubernetes import config, client
import os, sys


def main():
  print("nsx-natter starting")

  k8s_selector_key = utils.get_env_var('SELECTOR_KEY')
  
  # If KUBERNETES_PORT is set, assume to be inside a cluster and login with in cluster config
  try:
    os.environ['KUBERNETES_PORT']
    print('attempting to load in cluster config')
    config.load_incluster_config()
    print('loaded in cluster config')
  except:
    config.load_kube_config()
    print('loaded in local config')

  api_client = client.CoreV1Api()
  host_ip = k8s.host_ip_address.get_hosting_ip(api_client)

  nat_rule_properties = k8s.service.get_service_properties_by_selector(api_client, k8s_selector_key)

  nsx_client = nsx.client.generate_client()

  for nat_rule in nat_rule_properties:
    nsx_router_path = nsx.client.find_object_by_name(nsx_client, nat_rule['nsx_router_name'], "Tier1")['path']
    #TODO handle router not found
    nsx_service_name = f"{nat_rule['nsx_nat_service_prefix']}-{nat_rule['nsx_destination_port']}"
    nsx_service = nsx.client.find_object_by_name(nsx_client, nsx_service_name, "Service", True)
    if nsx_service:
      service_path = nsx.client.find_object_by_name(nsx_client, nsx_service_name, "Service", True)['path']
    else:
      #TODO Create Service if it doesn't exist
      sys.stderr.write(f"Service {nsx_service_name} does not exist in NSX-T\nExiting!")
      sys.exit(1)

    payload = {
      "display_name": nat_rule['nsx_nat_rule_name'], 
      "description": f"Rule generated by nsx-natter for {nat_rule['nsx_nat_rule_name']}",
      "action": "DNAT",
      "destination_network": nat_rule['nsx_dnat_ip'],
      "service": service_path,
      "translated_network": host_ip,
      "translated_ports": nat_rule['node_port'],
      "sequence_number": int(nat_rule['nsx_nat_priority']),
      "enabled": True,
      "logging": False,
      "firewall_match": "BYPASS",
    }

    url = f"https://{nsx_client['manager_fqdn']}/policy/api/v1{nsx_router_path}/nat/USER/nat-rules/{nat_rule['nsx_nat_rule_name']}"

    resp = nsx_client['session'].patch(url, json=payload)

    if resp.status_code != 200:
      sys.stderr.write(f"NSX returned error when trying to create {nat_rule['nsx_nat_rule_name']}")
      sys.stderr.write(f"Error {resp.content}\nExiting!")
      sys.exit(1)
  
  print("nsx-natter complete")
  return True

if __name__ == "__main__":
  main()

