from vast.create import create_moddef, create_inputs, create_wires, create_outputs, create_ilist
from vast.moddef import ModuleDefWrapper
from vast.search import get_ilist_output, get_ilist_inputs, get_ilist_type, get_ilist_name

class MiterBuilder:
    def __init__(self):
        self._inputs = set()
        self._outputs = set()
        self._wires = set()
        self._ilists = []

    def build(self, options):
        self._add_miter_half(options.get_half0(), "__half0")
        self._add_miter_half(options.get_half1(), "__half1")
        self._tie_outputs()
        return self._finalize(options)

    def _add_miter_half(self, options, suffix):
        for input_ in options["moddef"].inputs:
            if input_ in options["no_suffix_inputs"]:
                self._inputs.add(input_)
            elif input_ in options["applied_inputs"]:
                continue
            else:
                self._inputs.add("%s%s" % (input_, suffix))

        for wire in options["moddef"].wires:
            self._wires.add("%s%s" % (wire, suffix))

        for output in options["moddef"].outputs:
            self._outputs.add("%s%s" % (output, suffix))

        for ilist in options["moddef"].ilists:
            output = "%s%s" % (get_ilist_output(ilist), suffix)
            inputs = self._get_ilist_inputs(ilist, options, suffix)
            type_ = get_ilist_type(ilist)
            name = "%s%s" % (get_ilist_name(ilist), suffix)

            self._ilists.append((output, inputs, type_, name))

    def _get_ilist_inputs(self, ilist, options, suffix):
        old_inputs = get_ilist_inputs(ilist)
        new_inputs = [None] * len(old_inputs)

        for i, input_ in enumerate(old_inputs):
            if input_ == 0 or input_ == 1:
                new_inputs[i] = input_
            elif input_ in options["no_suffix_inputs"]:
                new_inputs[i] = input_
            elif input_ in options["applied_inputs"]:
                new_inputs[i] = options["applied_inputs"][input_]
            else:
                new_inputs[i] = "%s%s" % (input_, suffix)

        return new_inputs

    def _tie_outputs(self):
        outputs = sorted(list(self._outputs))
        xor_outputs = []

        for i in range(int(len(outputs) / 2)):
            self._wires.add("miter_xor_%i" % i)
            xor_outputs.append("miter_xor_%i" % i)

        for i in range(int(len(outputs) / 2)):
            output_half0 = outputs[2 * i]
            output_half1 = outputs[2 * i + 1]
            self._ilists.append(("miter_xor_%i" % i, [output_half0, output_half1], "xor", "MITER_XOR_%i" % i))

        self._ilists.append(("diff", xor_outputs, "or", "MITER_OR"))

        self._wires.update(self._outputs)
        self._outputs = set(["diff"])

    def _finalize(self, options):
        moddef = create_moddef(options.name)
        create_inputs(moddef, self._inputs)
        create_wires(moddef, self._wires)
        create_outputs(moddef, self._outputs)

        for ilist in self._ilists:
            create_ilist(moddef, ilist[2], ilist[3], ilist[0], ilist[1], add_output_wire=False)

        return ModuleDefWrapper(moddef)
