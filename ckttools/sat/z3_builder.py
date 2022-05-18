from vast.search import get_ilists, get_ilist_output, get_ilist_inputs, get_ilist_type
import z3

def vast2z3_unused(moddef):
    return UnusedZ3Builder().build(moddef)

def vast2z3_default(moddef, key_suffix="", input_values={}):
    return DefaultZ3Builder(key_suffix=key_suffix, input_values=input_values).build(moddef)

class UnusedZ3Builder:
    def __init__(self):
        self.z3_repr = {}

    def build(self, moddef):
        for ilist in moddef.ilists:
            self._build_ilist(ilist)

        return list(self.z3_repr.values())

    def _build_ilist(self, ilist):
        output = get_ilist_output(ilist)
        inputs = get_ilist_inputs(ilist)
        type_ = get_ilist_type(ilist)

        fanin = self._get_fanin(inputs)

        if type_ == "and":
            repr_ = z3.Bool(output) == z3.And(*fanin)
        elif type_ == "nand":
            repr_ = z3.Bool(output) == z3.Not(z3.And(*fanin))
        elif type_ == "or":
            repr_ = z3.Bool(output) == z3.Or(*fanin)
        elif type_ == "nor":
            repr_ = z3.Bool(output) == z3.Not(z3.Or(*fanin))
        elif type_ == "not":
            repr_ = z3.Bool(output) == z3.Not(fanin[0])
        elif type_ == "buf":
            repr_ = z3.Bool(output) == fanin[0]
        elif type_ == "xor":
            repr_ = z3.Bool(output) == self._build_xor(fanin)
        elif type_ == "xnor":
            repr_ = z3.Bool(output) == z3.Not(self._build_xor(fanin))
        else:
            raise

        self.z3_repr[output] = repr_

    def _build_xor(self, fanin):
        total_xor = z3.Xor(fanin[0], fanin[1])

        for i in range(len(fanin) - 2):
            total_xor = z3.Xor(total_xor, fanin[i + 2])

        return total_xor

    def _get_fanin(self, inputs):
        fanin = [None] * len(inputs)

        for i, input_ in enumerate(inputs):
            if input_ == 0 or input_ == 1:
                fanin[i] = input_ == 1
            else:
                fanin[i] = z3.Bool(input_)

        return fanin

class DefaultZ3Builder:
    def __init__(self, key_suffix="", input_values={}):
        self.z3_repr = {}
        self.key_suffix = key_suffix
        self.input_values = input_values

    def build(self, moddef):
        for output in moddef.outputs:
            self._build_ilist(moddef, output)

        return {output: self.z3_repr[output] for output in moddef.outputs}

    def _build_ilist(self, moddef, name):
        if name in self.z3_repr:
            return self.z3_repr[name]

        ilist = moddef.get_ilist(name)
        output = get_ilist_output(ilist)
        inputs = get_ilist_inputs(ilist)
        type_ = get_ilist_type(ilist)

        fanin = [None] * len(inputs)
        for i, input_ in enumerate(inputs):
            if moddef.is_ilist(input_):
                fanin[i] = self._build_ilist(moddef, input_)
            elif moddef.is_input(input_):
                fanin[i] = self._build_input(input_)
            else:
                fanin[i] = name == 1

        if type_ == "and":
            repr_ = z3.And(*fanin)
        elif type_ == "nand":
            repr_ = z3.Not(z3.And(*fanin))
        elif type_ == "or":
            repr_ = z3.Or(*fanin)
        elif type_ == "nor":
            repr_ = z3.Not(z3.Or(*fanin))
        elif type_ == "not":
            repr_ = z3.Not(fanin[0])
        elif type_ == "buf":
            repr_ = fanin[0]
        elif type_ == "xor":
            repr_ = self._build_xor(fanin)
        elif type_ == "xnor":
            repr_ = z3.Not(self._build_xor(fanin))
        else:
            raise

        self.z3_repr[name] = repr_
        return repr_

    def _build_input(self, input_):
        if input_ in self.input_values:
            return self.input_values[input_]
        elif "key" in input_:
            return z3.Bool(input_ + self.key_suffix)
        else:
            return z3.Bool(input_)

    def _build_xor(self, fanin):
        total_xor = z3.Xor(fanin[0], fanin[1])

        for i in range(len(fanin) - 2):
            total_xor = z3.Xor(total_xor, fanin[i + 2])

        return total_xor

