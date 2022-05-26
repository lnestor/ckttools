from miter.builder import MiterBuilder
from miter.options import MiterOptions
import z3
from z3int.z3_builder import vast2z3_default

def check_key_correctness(locked_moddef, unlocked_moddef, keys):
    primary_inputs = locked_moddef.primary_inputs

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
