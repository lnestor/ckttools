import pytest
from pyverilog.vparser.parser import parse
from ckttools.locking.filters import get_filter
from ckttools.vast.search import get_net_names, get_moddef

VERILOG = """
module test_module(in1, in2, in3, in4, out1, out2, keyIn0_0);

input in1, in2, in3, in4;
input keyIn0_0;
output out1, out2;
wire w1, w2;
wire w3;

and AND1 (out1, in1, in2);
buf BUF1 (w2, in2);
xor XOR1 (w3, w2, keyIn0_0);
or OR1 (w1, w3, in3);
and AND2 (out2, w1, in4);

endmodule
"""

@pytest.fixture(scope="module")
def moddef():
    ast, _ = parse([VERILOG], debug=False)
    return get_moddef(ast)

def test_unknown_filter(moddef, capfd):
    filter_ = get_filter("other", None, 0)
    nets = get_net_names(moddef)

    out, err = capfd.readouterr()
    assert out == "WARNING: unknown insertion filter other\n"
    assert filter_.filter(moddef, nets, {}) == nets

def test_filter_with_no_valid_nets(capfd, moddef):
    filter_ = get_filter("net-name", "other", 0)
    nets = get_net_names(moddef)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        filter_.filter(moddef, nets, {})

    out, err = capfd.readouterr()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == -1
    assert out == "ERROR: pass has no valid insertion net\n"

def test_net_type_filter_output(moddef):
    filter_ = get_filter("net-type", "output", 0)
    nets = get_net_names(moddef)

    assert filter_.filter(moddef, nets, {}) == ["out1", "out2"]

def test_net_type_filter_last_two_input_gate_non_output(moddef):
    filter_ = get_filter("net-type", "output-adjacent-non-unary", 0)
    nets = get_net_names(moddef)

    assert filter_.filter(moddef, nets, {}) == ["w1"]

def test_net_type_filter_previous(moddef):
    filter_ = get_filter("net-type", "previous", 1)
    nets = get_net_names(moddef)
    prev_pass_data = [{"insertion_net": "w2"}]

    assert filter_.filter(moddef, nets, prev_pass_data) == ["w2"]

def test_net_type_filter_other(moddef, capfd):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        filter_ = get_filter("net-type", "other", 0)

    out, err = capfd.readouterr()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == -1
    assert out == "ERROR: unknown net type other in insertion filter\n"

def test_net_name_filter(moddef):
    filter_ = get_filter("net-name", "w1", 0)
    nets = get_net_names(moddef)

    assert filter_.filter(moddef, nets, {}) == ["w1"]

def test_interference_filter_type_none(moddef):
    filter_ = get_filter("interference", {"type": "none", "passes": [0]}, 1)
    nets = get_net_names(moddef)
    prev_pass_data = [{"insertion_net": "w2"}]

    assert filter_.filter(moddef, nets, prev_pass_data) == ["in1", "out1"]

def test_interference_filter_type_none_multiple_passes(moddef):
    filter_ = get_filter("interference", {"type": "none", "passes": [0, 1]}, 2)
    nets = get_net_names(moddef)
    prev_pass_data = [{"insertion_net": "w2"}, {"insertion_net": "w3"}]

    assert filter_.filter(moddef, nets, prev_pass_data) == ["in1", "out1"]

def test_interference_filter_type_indirect(moddef):
    filter_ = get_filter("interference", {"type": "indirect", "passes": [0]}, 1)
    nets = get_net_names(moddef)
    prev_pass_data = [{"insertion_net": "w3"}]

    assert filter_.filter(moddef, nets, prev_pass_data) == ["in3", "in4"]

def test_interference_filter_type_indirect_with_hops(moddef):
    filter_ = get_filter("interference", {"type": "indirect", "passes": [0], "hops": 1}, 1)
    nets = get_net_names(moddef)
    prev_pass_data = [{"insertion_net": "w3"}]

    assert filter_.filter(moddef, nets, prev_pass_data) == ["in4"]

@pytest.mark.skip
def test_interference_filter_type_indirect_multiple_passes(moddef):
    return
