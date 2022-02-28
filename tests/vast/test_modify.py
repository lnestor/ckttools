from ckttools.vast.modify import *
import pytest

@pytest.fixture
def ilist():
    out_port = vast.PortArg(None, vast.Identifier("output"))
    in_ports = [vast.PortArg(None, vast.Identifier("input%i" % i)) for i in range(2)]
    instance = vast.Instance("and", "TEST_AND", (out_port, *in_ports), ())
    return vast.InstanceList("and", (), (instance,))

@pytest.fixture
def ilist_with_const():
    out_port = vast.PortArg(None, vast.Identifier("output"))
    in_ports = [vast.PortArg(None, vast.IntConst(1)), vast.PortArg(None, vast.Identifier("input0"))]
    instance = vast.Instance("and", "TEST_AND", (out_port, *in_ports), ())
    return vast.InstanceList("and", (), (instance,))

def test_change_ilist_input_name(ilist):
    change_ilist_input_name(ilist, "input0", "newinput")
    assert ilist.children()[0].children()[1].children()[0].name == "newinput"

def test_change_ilist_input_name_with_constant(ilist_with_const):
    change_ilist_input_name(ilist_with_const, "input0", "newinput")
    assert ilist_with_const.children()[0].children()[2].children()[0].name == "newinput"
