from ckttools.bench.bench import Bench
from ckttools.bench.parse import parse_from_verilog
from ckttools.propagation.measure import create_test_bench_file, get_key_patterns
from tests.fixtures.fixtures import get_fixture_path
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

def test_get_key_patterns_simple(tmp_path):
    key_gate_info = {
        "key_gate_name": "XOR1",
        "key_gate_output_net": "w1",
        "key_input_net": "keyIn0_0",
        "circuit_input_net": "in1"
    }
    original_bench = parse_from_verilog(get_fixture_path("simple_propagation_locked"))
    fault_filename = tmp_path / "example.flt"
    fault_filename.write_text("w1 /0\nw1 /1\n")

    key_patterns = get_key_patterns(key_gate_info, "01", ["in1", "in2"], original_bench, fault_filename, 0)
    assert key_patterns == ["1"]

def test_get_key_patterns_branching(tmp_path):
    key_gate_info = {
        "key_gate_name": "KeyGate2",
        "key_gate_output_net": "w2",
        "key_input_net": "keyIn0_1",
        "circuit_input_net": "in2"
    }
    original_bench = parse_from_verilog(get_fixture_path("branching_propagation_locked"))
    fault_filename = tmp_path / "example.flt"
    fault_filename.write_text("w2 /0\nw2 /1\n")

    key_patterns = get_key_patterns(key_gate_info, "11", ["in1", "in2"], original_bench, fault_filename, 0)
    assert set(key_patterns) == set(["01", "1x"])

def test_get_key_patterns_single_branch(tmp_path):
    key_gate_info = {
        "key_gate_name": "KeyGate2",
        "key_gate_output_net": "w2",
        "key_input_net": "keyIn0_1",
        "circuit_input_net": "in2"
    }
    original_bench = parse_from_verilog(get_fixture_path("single_branch_propagation_locked"))
    fault_filename = tmp_path / "example.flt"
    fault_filename.write_text("w2 /0\nw2 /1\n")

    key_patterns = get_key_patterns(key_gate_info, "11", ["in1", "in2"], original_bench, fault_filename, 0)
    assert set(key_patterns) == set(["x1"])
