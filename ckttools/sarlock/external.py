import copy

from . import sarlock

def get_args(config, args):
    args["key_bits"] = config["number-bits"]
    args["correct_key"] = "0" * int(args["key_bits"])

def run(ast, args):
    return sarlock.run(ast, args)
