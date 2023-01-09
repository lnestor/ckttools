from ckttools.vast.group import find_interference_groups
from ckttools.vast.moddef import get_moddef_from_verilog
import pytest

BASE_VERILOG = """
module test_module(in1, in2, out1, out2, out3, out4, keyIn1, keyIn2, keyIn3, keyIn4, keyIn5, keyIn6, keyIn7, keyIn8);

input in1, in2;
output out1, out2, out3, out4;
input keyIn1, keyIn2, keyIn3, keyIn4, keyIn5, keyIn6, keyIn7, keyIn8;

wire keyWire1, keyWire2, keyWire3, keyWire4, keyWire5, keyWire7, keyWire8;
wire w1, w2, w3;

not NOT1(out1, keyWire1);
xor KeyGate1(keyWire1, keyIn1, in1);

and AND2(out2, keyWire2, keyWire3);
xor KeyGate2(keyWire2, keyIn2, w1);
xor KeyGate3(keyWire3, keyIn3, w2);
and AND3(w1, in1, in2);
and AND4(w2, in1, in2);

not NOT2(out3, keyWire4);
xor KeyGate4(keyWire4, keyIn4, keyWire5);
xor KeyGate5(keyWire5, keyIn5, in1);

xor KeyGate6(out4, keyIn6, w3);
and AND5(w3, keyWire7, keyWire8);
xor KeyGate7(keyWire7, keyIn7, in1);
xor KeyGate8(keyWire8, keyIn8, in2);

endmodule
"""

@pytest.fixture()
def moddef():
    return get_moddef_from_verilog(BASE_VERILOG)

def test_find_interference_groups_returns_correct_groups(moddef):
    groups = find_interference_groups(moddef)

    assert set(groups[0]) == set(["KeyGate1"])
    assert set(groups[1]) == set(["KeyGate2"])
    assert set(groups[2]) == set(["KeyGate3"])
    assert set(groups[3]) == set(["KeyGate4", "KeyGate5"])
    assert set(groups[4]) == set(["KeyGate6", "KeyGate7", "KeyGate8"])

