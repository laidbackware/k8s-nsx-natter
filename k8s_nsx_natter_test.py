import k8s_nsx_natter

def test_e2e():
  resp = k8s_nsx_natter.main()
  assert resp == True
 
  #TODO better tests!
