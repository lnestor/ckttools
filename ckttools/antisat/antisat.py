import easylock
from locking.keys import create_keys
import locking.globals as GLOBALS

def create_xor_gates(moddef, keys, primary_inputs, args):
    primary_input_idx = args["start_input_index"]
    g_gates = [None] * args["key_bits_per_block"]
    gbar_gates = [None] * args["key_bits_per_block"]

    for i in range(args["key_bits_per_block"]):
        instance_name = "G_XOR_%i_%i" % (GLOBALS.pass_index, i)
        output_name = "g_xor_%i_%i" % (GLOBALS.pass_index, i)
        inputs = [keys[i], primary_inputs[primary_input_idx]]
        moddef.create_ilist("xor", instance_name, output_name, inputs)
        g_gates[i] = output_name

        instance_name = "GBAR_XOR_%i_%i" % (GLOBALS.pass_index, i)
        output_name = "gbar_xor_%i_%i" % (GLOBALS.pass_index, i)
        inputs = [keys[i + args["key_bits_per_block"]], primary_inputs[primary_input_idx]]
        moddef.create_ilist( "xor", instance_name, output_name, inputs)
        gbar_gates[i] = output_name

        primary_input_idx += 1

    return g_gates, gbar_gates

def create_antisat_block(moddef, g_gates, gbar_gates):
    f_g = "g_block_%i" % GLOBALS.pass_index
    f_gbar = "gbar_block_%i" % GLOBALS.pass_index
    antisat_output = "antisat_and_%i" % GLOBALS.pass_index

    moddef.create_ilist("and", "G_BLOCK_%i" % GLOBALS.pass_index, f_g, g_gates)
    moddef.create_ilist("nand", "GBAR_BLOCK_%i" % GLOBALS.pass_index, f_gbar, gbar_gates)
    moddef.create_ilist("and", "ANTISAT_AND_%i" % GLOBALS.pass_index, antisat_output, [f_g, f_gbar])

    return antisat_output

def insert_locking(moddef, antisat_output, insertion_net_name):
    instance_name = "FLIP_IT_%i" % GLOBALS.pass_index
    changed_name = "signal_from_circuit_%i" % GLOBALS.pass_index

    moddef.rename_ilist_output(insertion_net_name, changed_name)
    moddef.create_wire(changed_name)
    moddef.create_ilist("xor", instance_name, insertion_net_name, [antisat_output, changed_name], add_output_wire=False)

def run(moddef, args):
    primary_inputs = moddef.primary_inputs

    new_keys = create_keys(moddef, args["start_input_index"], args["key_bits"])
    g_gates, gbar_gates = create_xor_gates(moddef, new_keys, primary_inputs, args)
    antisat_output = create_antisat_block(moddef, g_gates, gbar_gates)
    insert_locking(moddef, antisat_output, args["insertion_net"])

    run_data = {}
    run_data["insertion_net"] = args["insertion_net"]
    run_data["last_input_index"] = args["start_input_index"] + int((args["key_bits"] / 2) - 1)
    return run_data
