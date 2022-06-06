import locking.globals as GLOBALS
from locking.keys import create_keys
from sarlock.signal_comparator import create_signal_comparator
from sarlock.constant_comparator import create_const_comparator

def create_key_comparator(moddef, key_inputs, args):
    start_idx = args["start_input_index"]
    chosen_primary_inputs = moddef.primary_inputs[start_idx:start_idx + len(key_inputs)]
    comparator = create_signal_comparator(moddef, key_inputs, chosen_primary_inputs, GLOBALS.pass_index)
    return comparator

def create_modify_comparator(moddef, key_inputs, args):
    start_idx = args["start_input_index"]
    chosen_primary_inputs = moddef.primary_inputs[start_idx:start_idx + len(key_inputs)]
    comparator = create_const_comparator(moddef, chosen_primary_inputs, args["protected_input"], GLOBALS.pass_index)
    return comparator

def insert_locking(moddef, key_check, modify_output, args):
    modify_instance_name = "MODIFY_%i" % GLOBALS.pass_index
    changed_name = "signal_from_circuit_%i" % GLOBALS.pass_index
    modify_output_name = "modify_%i" % GLOBALS.pass_index

    moddef.rename_ilist_output(args["insertion_net"], changed_name)
    moddef.create_wire(changed_name)
    moddef.create_ilist("xor", modify_instance_name, modify_output_name, [modify_output, changed_name])

    restore_instance_name = "RESTORE_%i" % GLOBALS.pass_index
    moddef.create_ilist("xor", restore_instance_name, args["insertion_net"], [key_check, modify_output_name], add_output_wire=False)

def run(moddef, args):
    new_keys = create_keys(moddef, args["start_input_index"], args["key_bits"])
    key_check = create_key_comparator(moddef, new_keys, args)
    modify_output = create_modify_comparator(moddef, new_keys, args)
    insert_locking(moddef, key_check, modify_output, args)

    run_data = {}
    run_data["insertion_net"] = args["insertion_net"]
    run_data["last_input_index"] = args["start_input_index"] + int(args["key_bits"]) - 1
    return run_data
