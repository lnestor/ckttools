from atalanta import (
    create_fault_file,
    parse_test_file,
    run_atalanta
)
from bench.parse import parse_from_moddef
import os

def cleanup(*filenames):
    for filename in filenames:
        os.remove(filename)

def create_oracle_bench_file(moddef, bench_filename, key_metadata):
    bench = parse_from_moddef(moddef)

    for key_gate_name in key_metadata:
        m = key_metadata[key_gate_name]
        bench.remove_gates_recursive(m["key_input_net"])
        bench.remove_gate(m["output_net"])
        bench.add_gate(m["output_net"], "buf", [m["circuit_input_net"]])

    with open(bench_filename, "w") as f:
        f.write(str(bench))

def switch_to_key_gate_name(input_patterns, key_metadata):
    gate_name_map = {m["output_net"]: gate_name for gate_name, m in key_metadata.items()}
    return {gate_name_map[output]: patterns for output, patterns in input_patterns.items()}

def get_input_patterns(moddef, key_metadata):
    create_oracle_bench_file(moddef, "tmp/oracle.bench", key_metadata)
    create_fault_file("tmp/oracle.flt", [m["output_net"] for _, m in key_metadata.items()])

    run_atalanta("tmp/oracle.bench", "tmp/oracle.flt", "tmp/oracle.log", "tmp/oracle.test")
    input_patterns = parse_test_file("tmp/oracle.test")
    input_patterns = switch_to_key_gate_name(input_patterns, key_metadata)

    cleanup("tmp/oracle.flt", "tmp/oracle.bench", "tmp/oracle.log", "tmp/oracle.test")
    return input_patterns
