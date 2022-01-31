module single_branch_propagation(in1, in2, out1, out2, keyIn0_0, keyIn0_1, keyIn0_2);

input in1, in2, keyIn0_0, keyIn0_1, keyIn0_2;
output out1, out2;
wire w1, w2;

and AND1 (w1, in1, in2);

and KeyGate1 (out1, w1, keyIn0_0);
xor KeyGate2 (w2, in2, keyIn0_1);
and KeyGate3 (out2, w2, keyIn0_2);

endmodule
