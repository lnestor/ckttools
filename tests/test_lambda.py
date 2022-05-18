import importlib
import pytest

from ckttools.keygates.metadata import parse_metadata
lambda_ = importlib.import_module("ckttools.lambda")
from ckttools.vast.moddef import get_moddef_from_verilog
from tests.fixtures.fixtures import get_benchmark_path

@pytest.mark.skip
def test_calculate_lambda_functional_sarlock():
    filename = get_benchmark_path("iscas/c1908/sarlock8")

    moddef = get_moddef_from_verilog(filename)
    metadata = parse_metadata(filename)
    num_samples = 10

    expected = lambda_.measure_lambda(moddef, metadata, num_samples)

    assert expected == 255

def test_calculate_lambda_functional_antisat():
    filename = get_benchmark_path("iscas/c1355/antisat8")

    moddef = get_moddef_from_verilog(filename)
    metadata = parse_metadata(filename)
    num_samples = 10

    expected = lambda_.measure_lambda(moddef, metadata, num_samples)

    assert expected == 16

def test_calculate_lambda_functional_antisat_mux():
    filename = get_benchmark_path("iscas/c1355/antisat4_mux1")

    moddef = get_moddef_from_verilog(filename)
    metadata = parse_metadata(filename)
    num_samples = 10

    expected = lambda_.measure_lambda(moddef, metadata, num_samples)

    assert expected == 8

def test_calculate_lambda_functional_no_interference_same_pflip_no_prop():
    filename  = get_benchmark_path("iscas/c1908/as8_as8_none")

    moddef = get_moddef_from_verilog(filename)
    metadata = parse_metadata(filename)
    num_samples = 10

    expected = lambda_.measure_lambda(moddef, metadata, num_samples)

    assert expected - 8.756539 < 1e-6
