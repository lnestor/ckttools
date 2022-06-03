import locking.globals as GLOBALS
from locking.keys import create_keys
from .constant_comparator import create_const_comparator
from .signal_comparator import create_signal_comparator

def create_comparator(moddef, key_inputs, primary_inputs, args):
    start_idx = args["start_input_index"]
    chosen_primary_inputs = primary_inputs[start_idx:start_idx + len(key_inputs)]
    comparator = create_signal_comparator(moddef, key_inputs, chosen_primary_inputs, GLOBALS.pass_index)
    return comparator

def add_mask(moddef, comparator, key_inputs, args):
    correct_key = args["correct_key"]
    mask_comparator = create_const_comparator(moddef, key_inputs, correct_key, GLOBALS.pass_index)

    instance_name = "MASK_AND_%i" % GLOBALS.pass_index
    output_name = "mask_and_%i" % GLOBALS.pass_index
    moddef.create_ilist("and", instance_name, output_name, [comparator, mask_comparator])
    return output_name

def insert_locking(moddef, locking_output, insertion_net_name):
    instance_name = "FLIP_IT_%i" % GLOBALS.pass_index
    changed_name = "signal_from_circuit_%i" % GLOBALS.pass_index

    moddef.rename_ilist_output(insertion_net_name, changed_name)
    moddef.create_wire(changed_name)
    moddef.create_ilist("xor", instance_name, insertion_net_name, [locking_output, changed_name], add_output_wire=False)

def run(moddef, args):
    primary_inputs = moddef.primary_inputs

    new_keys = create_keys(moddef, args["start_input_index"], args["key_bits"])
    comparator = create_comparator(moddef, new_keys, primary_inputs, args)
    mask = add_mask(moddef, comparator, new_keys, args)
    insert_locking(moddef, mask, args["insertion_net"])

    run_data = {}
    run_data["insertion_net"] = args["insertion_net"]
    run_data["last_input_index"] = args["start_input_index"] + args["key_bits"] - 1
    return run_data
