import importlib

from ckttools.keygates.metadata import parse_metadata
lambda_ = importlib.import_module("ckttools.lambda")
from ckttools.vast.search import get_moddef_from_verilog
from tests.fixtures.fixtures import get_benchmark_path

def test_calculate_lambda_functional_sarlock():
    filename = get_benchmark_path("iscas/c1908/sarlock8")

    moddef = get_moddef_from_verilog(filename)
    metadata = parse_metadata(filename)
    num_samples = 10

    expected = lambda_.measure_lambda(moddef, metadata, num_samples)

    assert expected == 255
