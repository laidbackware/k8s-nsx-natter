import nsx.client



def test_generate_client():
  nsx_client = nsx.client.generate_client()
  assert len(nsx_client) > 0
 
  #TODO better tests!

def test_find_router():
  nsx_client = nsx.client.generate_client()
  router = nsx.client.find_object_by_name(nsx_client, "nat-test", "Tier1")
  assert type(router) == dict
  assert "display_name" in router
  assert router["display_name"] == "nat-test"

def test_find_service():
  nsx_client = nsx.client.generate_client()
  service = nsx.client.find_object_by_name(nsx_client, "sctp-4000", "Service")
  assert type(service) == dict
  assert "display_name" in service
  assert service["display_name"] == "sctp-4000"

def test_find_service_empty():
  nsx_client = nsx.client.generate_client()
  service = nsx.client.find_object_by_name(nsx_client, "DUMMY", "Service", True)
  assert service == None

def test_find_nat_rule():
  nsx_client = nsx.client.generate_client()
  policy_nat = nsx.client.find_object_by_name(nsx_client, "PolicyNat", "Service", True)
  policy_nat_rule = nsx.client.find_object_by_name(nsx_client, "PolicyNatRule", "Service", True)
  assert policy_nat == None