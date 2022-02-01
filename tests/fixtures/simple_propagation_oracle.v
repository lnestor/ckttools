module simple_propagation(in1, in2, out1);

input in1, in2;
output out1;
wire w3;

not NOT1 (w3, in1);
and AND1 (out1, w3, in2);

endmodule
