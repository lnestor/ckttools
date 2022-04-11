from ckttools.logic.circuit_solver import *

VERILOG = """
module test_module(in1, in2, in3, in4, out1, out2);

input in1, in2, in3, in4;
output out1, out2;
wire w1, w2;

and AND1 (w1, in1, in2);
or OR1 (out1, w1, in3);
xor XOR1 (w2, in2, in4);
and AND2 (out2, in3, w2);

endmodule
"""

def test_solve():
    solver = CircuitSolver(VERILOG)
    inputs = {"in1": True, "in2": True, "in3": True, "in4": True}
    solution = solver.solve(inputs)

    assert solution["out1"] == True
    assert solution["out2"] == False
