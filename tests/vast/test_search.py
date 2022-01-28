import pytest
from pyverilog.vparser.parser import parse
from ckttools.vast.search import *

VERILOG = """
module test_module(in1, in2, in3, in4, out1, out2, keyIn0_0);

input in1, in2, in3, in4;
input keyIn0_0;
output out1, out2;
wire w1, w2;
wire w3;

and AND1 (out1, in1, in2);
buf BUF1 (w2, in2);
xor XOR1 (w3, w2, keyIn0_0);
or OR1 (w1, w3, in3);
and AND2 (out2, w1, in4);

endmodule
"""

@pytest.fixture(scope="module")
def moddef():
    ast, _ = parse([VERILOG], debug=False)
    return get_moddef(ast)

@pytest.fixture(scope="module")
def ilist():
    out_port = vast.PortArg(None, vast.Identifier("output"))
    in_ports = [vast.PortArg(None, vast.Identifier("input%i" % i)) for i in range(2)]
    instance = vast.Instance("and", "TEST_AND", (out_port, *in_ports), ())
    return vast.InstanceList("and", (), (instance,))

def test_get_wire_names(moddef):
    assert get_wire_names(moddef) == ["w1", "w2", "w3"]

def test_get_primary_input_names(moddef):
    assert get_primary_input_names(moddef) == ["in1", "in2", "in3", "in4"]

def test_get_key_input_names(moddef):
    assert get_key_input_names(moddef) == ["keyIn0_0"]

def test_get_input_names(moddef):
    assert get_input_names(moddef) == ["in1", "in2", "in3", "in4", "keyIn0_0"]

def test_get_output_names(moddef):
    assert get_output_names(moddef) == ["out1", "out2"]

def test_find_last_input(moddef):
    # Index 0: paramlist, index 1: port list, index 2: first inputs
    assert find_last_input(moddef) == 3

def test_find_last_wire(moddef):
    assert find_last_wire(moddef) == 6

def test_try_get_ilist_from_output_with_no_ilists(moddef):
    assert try_get_ilist_from_output(moddef, "random") is None

def test_try_get_ilist_from_output_with_ilists(moddef):
    assert try_get_ilist_from_output(moddef, "w3").children()[0].name == "XOR1"

def test_get_ilist_from_output(moddef):
    assert get_ilist_from_output(moddef, "w3").children()[0].name == "XOR1"

def test_get_ilists_from_input(moddef):
    ilists = get_ilists_from_input(moddef, "in2")
    assert len(ilists) == 2
    assert ilists[0].children()[0].name == "AND1"
    assert ilists[1].children()[0].name == "BUF1"

def test_get_ilists(moddef):
    ilists = get_ilists(moddef)
    assert len(ilists) == 5

def test_get_ilist_output(ilist):
    assert get_ilist_output(ilist) == "output"

def test_get_ilist_inputs(ilist):
    assert get_ilist_inputs(ilist) == ["input0", "input1"]

def test_get_ilist_input(ilist):
    assert get_ilist_input(ilist, 0) == "input0"

def test_get_ilist_type(ilist):
    assert get_ilist_type(ilist) == "and"
