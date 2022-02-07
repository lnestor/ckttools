import pytest
from vast.graph_search import get_key_inputs_from_subcircuit
from vast.search import get_moddef_from_verilog

VERILOG = """
module example(in1, in2, in3, out1, keyIn0_0);

input in1, in2, keyIn0_0, keyIn0_1;
output out1;
wire w1, w2, w3, keyWire0;

and AND0 (w1, in1, in2);
and AND2 (w4, 0, keyIn0_0);
and AND1 (w3, in3, w4);
or OR0 (w2, keyIn0_0, w3);
xor XOR0 (keyWire0, w2, keyIn0_1);
xor XOR1 (out1, w1, keyWire0);

endmodule
"""

@pytest.fixture(scope="module")
def moddef():
    return get_moddef_from_verilog(VERILOG)

def test_get_key_inputs_from_subcircuit(moddef):
    key_inputs = get_key_inputs_from_subcircuit(moddef, "keyWire0")

    assert len(key_inputs) == 2
    assert set(key_inputs) == set(["keyIn0_0", "keyIn0_1"])
