from ckttools.bench.parse import parse_from_moddef, parse_from_verilog
from ckttools.vast.search import get_moddef_from_verilog

VERILOG = """
module sample(in1, in2, out1);
input in1, in2;
output out1;
wire w1;
and AND1 (w1, in1, in2);
buf BUF1 (out1, w1);
endmodule
"""

BENCH = """# sample
#

INPUT(in1)
INPUT(in2)

OUTPUT(out1)

w1 = and(in1, in2)
out1 = buf(w1)
"""

def test_parse_from_verilog():
    bench = parse_from_verilog(VERILOG)
    assert str(bench) == BENCH

def test_parse_from_moddef():
    moddef = get_moddef_from_verilog(VERILOG)
    bench = parse_from_moddef(moddef)
    assert str(bench) == BENCH

