import argparse
import bitpattern
from propagation import get_propagation_events
from pyverilog.vparser.parser import parse
from vast import search

def get_args():
    parser = argparse.ArgumentParser(description="Calculate p(prop) for a circuit")
    parser.add_argument("locked_filename", help="The locked circuit file")
    parser.add_argument("oracle_filename", help="The oracle file")
    return parser.parse_args()

def get_input_names(filename):
    ast, _ = parse([filename], debug=False)
    return vast.search.get_input_names(ast.children()[0].children()[0])

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
