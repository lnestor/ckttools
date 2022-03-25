import easylock
from locking.keys import create_keys
import locking.globals as GLOBALS
from vast.create import create_ilist, create_wire
from vast.modify import rename_ilist_output
from vast.search import get_primary_input_names, get_ilist_from_output

def create_xor_gates(moddef, keys, primary_inputs, args):
    primary_input_idx = args["start_input_index"]
    g_gates = [None] * args["key_bits_per_block"]
    gbar_gates = [None] * args["key_bits_per_block"]

    for i in range(args["key_bits_per_block"]):
        instance_name = "G_XOR_%i_%i" % (GLOBALS.pass_index, i)
        output_name = "g_xor_%i_%i" % (GLOBALS.pass_index, i)
        inputs = [keys[i], primary_inputs[primary_input_idx]]
        xor_g = create_ilist(moddef, "xor", instance_name, output_name, inputs)
        g_gates[i] = xor_g

        instance_name = "GBAR_XOR_%i_%i" % (GLOBALS.pass_index, i)
        output_name = "gbar_xor_%i_%i" % (GLOBALS.pass_index, i)
        inputs = [keys[i + args["key_bits_per_block"]], primary_inputs[primary_input_idx]]
        xor_gbar = create_ilist(moddef, "xor", instance_name, output_name, inputs)
        gbar_gates[i] = xor_gbar

        primary_input_idx += 1

    return g_gates, gbar_gates

def create_antisat_block(moddef, g_gates, gbar_gates):
    f_g = create_ilist(moddef, "and", "G_BLOCK_%i" % GLOBALS.pass_index, "g_block_%i" % GLOBALS.pass_index, g_gates)
    f_gbar = create_ilist(moddef, "nand", "GBAR_BLOCK_%i" % GLOBALS.pass_index, "gbar_block_%i" % GLOBALS.pass_index, gbar_gates)
    antisat_output = create_ilist(moddef, "and", "ANTISAT_AND_%i" % GLOBALS.pass_index, "antisat_and_%i" % GLOBALS.pass_index, [f_g, f_gbar])
    return antisat_output

def insert_locking(moddef, antisat_output, insertion_net_name):
    instance_name = "FLIP_IT_%i" % GLOBALS.pass_index
    changed_name = "signal_from_circuit_%i" % GLOBALS.pass_index
    create_ilist(moddef, "xor", instance_name, insertion_net_name, [antisat_output, changed_name], add_output_wire=False)

    ilist = get_ilist_from_output(moddef, insertion_net_name)
    rename_ilist_output(ilist, changed_name)
    create_wire(moddef, changed_name)

def run(moddef, args):
    primary_inputs = get_primary_input_names(moddef)

    new_keys = create_keys(moddef, args["start_input_index"], args["key_bits"])
    g_gates, gbar_gates = create_xor_gates(moddef, new_keys, primary_inputs, args)
    antisat_output = create_antisat_block(moddef, g_gates, gbar_gates)
    insert_locking(moddef, antisat_output, args["insertion_net"])

    run_data = {}
    run_data["insertion_net"] = args["insertion_net"]
    run_data["last_input_index"] = args["start_input_index"] + args["key_bits"] - 1
    return run_data
