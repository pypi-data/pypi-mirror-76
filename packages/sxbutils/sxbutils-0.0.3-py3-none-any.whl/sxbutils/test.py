#from sxbutils import sxbutils
import sxbutils
from envvar import envvar 

def test_stub():
  m="test_stub"
  sxbutils.do_stuff()
  report=envvar("REPORT", True, "sxb.txt")
  diddle=envvar("DIDDLE", False, "did")
  print(m+" report.tostr()="+report.tostr())



test_stub()
