from ckttools.keygates.metadata import parse_metadata

VERILOG_WITH_METADATA = """
// Key Gate Metadata:
// [KeyGate]: KeyGate1, circuit_input, output, key_input, original_net
module someverilog();
endmodule
"""
def test_parse_metadata(tmp_path):
    f = tmp_path / "example.v"
    f.write_text(VERILOG_WITH_METADATA)

    metadata = parse_metadata(f)

    assert metadata["KeyGate1"]["key_gate_name"] == "KeyGate1"
    assert metadata["KeyGate1"]["circuit_input_net"] == "circuit_input"
    assert metadata["KeyGate1"]["output_net"] == "output"
    assert metadata["KeyGate1"]["key_input_net"] == "key_input"
    assert metadata["KeyGate1"]["original_circuit_net"] == "original_net"

