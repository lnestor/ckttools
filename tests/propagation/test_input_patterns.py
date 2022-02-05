from ckttools.propagation.input_patterns import get_input_patterns
from ckttools.keygates.metadata import parse_metadata
from ckttools.vast.search import get_moddef_from_verilog
from tests.fixtures.fixtures import get_fixture_path

def test_get_input_patterns_simple():
    locked_filename = get_fixture_path("simple_propagation_locked")
    moddef = get_moddef_from_verilog(locked_filename)
    metadata = parse_metadata(locked_filename)

    input_patterns = get_input_patterns(moddef, metadata)

    # Dont current have a way to combine to to 'dont care' values
    assert set(input_patterns["KeyGate1"]) == set(["01", "11"])
    assert set(input_patterns["KeyGate2"]) == set(["01", "11", "x0"])

def test_get_input_patterns_branching():
    locked_filename = get_fixture_path("branching_propagation_locked")
    moddef = get_moddef_from_verilog(locked_filename)
    metadata = parse_metadata(locked_filename)

    input_patterns = get_input_patterns(moddef, metadata)

    # Dont current have a way to combine to to 'dont care' values
    assert set(input_patterns["KeyGate2"]) == set(["001", "011", "10x", "11x"])

def test_get_input_patterns_single_branch():
    locked_filename = get_fixture_path("single_branch_propagation_locked")
    moddef = get_moddef_from_verilog(locked_filename)
    metadata = parse_metadata(locked_filename)

    input_patterns = get_input_patterns(moddef, metadata)

    # Dont current have a way to combine to to 'dont care' values
    assert set(input_patterns["KeyGate2"]) == set(["x01", "x11"])

def test_get_input_patterns_input_fault():
    locked_filename = get_fixture_path("input_propagation_locked")
    moddef = get_moddef_from_verilog(locked_filename)
    metadata = parse_metadata(locked_filename)

    input_patterns = get_input_patterns(moddef, metadata)

    # Dont current have a way to combine to to 'dont care' values
    assert set(input_patterns["KeyGate1"]) == set(["11xx", "10xx", "0101", "0001"])

def test_get_input_patterns_primary_inputs_used_in_key():
    locked_filename = get_fixture_path("primary_inputs_key_locked")
    moddef = get_moddef_from_verilog(locked_filename)
    metadata = parse_metadata(locked_filename)

    input_patterns = get_input_patterns(moddef, metadata)

    # Dont current have a way to combine to to 'dont care' values
    assert set(input_patterns["KeyGate0"]) == set(["0", "1"])

