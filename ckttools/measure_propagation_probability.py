from atalanta import (
    create_fault_file,
    parse_test_file,
    run_atalanta
)
import argparse
from bench.create import create_bench_file
import os
from pyverilog.vparser.parser import parse
import vast.search

def get_args():
    parser = argparse.ArgumentParser(description="Calculate p(prop) for a circuit")
    parser.add_argument("locked_filename", help="The locked circuit file")
    parser.add_argument("oracle_filename", help="The oracle file")
    return parser.parse_args()

def cleanup(*filenames):
    for filename in filenames:
        os.remove(filename)

def parse_key_gate_info(filename):
    with open(filename) as f:
        lines = f.readlines()

    key_gate_info = {}
    for line in lines:
        if line.startswith("// [LN]:"):
            raw_info = line.split(":")[1].split(",")

            single_key_info = {}
            single_key_info["key_gate_name"] = raw_info[0].strip()
            single_key_info["key_gate_output_net"] = raw_info[2].strip()
            single_key_info["key_input_net"] = raw_info[3].strip()

            circuit_input_net = raw_info[1].strip()
            key_gate_info[circuit_input_net] = single_key_info

    return key_gate_info

def get_input_names(filename):
    ast, _ = parse([filename], debug=False)
    return vast.search.get_input_names(ast.children()[0].children()[0])

def get_input_patterns(filename, net_names):
    create_fault_file("tmp/oracle.flt", net_names)
    create_bench_file("tmp/oracle.bench", filename)

    run_atalanta("tmp/oracle.bench", "tmp/oracle.flt", "tmp/oracle.log", "tmp/oracle.test")
    input_patterns = parse_test_file("tmp/oracle.test")

    cleanup("tmp/oracle.flt", "tmp/oracle.bench", "tmp/oracle.log", "tmp/oracle.test")
    return input_patterns

if __name__ == "__main__":
    args = get_args()
    key_gate_info = parse_key_gate_info(args.locked_filename)
    primary_inputs = get_input_names(args.oracle_filename)
    input_patterns_per_key = get_input_patterns(args.oracle_filename, key_gate_info.keys())

    import pdb; pdb.set_trace()
