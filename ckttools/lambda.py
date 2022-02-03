import argparse
from flip.calculator import calculate_flip_probability
from keygates.metadata import parse_metadata
from vast.graph_search import get_key_inputs_from_subcircuit
from vast.search import get_moddef_from_verilog, get_ilists

DESCRIPTION = "Calculate the minimum number of iterations a SAT attack needs to finish"

def get_args():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("locked", help="The locked verilog file")
    return parser.parse_args()

def find_total_keys(moddef, net):
    key_inputs = get_key_inputs_from_subcircuit(moddef, net)
    return 2**len(key_inputs)

def main():
    args = get_args()
    key_metadata = parse_metadata(args.locked)
    moddef = get_moddef_from_verilog(args.locked)

    for gate_name in key_metadata:
        m = key_metadata[gate_name]

        total_keys = find_total_keys(moddef, m["key_input_net"])
        pflip = calculate_flip_probability(get_ilists(moddef), m["key_input_net"])

        # Calculate # incorrect keys
        # Calculate p(prop)
        # lambda >= p(incorrect) / (p(prop) * p(flip))

        import pdb; pdb.set_trace()

if __name__ == "__main__":
    main()
