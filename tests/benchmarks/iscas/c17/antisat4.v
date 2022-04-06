

module c17
(
  N1,
  N2,
  N3,
  N6,
  N7,
  N22,
  N23,
  keyIn_0_0,
  keyIn_0_1,
  keyIn_0_2,
  keyIn_0_3
);

  input N1;input N2;input N3;input N6;input N7;
  input keyIn_0_0;
  input keyIn_0_1;
  input keyIn_0_2;
  input keyIn_0_3;
  output N22;output N23;
  wire N10;wire N11;wire N16;wire N19;
  wire g_xor_0_0;
  wire gbar_xor_0_0;
  wire g_xor_0_1;
  wire gbar_xor_0_1;
  wire g_block_0;
  wire gbar_block_0;
  wire antisat_and_0;
  wire signal_from_circuit_0;

  nand
  NAND2_1
  (
    N10,
    N1,
    N3
  );


  nand
  NAND2_2
  (
    N11,
    N3,
    N6
  );


  nand
  NAND2_3
  (
    N16,
    N2,
    N11
  );


  nand
  NAND2_4
  (
    N19,
    N11,
    N7
  );


  nand
  NAND2_5
  (
    signal_from_circuit_0,
    N10,
    N16
  );


  nand
  NAND2_6
  (
    N23,
    N16,
    N19
  );


  xor
  G_XOR_0_0
  (
    g_xor_0_0,
    keyIn_0_0,
    N1
  );


  xor
  GBAR_XOR_0_0
  (
    gbar_xor_0_0,
    keyIn_0_2,
    N1
  );


  xor
  G_XOR_0_1
  (
    g_xor_0_1,
    keyIn_0_1,
    N2
  );


  xor
  GBAR_XOR_0_1
  (
    gbar_xor_0_1,
    keyIn_0_3,
    N2
  );


  and
  G_BLOCK_0
  (
    g_block_0,
    g_xor_0_0,
    g_xor_0_1
  );


  nand
  GBAR_BLOCK_0
  (
    gbar_block_0,
    gbar_xor_0_0,
    gbar_xor_0_1
  );


  and
  ANTISAT_AND_0
  (
    antisat_and_0,
    g_block_0,
    gbar_block_0
  );


  xor
  FLIP_IT_0
  (
    N22,
    antisat_and_0,
    signal_from_circuit_0
  );


endmodule

