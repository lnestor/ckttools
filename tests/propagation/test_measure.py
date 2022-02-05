from ckttools.keygates.metadata import parse_metadata
from ckttools.propagation.measure import measure_propagation_events
from ckttools.vast.search import get_moddef_from_verilog
from tests.fixtures.fixtures import get_benchmark_path

def test_measure_propagation_events_functional_sarlock():
    filename = get_benchmark_path("iscas/c1908/sarlock8")

    moddef = get_moddef_from_verilog(filename)
    metadata = parse_metadata(filename)
    num_samples = 10

    events = measure_propagation_events(moddef, metadata, num_samples)

    assert events["FLIP_IT_0"].get_probability() == 1.0

def test_measure_propagation_events_functional_sarlock_mux1():
    filename = get_benchmark_path("iscas/c1908/sarlock8_mux1")

    moddef = get_moddef_from_verilog(filename)
    metadata = parse_metadata(filename)
    num_samples = 10

    events = measure_propagation_events(moddef, metadata, num_samples)

    assert events["FLIP_IT_0"].get_probability() == 0.5
