from .copy import copy_moddef
from .miter import build_miter
from .model import extract
from vast.search import get_primary_input_names, get_key_input_names
import z3
from .z3_builder import vast2z3

class DipFinder:
    def __init__(self, moddef):
        self.moddef = moddef
        self.primary_inputs = moddef.primary_inputs
        self.key_inputs = moddef.key_inputs
        self.solver = z3.Solver()
        self.iterations = 0

        miter = build_miter(self.moddef)
        miter_z3 = vast2z3(miter)

        for z3_repr in miter_z3:
            self.solver.add(z3_repr)
        self.solver.add(z3.Bool("diff") == True)

    def can_find_dip(self):
        self.model = None
        return self.solver.check() == z3.sat

    def get_dip(self):
        if self.model is None:
            self.model = self.solver.model()

        return extract(self.model, self.primary_inputs, completion=True)

    def get_keys(self):
        if self.model is None:
            self.model = self.solver.model()

        key1 = extract(self.model, ["%s__half0" % k for k in self.key_inputs], completion=True)
        key2 = extract(self.model, ["%s__half1" % k for k in self.key_inputs], completion=True)

        return key1, key2

    def add_constraint(self, inputs, oracle_output):
        moddef_half0 = copy_moddef(self.moddef, input_values=inputs, key_suffix="__half0", main_suffix="__half0__iteration%i" % self.iterations)
        moddef_half1 = copy_moddef(self.moddef, input_values=inputs, key_suffix="__half1", main_suffix="__half1__iteration%i" % self.iterations)

        outputs_half0 = {"%s__half0__iteration%i" % (key, self.iterations): value for key, value in oracle_output.items()}
        outputs_half1 = {"%s__half1__iteration%i" % (key, self.iterations): value for key, value in oracle_output.items()}

        half0_z3 = vast2z3(moddef_half0)
        half1_z3 = vast2z3(moddef_half1)

        for z3_repr in half0_z3:
            self.solver.add(z3_repr)

        for z3_repr in half1_z3:
            self.solver.add(z3_repr)

        for output_name, output_val in outputs_half0.items():
            self.solver.add(z3.Bool(output_name) == output_val)

        for output_name, output_val in outputs_half1.items():
            self.solver.add(z3.Bool(output_name) == output_val)

        self.iterations += 1
