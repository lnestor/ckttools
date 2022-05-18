from ..miter import build_miter
from ..model import extract
from util.lazyprop import lazyprop
import z3
from ..z3_builder import vast2z3_legacy

class DefaultDipFinder:
    def __init__(self, moddef):
        self.moddef = moddef
        self.iterations = 0

    @lazyprop
    def _solver(self):
        s = z3.Solver()
        miter = build_miter(self.moddef)
        miter_z3 = vast2z3_legacy(miter)
        s.add(miter_z3["diff"] == True)
        return s

    def can_find_dip(self):
        self.model = None
        return self._solver.check() == z3.sat

    def get_dip(self):
        if self.model is None:
            self.model = self.solver.model()

        return extract(self.model, self.moddef.primary_inputs, completion=True)

    def get_keys(self):
        if self.model is None:
            self.model = self._solver.model()

        key1 = extract(self.model, ["%s__half0" % k for k in self.moddef.key_inputs], completion=True)
        key2 = extract(self.model, ["%s__half1" % k for k in self.moddef.key_inputs], completion=True)

        return key1, key2

    def add_constraint(self, inputs, oracle_output):
        half0_z3 = vast2z3_legacy(self.moddef, key_suffix="__half0", input_values=inputs)
        half1_z3 = vast2z3_legacy(self.moddef, key_suffix="__half1", input_values=inputs)

        half0_constraints = [half0_z3[name] == oracle_output[name] for name in half0_z3]
        half1_constraints = [half1_z3[name] == oracle_output[name] for name in half1_z3]

        self._solver.add(*half0_constraints)
        self._solver.add(*half1_constraints)

        self.iterations += 1
