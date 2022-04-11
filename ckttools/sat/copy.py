from vast.create import create_moddef, create_inputs, create_wires, create_outputs, create_ilist
from vast.search import get_key_input_names, get_wire_names, get_output_names, get_ilists, get_ilist_output, get_ilist_type, get_ilist_inputs, get_ilist_name

def copy_moddef(moddef, input_values=None, key_suffix=None, main_suffix=None):
    copy = create_moddef(_suffix_name(moddef.name, main_suffix))

    key_input_names = get_key_input_names(moddef)
    wire_names = get_wire_names(moddef)
    output_names = get_output_names(moddef)

    create_inputs(copy, [_suffix_name(i, key_suffix) for i in key_input_names])
    create_wires(copy, [_suffix_name(w, main_suffix) for w in wire_names])
    create_outputs(copy, [_suffix_name(o, main_suffix) for o in output_names])

    for ilist in get_ilists(moddef):
        ilist_output = _suffix_name(get_ilist_output(ilist), main_suffix)
        ilist_inputs = _get_ilist_inputs(ilist, input_values, key_suffix, main_suffix, key_input_names)
        ilist_type = get_ilist_type(ilist)
        ilist_name = _suffix_name(get_ilist_name(ilist), main_suffix)

        create_ilist(copy, ilist_type, ilist_name, ilist_output, ilist_inputs, add_output_wire=False)

    return copy

def _suffix_name(original, suffix):
    if suffix is None:
        return original
    else:
        return "%s%s" % (original, suffix)

def _get_ilist_inputs(ilist, input_values, key_suffix, main_suffix, key_input_names):
    old_input_names = get_ilist_inputs(ilist)
    new_input_names = [None] * len(old_input_names)

    for i, input_ in enumerate(old_input_names):
        if input_ == 0 or input_ == 1:
            new_input_names[i] = input_
        elif input_ in input_values:
            new_input_names[i] = 1 if input_values[input_] == True else 0
        elif input_ in key_input_names:
            new_input_names[i] = _suffix_name(input_, key_suffix)
        else:
            new_input_names[i] = _suffix_name(input_, main_suffix)

    return new_input_names
