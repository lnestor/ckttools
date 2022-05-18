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
    parser.add_argument("--display-key-elimination", action="store_true", help="Display which keys are eliminated each iteration")
    return parser.parse_args()

def display_key_eliminations(keys):
    print("Keys eliminated each iteration:\n")
    for i, iteration in enumerate(keys):
        print("Iteration %i: %s" % (i, " ".join(iteration)))

def run(locked, oracle, args):
    iterations = 0
    # TODO: how to make this based on the circuit?
    iteration_data = IterationData([4,4,4])

    oracle_runner = CircuitSolver(oracle)
    dip_finder = LegacyDipFinder(locked)
    key_finder = LegacyKeyFinder(locked)

    ### DIP values here
    in1 = 0
    in2 = 0
    in3 = 0
    in4 = 0
    ###

    print("\nStarting SAT Attack\n")
    while dip_finder.can_find_dip():
        dip = dip_finder.get_dip()
        key1, key2 = dip_finder.get_keys()

        #if iterations < 7:
        #    ### Changes to DIP here
        #    in1_str = "{0:02b}".format(in1)
        #    in2_str = "{0:02b}".format(in2)
        #    in3_str = "{0:02b}".format(in3)
        #    in4_str = "{0:02b}".format(in4)

        #    dip["G1"] = in1_str[0] == "1"
        #    dip["G2"] = in1_str[1] == "1"

        #    dip["G3"] = in2_str[0] == "1"
        #    dip["G4"] = in2_str[1] == "1"

        #    dip["G5"] = in3_str[0] == "1"
        #    dip["G6"] = in3_str[1] == "1"

        #    # dip["G7"] = in4_str[0] == "1"
        #    # dip["G8"] = in4_str[1] == "1"

        #    print(in1_str + " " + in2_str + " " + in3_str + " " + in4_str)

        #    if iterations == 3:
        #        in1 = 0
        #        in2 = 1
        #        in3 = 2
        #        in4 = 3
        #    elif iterations > 3:
        #        in1 = (in1 + 3) % 4
        #        in2 = (in1 + 1) % 4
        #        in3 = (in1 + 2) % 4
        #        in4 = (in1 + 3) % 4

        #        # in1 = (in1 + 3) % 4
        #        # in2 = (in2 + 3) % 4
        #        # in3 = (in3 + 3) % 4
        #        # in4 = (in4 + 3) % 4
        #    else:
        #        in1 = (in1 + 1) % 4
        #        in2 = (in2 + 1) % 4
        #        in3 = (in3 + 1) % 4
        #        in4 = (in4 + 1) % 4
        #    ###

        oracle_output = oracle_runner.solve(dip)

        dip_finder.add_constraint(dip, oracle_output)
        key_finder.add_constraint(dip, oracle_output)

        iterations += 1
        iteration_data.add_iteration(dip, key1, key2, oracle_output)
        print("# Iterations: %i" % iterations)

    iteration_data.display()
    key = key_finder.get_key()
    print("\nKey: %s\n" % pp(key))

    if args.display_key_elimination:
        keys = key_finder.keys_eliminated_each_iteration()
        display_key_eliminations(keys)

    # Save data to tmp/sat/last run or something like that
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