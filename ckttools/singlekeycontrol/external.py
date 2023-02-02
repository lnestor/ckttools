from . import singlekeycontrol
import math

def get_args(config, args):
    args["key_bits"] = config["number-bits"]
    args["hamming_distance"] = config["hamming-distance"]

    if "percent_correct" in args:
        number_keys = 2**args["key_bits"]
        args["number_correct"] = math.ceil(config["percent-correct"] * number_keys)
    else:
        args["number_correct"] = config["number-correct-keys"]

def run(ast, args):
    return singlekeycontrol.run(ast, args)
