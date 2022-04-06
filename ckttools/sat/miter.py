import copy
from vast.create import create_moddef, create_inputs, create_wires, create_outputs, create_ilist
from vast.search import get_primary_input_names, get_key_input_names, get_wire_names, get_output_names, get_ilists, get_ilist_output, get_ilist_name, get_ilist_inputs, get_ilist_type

def build_miter(moddef):
    miter = create_moddef("%s_miter" % (moddef.name))
    _add_miter_half(miter, moddef, "__half0")
    _add_miter_half(miter, moddef, "__half1")
    _tie_outputs(miter)
    return miter

def _add_miter_half(miter, moddef, suffix):
    primary_inputs = get_primary_input_names(moddef)
    create_inputs(miter, primary_inputs)
    create_inputs(miter, ["%s%s" % (i, suffix) for i in get_key_input_names(moddef)])
    create_wires(miter, ["%s%s" % (w, suffix) for w in get_wire_names(moddef)])
    create_outputs(miter, ["%s%s" % (o, suffix) for o in get_output_names(moddef)])

    for ilist in get_ilists(moddef):
        output = "%s%s" % (get_ilist_output(ilist), suffix)
        inputs = _get_ilist_inputs(ilist, suffix, primary_inputs)
        type_ = get_ilist_type(ilist)
        name = "%s%s" % (get_ilist_name(ilist), suffix)

        create_ilist(miter, type_, name, output, inputs, add_output_wire=False)

def _get_ilist_inputs(ilist, suffix, primary_inputs):
    old_inputs = get_ilist_inputs(ilist)
    new_inputs = [None] * len(old_inputs)

    for i, input_ in enumerate(old_inputs):
        if input_ == 0 or input_ == 1:
            new_inputs[i] = input_
        elif input_ in primary_inputs:
            new_inputs[i] = input_
        else:
            new_inputs[i] = "%s%s" % (input_, suffix)

    return new_inputs

def _tie_outputs(miter):
    outputs = sorted(get_output_names(miter))
    create_wires(miter, ["miter_xor_%i" % i for i in range(int(len(outputs) / 2))])

    for i in range(int(len(outputs) / 2)):
        output_half0 = outputs[2 * i]
        output_half1 = outputs[2 * i + 1]

        create_ilist(miter, "xor", "MITER_XOR_%i" % i, "miter_xor_%i" % i, [output_half0, output_half1], add_output_wire=False)

    create_ilist(miter, "or", "MITER_OR", "diff", ["miter_xor_%i" % i for i in range(int(len(outputs) / 2))])
