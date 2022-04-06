from .miter import build_miter
from .model import extract
from vast.search import get_moddef_from_verilog, get_primary_input_names
import z3
from .z3_builder import vast2z3

class DipFinder:
    def __init__(self, locked):
        self.moddef = get_moddef_from_verilog(locked)
        self.primary_inputs = get_primary_input_names(self.moddef)
        self.solver = z3.Solver()

        miter = build_miter(self.moddef)
        miter_z3 = vast2z3(miter)

        for z3_repr in miter_z3:
            self.solver.add(z3_repr)
        self.solver.add(z3.Bool("diff") == True)

    def can_find_dip(self):
        return self.solver.check() == z3.sat

    def get_dip(self):
        model = self.solver.model()
        return extract(model, self.primary_inputs)

    # def add_constraint(self, inputs, oracle_output):
