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
        if 0 in inputs:
            self._add_false_const()
            inputs = [input_ if input_ != 0 else FALSE_GATE_OUTPUT for input_ in inputs]
        if 1 in inputs:
            self._add_true_const()
            inputs = [input_ if input_ != 1 else TRUE_GATE_OUTPUT for input_ in inputs]

        gate = Gate(output, gate_type, inputs)
        self.gates[output] = gate

    def add_buffer(self, net, next_gate_output=None):
        buffer_output = net + "__buffer"

        if net in self.outputs:
            self.outputs.remove(net)
            self.outputs.append(buffer_output)

        for gate_output in self.gates:
            gate = self.gates[gate_output]

            if next_gate_output is None or gate_output == next_gate_output:
                gate.inputs = [buffer_output if _input == net else _input for _input in gate.inputs]

        gate = Gate(buffer_output, "buf", [net])
        self.gates[buffer_output] = gate
        return buffer_output

    def remove_inputs(self, inputs):
        self.inputs = [i for i in self.inputs if i not in inputs]

    def remove_gate(self, gate_output):
        del self.gates[gate_output]

    def remove_gates_recursive(self, gate_output, preserve_inputs=False):
        self._remove_gates_recursive(gate_output, preserve_inputs)
        check_for_constants = TF_INPUT_NAME in self.inputs

        if check_for_constants:
            self._potentially_remove_constants()

    def _remove_gates_recursive(self, gate_output, preserve_inputs):
        net_name = gate_output

        if net_name == FALSE_GATE_OUTPUT or net_name == TRUE_GATE_OUTPUT:
            return
        elif net_name in self.inputs and not preserve_inputs:
            self.inputs.remove(net_name)
        elif net_name in self.gates:
            for input_ in self.gates[net_name].inputs:
                self._remove_gates_recursive(input_, preserve_inputs)

            del self.gates[net_name]

    def _potentially_remove_constants(self):
        has_false_constant = False
        has_true_constant = False

        for gate_output in self.gates:
            gate = self.gates[gate_output]

            if FALSE_GATE_OUTPUT in gate.inputs and gate_output != TF_NEG_NAME:
                has_false_constant = True

            if TRUE_GATE_OUTPUT in gate.inputs and gate_output != TF_NEG_NAME:
                has_true_constant = True

        if not has_false_constant and FALSE_GATE_OUTPUT in self.gates:
            self.remove_gate(FALSE_GATE_OUTPUT)

        if not has_true_constant and TRUE_GATE_OUTPUT in self.gates:
            self.remove_gate(TRUE_GATE_OUTPUT)

        if not has_false_constant and not has_true_constant:
            self.remove_gates_recursive(TF_NEG_NAME)

    def apply_input_pattern(self, pattern):
        if "0" in pattern.values():
            self._add_false_const()
        if "1" in pattern.values():
            self._add_true_const()

        for gate_output in self.gates:
            gate = self.gates[gate_output]
            gate.inputs = [self._change_to_constants(i, pattern) for i in gate.inputs]

    def _add_false_const(self):
        if TF_INPUT_NAME not in self.inputs:
            self.add_input(TF_INPUT_NAME)
            self.add_gate(TF_NEG_NAME, "not", [TF_INPUT_NAME])

        if FALSE_GATE_OUTPUT not in self.gates:
            self.add_gate(FALSE_GATE_OUTPUT, "and", [TF_INPUT_NAME, TF_NEG_NAME])

    def _add_true_const(self):
        if TF_INPUT_NAME not in self.inputs:
            self.add_input(TF_INPUT_NAME)
            self.add_gate(TF_NEG_NAME, "not", [TF_INPUT_NAME])

        if TRUE_GATE_OUTPUT not in self.gates:
            self.add_gate(TRUE_GATE_OUTPUT, "nand", [TF_INPUT_NAME, TF_NEG_NAME])

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
