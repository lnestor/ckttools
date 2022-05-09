import argparse
from locking.args import default_pass_args
import locking.globals as GLOBALS
from locking.definition import Definition
from pyverilog.ast_code_generator.codegen import ASTCodeGenerator
from vast.moddef import get_moddef, get_ast
import yaml

DEFINITIONS_FILENAME = "ckttools/locking/definitions.yaml"

def get_args():
    parser = argparse.ArgumentParser(description="Lock a circuit using several different locking circuits")
    parser.add_argument("circuit", help="The circuit to lock")
    parser.add_argument("--config", help="The config file containing information on how the lock the circuit", required=True)
    parser.add_argument("-o", "--output", help="The verilog file to output to. Otherwise it will print to the screen.")
    return parser.parse_args()

def get_definitions():
    data = read_yaml(DEFINITIONS_FILENAME)
    return {d["key"]: Definition(d) for d in data["locking-types"]}

def get_config(args):
    config = read_yaml(args.config)
    return config

def print_ast(ast, filename):
    codegen = ASTCodeGenerator()
    rslt = codegen.visit(ast)

    if filename:
        with open(filename, "w") as f:
            f.write(rslt)
    else:
        print(rslt)

def read_yaml(filename):
    with open(filename) as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print("Error parsing yaml file (%s): %s" % (filename, e))
            exit(-1)

    return data

def run_pass(moddef, pass_config, defs, prev_pass_data):
    locking_type = pass_config["locking-type"].lower()
    if locking_type not in defs:
        print("ERROR: locking type %s not recognized" % locking_type)
        exit(-1)

    GLOBALS.pass_index += 1

    args = default_pass_args(moddef, pass_config, prev_pass_data)
    defs[locking_type].get_args(pass_config, args)
    return defs[locking_type].run(moddef, args)

def main():
    args = get_args()
    defs = get_definitions()
    config = get_config(args)

    pass_data = []
    ast = get_ast(args.circuit)
    moddef = get_moddef(ast)

    for idx, pass_config in enumerate(config["passes"]):
        pass_config["index"] = idx
        return_data = run_pass(moddef, pass_config, defs, pass_data)
        pass_data.append(return_data)

    print_ast(ast, args.output)

if __name__ == "__main__":
    main()
