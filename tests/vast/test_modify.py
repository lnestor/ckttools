import pytest
import pyverilog.vparser.ast as vast
from vast.modify import *
from vast.search import get_ilist_output

@pytest.fixture(scope="module")
def ilist():
    out_port = vast.PortArg(None, vast.Identifier("output"))
    in_ports = [vast.PortArg(None, vast.Identifier("input%i" % i)) for i in range(2)]
    instance = vast.Instance("and", "TEST_AND", (out_port, *in_ports), ())
    return vast.InstanceList("and", (), (instance,))

def test_rename_ilist_output(ilist):
    rename_ilist_output(ilist, "new_name")
    assert get_ilist_output(ilist) == "new_name"
