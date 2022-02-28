import argparse
from sat.dip_finder import DipFinder

def get_args():
    parser = argparse.ArgumentParser(description="Run a SAT attack")
    parser.add_argument("locked", help="The locked verilog file.")
    parser.add_argument("oracle", help="The unlocked verilog file.")
    return parser.parse_args()

def run(locked, oracle):
    iterations = 0
    key_constraints = []
    dip_finder = DipFinder(locked)

    while dip_finder.can_find_dip():
        dip = dip_finder.get_dip()
        oracle_output = run_circuit(oracle, dip)
        dip_finder.add_constraint(dip, oracle_output)

        key_constraints.append((dip, oracle_output))

        iterations += 1

    key = find_key(key_constraints)
    print(iterations)

def main():
    args = get_args()

    run(args.locked, args.oracle)

if __name__ == "__main__":
    main()
