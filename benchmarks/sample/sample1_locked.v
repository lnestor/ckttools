// Propagation data:
// gate name, circuit input name, output name, key input name, original circuit net name
// [KeyGate]: KeyGate1, in1, g1, keyIn0_0, in1
// [KeyGate]: KeyGate2, g2, out1, keyIn0_1, out1
// [KeyGate]: KeyGate3, in2, g3, keyIn0_2, in2
// [KeyGate]: KeyGate4, in4, g4, keyIn0_3, in4
module sample2(in1, in2, in3, in4, out1, out2, keyIn0_0, keyIn0_1, keyIn0_2, keyIn0_3);

input in1, in2, in3, in4, keyIn0_0, keyIn0_1, keyIn0_2, keyIn0_3;
output out1, out2;
wire w1, g1, g2, g3, g4;

and AND1 (g2, g1, in2);
or OR1 (w1, g3, in3);
and AND2 (out2, w1, g4);

xor KeyGate1 (g1, in1, keyIn0_0);
and KeyGate2 (out1, g2, keyIn0_1);
and KeyGate3 (g3, in2, keyIn0_2);
xor KeyGate4 (g4, in4, keyIn0_3);

endmodule

