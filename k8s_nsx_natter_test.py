import k8s_nsx_natter

def test_main():
  resp = k8s_nsx_natter.main()
  assert resp == True
 
  #TODO better tests!
