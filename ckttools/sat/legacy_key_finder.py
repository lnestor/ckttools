from .model import extract
import z3
from .z3_builder import vast2z3_legacy

class LegacyKeyFinder:
    def __init__(self, moddef):
        self.moddef = moddef
        self.solver = z3.Solver()
        self.iterations = 0

    def get_key(self):
        self.solver.check()
        model = self.solver.model()
        return extract(model, self.moddef.key_inputs, completion=True)

    def add_constraint(self, inputs, oracle_output):
        moddef_z3 = vast2z3_legacy(self.moddef, input_values=inputs)
        constraint = [moddef_z3[name] == oracle_output[name] for name in moddef_z3]
        self.solver.add(*constraint)

        self.iterations += 1
