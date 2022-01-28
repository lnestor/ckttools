module sample2(in1, in2, in3, in4, out1, out2);

input in1, in2, in3, in4;
output out1, out2;
wire w1;

and AND1 (out1, in1, in2);
or OR1 (w1, in2, in3);
and AND2 (out2, w1, in4);

endmodule
