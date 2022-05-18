from util.lazyprop import lazyprop

class ChosenDipFinder:
    def __init__(self, moddef, dip_file):
        self._moddef = moddef
        self._dip_file = dip_file

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
            return False

    def get_dip(self):
        inputs = self._moddef.primary_inputs[0:self._n]
        return {input_: val == "1" for input_, val in zip(inputs, self._next)}

    def get_keys(self):
        values = {key: "X" for key in self._moddef.key_inputs}
        return (values, values)

    def add_constraint(self, a, b):
        # No need to do anything
        return


