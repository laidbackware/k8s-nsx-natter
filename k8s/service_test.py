import k8s.service
from k8s.host_ip_address_test import validate_ip_address
from kubernetes import config, client
import ipaddress 
from kubernetes.client.models.v1_service import V1Service

config.load_kube_config()
api_client = client.CoreV1Api()

svc_label = {"key": "app", "prefix": "natter-example-pod"}

def test_get_all_services():
  services = k8s.service.get_services_in_current_namespace(api_client)
  assert len(services) > 0
  
  #TODO better tests!

def test_get_current_namespace():
  namespace = k8s.service.get_current_namespace()
  assert type(namespace) == str
  assert namespace != ""

def test_get_service_by_label():
  found_services = k8s.service.get_service_by_selector(api_client, "app")
  assert type(found_services) == list
  assert type(found_services[0]) == V1Service
  assert len(found_services) == 2
  assert svc_label['key'] in found_services[0].metadata.labels
  assert found_services[0].metadata.labels["app"].startswith("natter-example-pod")


def test_get_service_properties_by_label():
  nat_rule_properties = k8s.service.get_service_properties_by_selector(api_client, "app")
  assert type(nat_rule_properties) == list
  assert len(nat_rule_properties) == 3
  for key in ['nsx_nat_rule_name', 'nsx_dnat_ip', 'nsx_router_name', 'nsx_nat_priority', 'nsx_nat_service_prefix', 'node_port', 'nsx_destination_port']:
    assert key in nat_rule_properties[0]
  for rule in nat_rule_properties:
    assert validate_ip_address(rule['nsx_dnat_ip'])
