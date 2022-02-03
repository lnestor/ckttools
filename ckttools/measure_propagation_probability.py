from atalanta import (
    create_fault_file,
    parse_test_file,
    run_atalanta
)
import argparse
from bench.parse import parse_from_verilog
import bitpattern
import os
from propagation import get_propagation_events
from pyverilog.vparser.parser import parse
from vast import search

def get_args():
    parser = argparse.ArgumentParser(description="Calculate p(prop) for a circuit")
    parser.add_argument("locked_filename", help="The locked circuit file")
    parser.add_argument("oracle_filename", help="The oracle file")
    return parser.parse_args()

def cleanup(*filenames):
    for filename in filenames:
        os.remove(filename)

def get_input_names(filename):
    ast, _ = parse([filename], debug=False)
    return vast.search.get_input_names(ast.children()[0].children()[0])

def create_oracle_bench_file(verilog_filename, bench_filename, key_metadata):
    bench = parse_from_verilog(verilog_filename)

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

def get_input_patterns(filename, key_metadata):
    create_oracle_bench_file(filename, "tmp/oracle.bench", key_metadata)
    create_fault_file("tmp/oracle.flt", [m["output_net"] for _, m in key_metadata.items()])

    run_atalanta("tmp/oracle.bench", "tmp/oracle.flt", "tmp/oracle.log", "tmp/oracle.test")
    input_patterns = parse_test_file("tmp/oracle.test")
    input_patterns = switch_to_key_gate_name(input_patterns, key_metadata)

    cleanup("tmp/oracle.flt", "tmp/oracle.bench", "tmp/oracle.log", "tmp/oracle.test")
    return input_patterns

if __name__ == "__main__":
    args = get_args()
    key_metadata = keygates.parse_metadata(args.locked_filename)
    primary_inputs = get_input_names(args.oracle_filename)
    input_patterns_per_key = get_input_patterns(args.locked_filename, key_metadata)

    events_per_key = {}
    for key_gate_name in input_patterns_per_key:
        seed_input_patterns = input_patterns_per_key[key_gate_name]
        pattern_generator = bitpattern.Generator(seed_input_patterns)

        events = get_propagation_events(key_metadata[key_gate_name], args.locked_filename, primary_inputs, pattern_generator, 100)
        events_per_key[key_metadata[insertion_net]["key_input_net"]] = events

    import pdb; pdb.set_trace()
