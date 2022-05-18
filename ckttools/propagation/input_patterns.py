from atalanta import (
    create_fault_file,
    parse_test_file,
    run_atalanta
)
from bench.parse import parse_from_moddef
import os
from vast.search import get_key_input_names

def cleanup(*filenames):
    for filename in filenames:
        os.remove(filename)

def create_oracle_bench_file(moddef, bench_filename, metadata):
    bench = parse_from_moddef(moddef)
    key_inputs = moddef.key_inputs
    bench.remove_inputs([input_ for input_ in key_inputs if input_ not in metadata["non_flip_key_inputs"]])

    for key_gate_name in metadata["key_gates"]:
        m = metadata["key_gates"][key_gate_name]
        bench.remove_gates_recursive(m["key_input_net"], preserve_inputs=True)
        bench.remove_gate(m["output_net"])
        bench.add_gate(m["output_net"], "buf", [m["circuit_input_net"]])

    with open(bench_filename, "w") as f:
        f.write(str(bench))

def switch_to_key_gate_name(input_patterns, key_metadata):
    gate_name_map = {m["output_net"]: gate_name for gate_name, m in key_metadata.items()}
    return {gate_name_map[output]: patterns for output, patterns in input_patterns.items()}

def get_input_patterns(moddef, metadata, num_samples=None):
    create_oracle_bench_file(moddef, "tmp/oracle.bench", metadata)
    create_fault_file("tmp/oracle.flt", [m["output_net"] for _, m in metadata["key_gates"].items()])

    run_atalanta("tmp/oracle.bench", "tmp/oracle.flt", "tmp/oracle.log", "tmp/oracle.test", num_samples)
    input_patterns = parse_test_file("tmp/oracle.test")
    input_patterns = switch_to_key_gate_name(input_patterns, metadata["key_gates"])

    cleanup("tmp/oracle.flt", "tmp/oracle.bench", "tmp/oracle.log", "tmp/oracle.test")
    return input_patterns
