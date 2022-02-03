import argparse
from keygates.metadata import parse_metadata

DESCRIPTION = "Calculate the minimum number of iterations a SAT attack needs to finish"

def get_args():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("locked", help="The locked verilog file")
    return parser.parse_args()

def main():
    args = get_args()
    key_metadata = parse_metadata(args.locked)

    # Note that these are for a single key gate
    # Calculate total # keys
    # Calculate # incorrect keys
    # Calculate p(flip)
    # Calculate p(prop)

    # lambda >= p(incorrect) / (p(prop) * p(flip))

if __name__ == "__main__":
    main()
