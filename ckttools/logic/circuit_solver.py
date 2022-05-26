import copy
from vast.search import get_ilists, get_output_names
import z3
from z3int.z3_builder import vast2z3_unused

class CircuitSolver:
    def __init__(self, moddef):
        z3_repr = vast2z3_unused(moddef)
        self.output_names = moddef.outputs

        self.solver = z3.Solver()
        for repr_ in z3_repr:
            self.solver.add(repr_)

    def solve(self, input_values):
        s = copy.deepcopy(self.solver)

        for name, value in input_values.items():
            input_obj = z3.Bool(name)
            s.add(input_obj == value)

        values = {}
        for name in self.output_names:
            s.push()
            s.add(z3.Bool(name) == True)
            values[name] = s.check() == z3.sat
            s.pop()

        return values
