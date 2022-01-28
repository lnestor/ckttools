from ckttools.bench.bench import Bench
import pytest

@pytest.fixture
def complex_bench():
    bench = Bench("test_file")
    bench.add_input("input1")
    bench.add_input("input2")
    bench.add_input("input3")
    bench.add_output("output")
    bench.add_gate("w1", "and", ["input1", "input2"])
    bench.add_gate("w2", "or", ["w1", "input3"])
    bench.add_gate("output", "buf", ["w2"])
    return bench

def test_add_input():
    bench = Bench("test_file")
    assert "new_input" not in str(bench)
    bench.add_input("new_input")
    assert "new_input" in str(bench)

def test_add_output():
    bench = Bench("test_file")
    assert "new_output" not in str(bench)
    bench.add_output("new_output")
    assert "new_output" in str(bench)

def test_add_gate():
    bench = Bench("test_file")
    assert "output = and(input1, input2)" not in str(bench)
    bench.add_gate("output", "and", ["input1", "input2"])
    assert "output = and(input1, input2)" in str(bench)

def test_remove_inputs():
    bench = Bench("test_file")
    bench.add_input("input1")
    bench.add_input("input2")
    assert "input1" in str(bench)
    assert "input2" in str(bench)
    bench.remove_inputs(["input1"])
    assert not "input1" in str(bench)
    assert "input2" in str(bench)

def test_remove_gate():
    bench = Bench("test_file")
    bench.add_gate("output1", "and", ["input1", "input2"])
    bench.add_gate("output2", "and", ["input1", "input2"])
    assert "output1 = and(input1, input2)" in str(bench)
    assert "output2 = and(input1, input2)" in str(bench)
    bench.remove_gate("output1")
    assert not "output1 = and(input1, input2)" in str(bench)
    assert "output2 = and(input1, input2)" in str(bench)

def test_remove_gates_recursive(complex_bench):
    complex_bench.remove_gates_recursive("w2")
    assert "w1 = and(input1, input2)" not in str(complex_bench)
    assert "w2 = or(w1, input3)" not in str(complex_bench)

def test_apply_input_pattern(complex_bench):
    complex_bench.apply_input_pattern({"input1": "1", "input2": "0", "input3": "1"})
    assert "w1 = and(TRUE_CONST, FALSE_CONST)" in str(complex_bench)
    assert "w2 = or(w1, TRUE_CONST)" in str(complex_bench)
    assert "TRUE_CONST = nand(TF_CONST, TF_CONST_NOT)" in str(complex_bench)
    assert "FALSE_CONST = and(TF_CONST, TF_CONST_NOT)" in str(complex_bench)
