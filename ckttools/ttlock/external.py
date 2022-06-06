from . import ttlock

def get_args(config, args):
    args["key_bits"] = config["number-bits"]
    args["protected_input"] = "1" * int(args["key_bits"])
    args["correct_key"] = "1" * int(args["key_bits"])

def run(ast, args):
    return ttlock.run(ast, args)
