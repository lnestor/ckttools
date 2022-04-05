import argparse
from flip.calculator import calculate_flip_probability
from keygates.metadata import parse_metadata
import numpy as np
import probability as prob
from propagation.measure import measure_propagation_events
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

def calculate_probabilities(moddef, m, prop_events, num_samples):
    total_keys = find_total_keys(moddef, m["key_input_net"])
    pflip = calculate_flip_probability(moddef, m["key_input_net"])

    pprop = prop_events[m["key_gate_name"]].get_probability()
    pincorrect = m["number_incorrect_keys"] / total_keys

    return {"pflip": pflip, "pprop": pprop, "pincorrect": pincorrect}

def measure_lambda(moddef, metadata, num_samples):
    prop_events = measure_propagation_events(moddef, metadata, num_samples)
    gate_probs = [calculate_probabilities(moddef, m, prop_events, num_samples) for _, m in metadata["key_gates"].items()]

    # Lambda = 1 - prod(correct) / or(flips)
    num = 1 - np.prod([1 - prob["pincorrect"] for prob in gate_probs])
    den = prob.or_([prob["pflip"] * prob["pprop"] for prob in gate_probs])

    return num / den

def main():
    args = get_args()
    metadata = parse_metadata(args.locked)
    moddef = get_moddef_from_verilog(args.locked)

    lambda_ = measure_lambda(moddef, metadata, args.num_samples)

    import pdb; pdb.set_trace()

if __name__ == "__main__":
    main()
