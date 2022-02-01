from ckttools.measure_propagation_probability import get_input_patterns
from tests.fixtures.fixtures import get_fixture_path

def test_get_input_patterns_simple():
    oracle_filename = get_fixture_path("simple_propagation_oracle")
    net_names = ["w3", "out1"]

    input_patterns = get_input_patterns(oracle_filename, net_names)

    # Dont current have a way to combine to to 'dont care' values
    assert set(input_patterns["w3"]) == set(["01", "11"])
    assert set(input_patterns["out1"]) == set(["01", "11", "x0"])

def test_get_input_patterns_branching():
    oracle_filename = get_fixture_path("branching_propagation_oracle")
    net_names = ["out1", "w3", "out2"]

    input_patterns = get_input_patterns(oracle_filename, net_names)

    # Dont current have a way to combine to to 'dont care' values
    assert set(input_patterns["out1"]) == set(["0xx", "10x", "11x"])
    assert set(input_patterns["out2"]) == set(["x01", "x11", "xx0"])
    assert set(input_patterns["w3"]) == set(["001", "011", "10x", "11x"])

