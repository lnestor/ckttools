from .miter import build_miter
from vast.search import get_moddef_from_verilog
import z3

class DipFinder:
    def __init__(self, locked):
        self.moddef = get_moddef_from_verilog(locked)
        self.solver = z3.Solver()

        miter = build_miter(self.moddef)
        self.solver.add(miter == True)

    def can_find_dip(self):
        return self.solver.check() == z3.sat

    def get_dip(self):
        model = self.solver.model()
        return extract(modef, self.primary_inputs)
