module simple_propagation(in1, in2, out1, keyIn0_0, keyIn0_1);

input in1, in2, keyIn0_0, keyIn0_1;
output out1;
wire w1, w2;

xor XOR1 (w1, in1, keyIn0_0);
and AND1 (w2, w1, in2);
and AND2 (out1, w2, keyIn0_1);

endmodule
