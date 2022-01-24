// [LN]: XOR1, IN1, w1, keyIn0_0
// [LN]: XOR2, IN3, w2, keyIn0_1
module sample1(IN1, IN2, IN3, keyIn0_0, keyIn0_1, OUT1, OUT2);

input IN1, IN2, IN3;
input keyIn0_0, keyIn0_1;
output OUT1, OUT2;
wire w1, w2;

xor XOR1 (w1, IN1, keyIn0_0);
xor XOR2 (w2, IN3, keyIn0_1);
and AND1 (OUT1, w1, IN2);
and AND2 (OUT2, IN2, w2);

endmodule
