import argparse
from sat.dip_finder import DipFinder
from sat.key_finder import KeyFinder
from logic.circuit_solver import CircuitSolver

def get_args():
    parser = argparse.ArgumentParser(description="Run a SAT attack")
    parser.add_argument("locked", help="The locked verilog file.")
    parser.add_argument("oracle", help="The unlocked verilog file.")
    return parser.parse_args()

def run(locked, oracle):
    iterations = 0
    key_constraints = []

    oracle_runner = CircuitSolver(oracle)
    dip_finder = DipFinder(locked)
    key_finder = KeyFinder(locked)

    while dip_finder.can_find_dip():
        dip = dip_finder.get_dip()
        oracle_output = oracle_runner.solve(dip)

        dip_finder.add_constraint(dip, oracle_output)
        key_finder.add_constraint(dip, oracle_output)

        iterations += 1

    print(iterations)
    key = key_finder.get_key()
    import pdb; pdb.set_trace()

def main():
    args = get_args()

    run(args.locked, args.oracle)

if __name__ == "__main__":
    main()
