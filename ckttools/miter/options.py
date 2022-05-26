class MiterOptions:
    def __init__(self, name):
        self.name = name
        self._options = [self._template(), self._template()]

    def half0(self, moddef):
        self.half = 0
        self._options[self.half]["moddef"] = moddef
        return self

    def half1(self, moddef):
        self.half = 1
        self._options[self.half]["moddef"] = moddef
        return self

    def apply_inputs(self, inputs):
        self._options[self.half]["applied_inputs"] = inputs
        return self

    def no_suffix_on_inputs(self, inputs):
        self._options[self.half]["no_suffix_inputs"] = inputs
        return self

    def copy_to_half1(self):
        self._options[1] = self._options[0]
        return self

    def get_half0(self):
        return self._options[0]

    def get_half1(self):
        return self._options[1]

    def _template(self):
        return {"moddef": None, "applied_inputs": {}, "no_suffix_inputs": []}
