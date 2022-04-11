import argparse
from logic.circuit_solver import CircuitSolver
from sat.dip_finder import DipFinder
from sat.iteration_data import IterationData
from sat.key_finder import KeyFinder
from sat.pretty_print import pp

# TODO: make this faster by potentially not rebuilding the moddef every time

def get_args():
    parser = argparse.ArgumentParser(description="Run a SAT attack")
    parser.add_argument("locked", help="The locked verilog file.")
    parser.add_argument("oracle", help="The unlocked verilog file.")
    return parser.parse_args()

def run(locked, oracle):
    iterations = 0
    # TODO: how to make this based on the circuit?
    iteration_data = IterationData([2, 12])
    # iteration_data = IterationData([4])

    oracle_runner = CircuitSolver(oracle)
    # TODO: legacy DIP finder
    dip_finder = DipFinder(locked)
    key_finder = KeyFinder(locked)

    print("\nStarting SAT Attack\n")
    while dip_finder.can_find_dip():
        dip = dip_finder.get_dip()
        key1, key2 = dip_finder.get_keys()
        oracle_output = oracle_runner.solve(dip)

        dip_finder.add_constraint(dip, oracle_output)
        key_finder.add_constraint(dip, oracle_output)

        iterations += 1
        iteration_data.add_iteration(dip, key1, key2, oracle_output)
        print("# Iterations: %i" % iterations)

    iteration_data.display()
    key = key_finder.get_key()
    print("\nKey: %s" % pp(key))

    # Save data to tmp/sat/last run or something like that

def main():
    args = get_args()
    run(args.locked, args.oracle)

if __name__ == "__main__":
    main()
