module sample1(IN1, IN2, IN3, OUT1, OUT2);

input IN1, IN2, IN3;
output OUT1, OUT2;

and AND1 (OUT1, IN1, IN2);
and AND2 (OUT2, IN2, IN3);

endmodule
