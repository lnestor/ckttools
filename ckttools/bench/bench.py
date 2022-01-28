from .gate import Gate
import os

TF_INPUT_NAME = "TF_CONST"
TF_NEG_NAME = "TF_CONST_NOT"
TRUE_GATE_OUTPUT = "TRUE_CONST"
FALSE_GATE_OUTPUT = "FALSE_CONST"

class Bench:
    def __init__(self, circuit_name):
        self.inputs = []
        self.outputs = []
        self.gates = {}
        self.name = circuit_name

    def add_input(self, i):
        self.inputs.append(i)

    def add_output(self, o):
        self.outputs.append(o)

    def add_gate(self, output, gate_type, inputs):
        gate = Gate(output, gate_type, inputs)
        self.gates[output] = gate

    def remove_inputs(self, inputs):
        self.inputs = [i for i in self.inputs if i not in inputs]

    def remove_gate(self, gate_output):
        del self.gates[gate_output]

    def remove_gates_recursive(self, gate_output):
        net_name = gate_output

        if net_name in self.inputs:
            self.inputs.remove(net_name)
        elif net_name in self.gates:
            for input_ in self.gates[net_name].inputs:
                self.remove_gates_recursive(input_)

            del self.gates[net_name]

    def apply_input_pattern(self, pattern):
        self.add_input(TF_INPUT_NAME)
        self.add_gate(TF_NEG_NAME, "not", [TF_INPUT_NAME])

        if "0" in pattern.values():
            self.add_gate(FALSE_GATE_OUTPUT, "and", [TF_INPUT_NAME, TF_NEG_NAME])
        if "1" in pattern.values():
            self.add_gate(TRUE_GATE_OUTPUT, "nand", [TF_INPUT_NAME, TF_NEG_NAME])

        for gate_output in self.gates:
            gate = self.gates[gate_output]
            gate.inputs = [self._change_to_constants(i, pattern) for i in gate.inputs]

    def _change_to_constants(self, input_, pattern):
        if input_ not in pattern:
            return input_

        if pattern[input_] == "0":
            return FALSE_GATE_OUTPUT
        else:
            return TRUE_GATE_OUTPUT

    def __str__(self):
        s = ""
        s += "# %s\n" % self.name
        s += "#\n"

        s += "\n"
        for i in self.inputs:
            s += "INPUT(%s)\n" % i

        s += "\n"
        for o in self.outputs:
            s += "OUTPUT(%s)\n" % o

        s += "\n"
        for output, gate in self.gates.items():
            s += "%s\n" % gate

        return s
