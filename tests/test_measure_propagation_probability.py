from ckttools.measure_propagation_probability import get_input_patterns, parse_key_gate_info
from tests.fixtures.fixtures import get_fixture_path

# TODO: add public method to get key gate info from a file and then 
# add key gate info the fixtures

def test_get_input_patterns_simple():
    locked_filename = get_fixture_path("simple_propagation_locked")
    key_gate_info = parse_key_gate_info(locked_filename)

    input_patterns = get_input_patterns(locked_filename, key_gate_info)

    # Dont current have a way to combine to to 'dont care' values
    assert set(input_patterns["KeyGate1"]) == set(["01", "11"])
    assert set(input_patterns["KeyGate2"]) == set(["01", "11", "x0"])

def test_get_input_patterns_branching():
    locked_filename = get_fixture_path("branching_propagation_locked")
    key_gate_info = parse_key_gate_info(locked_filename)

    input_patterns = get_input_patterns(locked_filename, key_gate_info)

    # Dont current have a way to combine to to 'dont care' values
    assert set(input_patterns["KeyGate2"]) == set(["001", "011", "10x", "11x"])

def test_get_input_patterns_single_branch():
    locked_filename = get_fixture_path("single_branch_propagation_locked")
    key_gate_info = parse_key_gate_info(locked_filename)

    input_patterns = get_input_patterns(locked_filename, key_gate_info)

    # Dont current have a way to combine to to 'dont care' values
    assert set(input_patterns["KeyGate2"]) == set(["x01", "x11"])

def test_get_input_patterns_input_fault():
    locked_filename = get_fixture_path("input_propagation_locked")
    key_gate_info = parse_key_gate_info(locked_filename)

    input_patterns = get_input_patterns(locked_filename, key_gate_info)

    # Dont current have a way to combine to to 'dont care' values
    assert set(input_patterns["KeyGate1"]) == set(["11xx", "10xx", "0101", "0001"])
