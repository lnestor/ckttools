// [KeyGate]: KeyGate0, w1, out1, keyWire0, out1
module primary_inputs_key(in1, ou1, keyIn0_0);

input in1, keyIn0_0;
output out1;
wire w1, keyWire0;

not NOT (w1, in1);
xor SubKeyGate0 (keyWire0, in1, keyIn0_0);
xor KeyGate0 (out1, w1, keyWire0);

endmodule
