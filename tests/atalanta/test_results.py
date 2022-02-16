from ckttools.atalanta.results import parse_test_file

FILE_CONTENTS = """* Name of circuit:  tmp/test.bench
* Primary inputs :
  in2 in3 in4 
  in5 in6
  in7
  in8
  in9

* Primary outputs:
  out2
  out3

* Test patterns and fault free responses:

b1 /0
      1: 101 1
b1 /1
      1: 001 0
in4->out2 /0
      1: x11 1
      2: 101 1
in4->out2 /1
      1: x10 0
      2: 100 0
"""

def test_parse_test_file(tmp_path):
    f = tmp_path / "example.test"
    f.write_text(FILE_CONTENTS)

    test_patterns = parse_test_file(f)

    assert test_patterns["b1"] == ["101", "001"]
    assert test_patterns["in4->out2"] == ["x11", "101", "x10", "100"]
