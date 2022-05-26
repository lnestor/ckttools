import argparse
from miter.builder import MiterBuilder
from miter.options import MiterOptions
from pyverilog.ast_code_generator.codegen import ASTCodeGenerator
from vast.moddef import get_moddef_from_verilog
import z3
from z3int.z3_builder import vast2z3_default

def get_args():
    parser = argparse.ArgumentParser(description="Checks if a key is correct")
    parser.add_argument("locked", help="The locked verilog file")
    parser.add_argument("unlocked", help="The oracle verilog file")
    parser.add_argument("--key", required=True, help="The key to test")
    return parser.parse_args()

def map_keybits(moddef, key):
    return {input_: int(value) for input_, value in zip(moddef.key_inputs, key)}

def main():
    args = get_args()

    locked_moddef = get_moddef_from_verilog(args.locked)
    unlocked_moddef = get_moddef_from_verilog(args.unlocked)

    primary_inputs = locked_moddef.primary_inputs
    keys = map_keybits(locked_moddef, args.key)

    options = MiterOptions("miter") \
        .half0(locked_moddef) \
        .no_suffix_on_inputs(primary_inputs) \
        .apply_inputs(keys) \
        .half1(unlocked_moddef) \
        .no_suffix_on_inputs(primary_inputs)

    miter_moddef = MiterBuilder().build(options)
    z3_repr = vast2z3_default(miter_moddef)

    solver = z3.Solver()
    solver.add(z3_repr["diff"] == True)

    if solver.check() == z3.sat:
        print("Key is not correct")
    else:
        print("Key is correct")

if __name__ == "__main__":
    main()
