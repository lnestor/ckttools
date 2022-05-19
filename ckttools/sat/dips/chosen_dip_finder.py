from .default_dip_finder import DefaultDipFinder
from util.lazyprop import lazyprop

class ChosenDipFinder:
    def __init__(self, moddef, dip_file):
        self._moddef = moddef
        self._dip_file = dip_file
        self._extra_finder = DefaultDipFinder(moddef)
        self._dips_left = True

    @lazyprop
    def _dip_generator(self):
        with open(self._dip_file) as f:
            self._n = int(f.readline())
            lines = f.readlines()
            inputs = "".join(l.strip().replace(" ", "") for l in lines)

        groups = [inputs[i:i+self._n] for i in range(0, len(inputs), self._n)]
        return iter(groups)

    def can_find_dip(self):
        try:
            self._next = next(self._dip_generator)
            return True
        except StopIteration:
            self._dips_left = False
            return self._extra_finder.can_find_dip()

    def get_dip(self):
        if self._dips_left:
            inputs = self._moddef.primary_inputs
            dip = {input_: val == "1" for input_, val in zip(inputs[0:self._n], self._next)}
            falses = {input_: False for input_ in inputs}
            return {**falses, **dip}
        else:
            return self._extra_finder.get_dip()

    def get_keys(self):
        values = {key: "X" for key in self._moddef.key_inputs}
        return (values, values)

    def add_constraint(self, inputs, oracle_output):
        self._extra_finder.add_constraint(inputs, oracle_output)
