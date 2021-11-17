from kubernetes import config, client
import sys, os
import k8s.service as svc
import utils.utils as utils


def get_hosting_ip(api_client) -> str:
  pod_name = utils.get_env_var('HOSTNAME')

  namespace = svc.get_current_namespace()
  pod = api_client.read_namespaced_pod(pod_name, namespace)
  return pod.status.host_ip

