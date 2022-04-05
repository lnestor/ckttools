from . import antisat

def get_args(config, args):
    args["key_bits"] = config["number-bits"]
    args["key_bits_per_block"] = int(config["number-bits"] / 2)

def run(ast, args):
    return antisat.run(ast, args)
