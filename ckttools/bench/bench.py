from .gate import Gate
import os

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
