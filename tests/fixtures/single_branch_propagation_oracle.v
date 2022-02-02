module single_branch_propagation(in1, in2, in3, out1, out2);

input in1, in2, in3;
output out1, out2;

not NOT1 (w3, in2);
and AND1 (out1, in1, w3);
and AND2 (out2, w3, in3);

endmodule
