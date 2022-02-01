module branching_propagation(in1, in2, in3, out1, out2, keyIn0_0, keyIn0_1, keyIn0_2);

input in1, in2, in3, keyIn0_0, keyIn0_1, keyIn0_2;
output out1, out2;
wire w1, w2, w3, w4;

not NOT1 (w3, in2);
and AND1 (w1, in1, w2);
and AND2 (w4, w2, in3);

and KeyGate1 (out1, w1, keyIn0_0);
xor KeyGate2 (w2, w3, keyIn0_1);
and KeyGate3 (out2, w4, keyIn0_2);

endmodule
