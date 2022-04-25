import argparse
from logic.circuit_solver import CircuitSolver
from sat.dip_finder import DipFinder
from sat.legacy_dip_finder import LegacyDipFinder
from sat.iteration_data import IterationData
from sat.key_finder import KeyFinder
from sat.legacy_key_finder import LegacyKeyFinder
from sat.pretty_print import pp
from vast.moddef import get_moddef_from_verilog

def get_args():
    parser = argparse.ArgumentParser(description="Run a SAT attack")
    parser.add_argument("locked", help="The locked verilog file.")
    parser.add_argument("oracle", help="The unlocked verilog file.")
    parser.add_argument("--csv", help="The file to log metrics to.")
    return parser.parse_args()

def run(locked, oracle):
    iterations = 0
    # TODO: how to make this based on the circuit?
    iteration_data = IterationData([4, 4])

    oracle_runner = CircuitSolver(oracle)
    dip_finder = LegacyDipFinder(locked)
    key_finder = LegacyKeyFinder(locked)

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
    return iterations

def main():
    args = get_args()
    locked = get_moddef_from_verilog(args.locked)
    oracle = get_moddef_from_verilog(args.oracle)

    iterations = run(locked, oracle)

    if args.csv is not None:
        with open(args.csv, "a") as f:
            f.write("%s,%i\n" % (args.locked, iterations))

if __name__ == "__main__":
    main()
