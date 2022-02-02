// [LN]: KeyGate1, in2, keyWire0, keyIn0_0, in2
module input_propagation(in1, in2, in3, in4, out1, out2, keyIn0_0);

input in1, in2, in3, in4, keyIn0_0;
output out1, out2;
wire w1, keyWire0;

and AND1 (out1, in1, keyWire0);
or OR1 (w1, keyWire0, in3);
and AND2 (out2, w1, in4);

xor KeyGate1 (keyWire0, in2, keyIn0_0);

endmodule
