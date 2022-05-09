from .model import extract
from .pretty_print import pp
import z3
from .z3_builder import vast2z3_legacy

class LegacyKeyFinder:
    def __init__(self, moddef):
        self.moddef = moddef
        self.solver = z3.Solver()
        self.iterations = 0
        self.constraints = []

    def get_key(self):
        self.solver.check()
        model = self.solver.model()
        return extract(model, self.moddef.key_inputs, completion=True)

    def add_constraint(self, inputs, oracle_output):
        self.constraints.append((inputs, oracle_output))

        moddef_z3 = vast2z3_legacy(self.moddef, input_values=inputs)
        constraint = [moddef_z3[name] == oracle_output[name] for name in moddef_z3]
        self.solver.add(*constraint)

        self.iterations += 1

    def keys_eliminated_each_iteration(self):
        keys_eliminated = []
        all_keys = set()

        for constraint in self.constraints:
            dip, oracle_output = constraint

            solver = z3.Solver()
            moddef_z3 = vast2z3_legacy(self.moddef, input_values=dip)
            z3_constraint = [moddef_z3[name] != oracle_output[name] for name in moddef_z3]
            solver.add(z3.Or(*z3_constraint))

            keys_this_iteration = []
            while solver.check() == z3.sat:
                model = solver.model()
                values = extract(model, self.moddef.key_inputs, completion=True)
                exclusion = z3.Or([z3.Bool(k) != v for k, v in values.items()])
                solver.add(exclusion)

                if pp(values) not in all_keys:
                    keys_this_iteration.append(pp(values))
                    all_keys.add(pp(values))

            keys_eliminated.append(keys_this_iteration)

        return keys_eliminated
