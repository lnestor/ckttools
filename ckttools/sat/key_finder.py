from .copy import copy_moddef
from .model import extract
from vast.search import get_moddef_from_verilog, get_key_input_names
import z3
from .z3_builder import vast2z3

class KeyFinder:
    def __init__(self, locked):
        self.moddef = get_moddef_from_verilog(locked)
        self.solver = z3.Solver()
        self.iterations = 0

    def get_key(self):
        self.solver.check()
        model = self.solver.model()
        return extract(model, get_key_input_names(self.moddef), completion=True)

    def add_constraint(self, inputs, oracle_output):
        moddef_copy = copy_moddef(self.moddef, input_values=inputs, main_suffix="__iteration%i" % self.iterations)
        outputs = {"%s__iteration%i" % (key, self.iterations): value for key, value in oracle_output.items()}
        moddef_z3 = vast2z3(moddef_copy)

        for z3_repr in moddef_z3:
            self.solver.add(z3_repr)

        for output_name, output_val in outputs.items():
            self.solver.add(z3.Bool(output_name) == output_val)

        self.iterations += 1
