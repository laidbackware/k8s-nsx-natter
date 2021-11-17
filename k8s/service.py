from kubernetes import config, client
from typing import Union
import sys, os
import ipaddress
# from kubernetes.client import api_client

def get_services_in_current_namespace(api_client) -> list:
  namespace = get_current_namespace()

  #TODO handle errors!
  namespaces = api_client.list_namespaced_service(namespace).items

  return namespaces

def get_current_namespace() -> str:
  # If running inside a cluster try to get the namespace form the SA directory
  # Otherwise extract it from the kube config context 
  namespace_name = ""
  try:
    with open('/var/run/secrets/kubernetes.io/serviceaccount/namespace') as f:
      namespace_name = f.read()
  except FileNotFoundError:
    current_context = config.list_kube_config_contexts()
    if len(current_context) > 1:
      namespace_name = "default"
      if current_context[1]['context'].__contains__("namespace"):
        return current_context[1]['context']['namespace']
  #TODO handle no current context etc
  return namespace_name

def get_service_by_label(api_client, k8s_service_key, k8s_service_prefix) -> Union[str, int]:
  services = get_services_in_current_namespace(api_client)

  found_services = []
  for service in services:
    labels = service.metadata.labels
    if labels and k8s_service_key in labels and labels[k8s_service_key].startswith(k8s_service_prefix):
      found_services.append(service)

  #TODO handle 2 or no services being found
  return found_services

def get_service_properties_by_label(api_client, k8s_service_key, k8s_service_prefix) -> list:
  found_services = get_service_by_label(api_client, k8s_service_key, k8s_service_prefix)
  #TODO handle services returning empty

  nat_rule_properties = []
  for service_details in found_services:
    for port in service_details.spec.ports:
      service_properties = {}
      #TODO handle annotations not being set!
      service_properties['nsx_nat_rule_name'] = f"{service_details.metadata.namespace}-{service_details.metadata.name}-{port.port}"
      service_properties['nsx_dnat_ip'] = service_details.metadata.annotations['nsx_nat_ip']
      service_properties['nsx_router_name'] = service_details.metadata.annotations['nsx_nat_router_name']
      service_properties['nsx_nat_priority'] = service_details.metadata.annotations['nsx_nat_priority']
      service_properties['nsx_nat_service_prefix'] = service_details.metadata.annotations['nsx_nat_service_prefix']
      service_properties['node_port'] = port.node_port
      service_properties['nsx_destination_port'] = port.port
      nat_rule_properties.append(service_properties.copy())
  return nat_rule_properties
