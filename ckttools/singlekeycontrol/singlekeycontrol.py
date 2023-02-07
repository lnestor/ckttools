from .adder import create_adder
import locking.globals as GLOBALS
from locking.keys import create_keys
import math
import random
from subcircuits.constant_comparator import create_const_comparator, create_mult_const_comparator

def _get_correct_keys(args):
    number_correct = args["number_correct"]
    number_keys = 2**args["key_bits"]
    correct_values = random.sample(range(0, number_keys), number_correct)
    correct_patterns = [bin(v)[2:].rjust(args["key_bits"], "0") for v in correct_values]

    return correct_patterns

def _create_compare_pattern(hamming_distance, number_bits):
    bits = bin(hamming_distance)[2:].rjust(10, "0")
    return bits[-number_bits:]

def _create_hamming_dist_xors(moddef, key_inputs, primary_inputs):
    gates = [None] * len(key_inputs)
    for i, input_pair in enumerate(zip(key_inputs, primary_inputs)):
        output_name = "skc_hd_xor_%i_%i" % (GLOBALS.pass_index, i)
        instance_name = "SKC_HD_XOR_%i_%i" % (GLOBALS.pass_index, i)
        moddef.create_ilist("xor", instance_name, output_name, input_pair)
        gates[i] = output_name

    return gates

def _create_hamming_dist_calc(moddef, key_inputs, args):
    primary_inputs = moddef.primary_inputs
    start_idx = args["start_input_index"]

    xor_gates = _create_hamming_dist_xors(moddef, key_inputs, primary_inputs[start_idx:start_idx + len(key_inputs)])
    adder_outputs = create_adder(moddef, xor_gates, GLOBALS.pass_index)
    adder_outputs.reverse()

    compare_pattern = _create_compare_pattern(args["hamming_distance"], len(adder_outputs))
    compare_output = create_const_comparator(moddef, adder_outputs, compare_pattern, GLOBALS.pass_index)

    return compare_output

def _create_mask(moddef, key_inputs, incorrect_key_values):
    mask = create_mult_const_comparator(moddef, key_inputs, incorrect_key_values, GLOBALS.pass_index)
    return mask

def _insert_locking(moddef, calc_output, mask_output, insertion_net_name):
    not_instance_name = "SKC_NOT_%i" % GLOBALS.pass_index
    not_output_name = "skc_not_%i" % GLOBALS.pass_index
    moddef.create_ilist("not", not_instance_name, not_output_name, [mask_output])

    and_instance_name = "SKC_AND_%i" % GLOBALS.pass_index
    and_output_name = "skc_and_%i" % GLOBALS.pass_index
    moddef.create_ilist("and", and_instance_name, and_output_name, [calc_output, not_output_name])

    flip_instance_name = "FLIP_IT_%i" % GLOBALS.pass_index
    flip_changed_name = "signal_from_circuit_%i" % GLOBALS.pass_index

    moddef.rename_ilist_output(insertion_net_name, flip_changed_name)
    moddef.create_wire(flip_changed_name)
    moddef.create_ilist("xor", flip_instance_name, insertion_net_name, [and_output_name, flip_changed_name], add_output_wire=False)

def run(moddef, args):
    correct_key_values = _get_correct_keys(args)

    new_keys = create_keys(moddef, args["start_input_index"], args["key_bits"])
    calc = _create_hamming_dist_calc(moddef, new_keys, args)
    mask = _create_mask(moddef, new_keys, correct_key_values)
    _insert_locking(moddef, calc, mask, args["insertion_net"])

    run_data = {}
    run_data["insertion_net"] = args["insertion_net"]
    run_data["last_input_index"] = args["start_input_index"] + args["key_bits"] - 1
    return run_data
