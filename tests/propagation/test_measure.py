from ckttools.bench.bench import Bench
from ckttools.propagation.measure import create_test_bench_file
import pytest

ORIGINAL_BENCH_CONTENTS = """
# original
#

INPUT(in1)
INPUT(in2)
INPUT(keyIn0_0)
INPUT(keyIn0_1)
INPUT(keyIn0_2)
INPUT(keyIn0_3)

OUTPUT(out1)
OUTPUT(out2)

key_mid = and(keyIn0_0, keyIn0_1)
key_out = xor(key_mid, keyIn0_2)
w1 = xor(key_out, in1)
w2 = xor(keyIn0_3, in2)
out1 = not(w1)
out2 = and(w1, w2)
"""

EXPECTED_BENCH_CONTENTS = """# example
#

INPUT(keyIn0_3)
INPUT(TF_CONST)

OUTPUT(out1)
OUTPUT(out2)

w2 = xor(keyIn0_3, FALSE_CONST)
out1 = not(w1)
out2 = and(w1, w2)
w1 = buf(TRUE_CONST)
TF_CONST_NOT = not(TF_CONST)
FALSE_CONST = and(TF_CONST, TF_CONST_NOT)
TRUE_CONST = nand(TF_CONST, TF_CONST_NOT)
"""

@pytest.fixture
def original_bench():
    bench = Bench("example")
    bench.add_input("in1")
    bench.add_input("in2")

    bench.add_input("keyIn0_0")
    bench.add_input("keyIn0_1")
    bench.add_input("keyIn0_2")
    bench.add_input("keyIn0_3")

    bench.add_output("out1")
    bench.add_output("out2")

    bench.add_gate("key_mid", "and", ["keyIn0_0", "keyIn0_1"])
    bench.add_gate("key_out", "xor", ["key_mid", "keyIn0_2"])
    bench.add_gate("w1", "xor", ["key_out", "in1"])
    bench.add_gate("w2", "xor", ["keyIn0_3", "in2"])
    bench.add_gate("out1", "not", ["w1"])
    bench.add_gate("out2", "and", ["w1", "w2"])

    return bench

def test_create_test_bench_file(tmp_path, original_bench):
    key_gate_info = {
        "key_input_net": "key_out",
        "key_gate_output_net": "w1",
        "circuit_input_net": "in1"
    }

    input_pattern = "10"
    primary_inputs = ["in1", "in2"]
    output_filename = tmp_path / "example.bench"

    create_test_bench_file(key_gate_info, input_pattern, primary_inputs, original_bench, output_filename)

    created_bench_contents = output_filename.read_text()
    assert created_bench_contents == EXPECTED_BENCH_CONTENTS

