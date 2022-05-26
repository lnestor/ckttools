import argparse
from logic.circuit_solver import CircuitSolver
from sat.dips.dip_finder_factory import DipFinderFactory
from sat.iteration_data import IterationData
from sat.keys.default_key_finder import DefaultKeyFinder
from sat.pretty_print import pp
from vast.moddef import get_moddef_from_verilog

def get_args():
    parser = argparse.ArgumentParser(description="Run a SAT attack")
    parser.add_argument("locked", help="The locked verilog file.")
    parser.add_argument("oracle", help="The unlocked verilog file.")
    parser.add_argument("--csv", help="The file to log metrics to.")
    parser.add_argument("--display-key-elimination", action="store_true", help="Display which keys are eliminated each iteration")
    parser.add_argument("--dips", help="The file with DIPs to run")
    return parser.parse_args()

def display_key_eliminations(keys):
    print("Keys eliminated each iteration:\n")
    for i, iteration in enumerate(keys):
        print("Iteration %i: %s" % (i, " ".join(iteration)))

def run(locked, oracle, args):
    iterations = 0
    # TODO: how to make this based on the circuit?
    #       probably just need metadata unless I do a whole circuit analysis
    #       circuit analysis wouldn't be too hard if the key gates and
    #       integration nodes are named well
    iteration_data = IterationData([4,4,4])

    oracle_runner = CircuitSolver(oracle)
    dip_finder = DipFinderFactory().get(locked, args.dips)
    key_finder = DefaultKeyFinder(locked)

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
    print("\nKey: %s\n" % pp(key))

    # Check if key is correct
    # if args.check_correctness:
        # raise

    if args.display_key_elimination:
        keys = key_finder.keys_eliminated_each_iteration()
        display_key_eliminations(keys)

    # Save data to tmp/sat/last_run or something like that
    return iterations

def main():
    args = get_args()
    locked = get_moddef_from_verilog(args.locked)
    oracle = get_moddef_from_verilog(args.oracle)

    iterations = run(locked, oracle, args)

    if args.csv is not None:
        with open(args.csv, "a") as f:
            f.write("%s,%i\n" % (args.locked, iterations))

if __name__ == "__main__":
    main()
