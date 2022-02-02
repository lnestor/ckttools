// [LN]: KeyGate1, w3, w1, keyIn0_0, w3
// [LN]: KeyGate2, w2, out1, keyIn0_1, out1
module simple_propagation(in1, in2, out1, keyIn0_0, keyIn0_1);

input in1, in2, keyIn0_0, keyIn0_1;
output out1;
wire w1, w2, w3;

not NOT1 (w3, in1);
and AND1 (w2, w1, in2);

xor KeyGate1 (w1, w3, keyIn0_0);
and KeyGate2 (out1, w2, keyIn0_1);

endmodule
