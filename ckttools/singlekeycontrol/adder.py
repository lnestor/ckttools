import math

def _create_half_adder(moddef, A, B, pass_index, stage_index, ha_index):
    sum_instance_name = "ADDER_HA_SUM_pass%i_stage%i_ha%i" % (pass_index, stage_index, ha_index)
    sum_output_name = "adder_ha_sum_pass%i_stage%i_ha%i" % (pass_index, stage_index, ha_index)
    moddef.create_ilist("xor", sum_instance_name, sum_output_name, [A, B])

    cout_instance_name = "ADDER_HA_COUT_pass%i_stage%i_ha%i" % (pass_index, stage_index, ha_index)
    cout_output_name = "adder_ha_cout_pass%i_stage%i_ha%i" % (pass_index, stage_index, ha_index)
    moddef.create_ilist("and", cout_instance_name, cout_output_name, [A, B])

    return sum_output_name, cout_output_name

# TODO: this isn't a true adder, this sums the number of 1s in the signal.
#       it should be renamed accordingly
def create_adder(moddef, inputs, pass_index):
    num_stages = len(inputs) - 1

    A_input_index = 0
    B_inputs = [inputs[1]]

    for i in range(num_stages):
        num_HAs = i + 1

        A_input = inputs[A_input_index]
        next_B_inputs = [None] * (num_HAs + 1)

        for j in range(num_HAs):
            ha_sum, ha_cout = _create_half_adder(moddef, A_input, B_inputs[j], pass_index, i, j)
            next_B_inputs[j] = ha_sum
            A_input = ha_cout

        next_B_inputs[-1] = A_input
        B_inputs = next_B_inputs
        A_input_index = i + 2

    num_bits_needed = math.floor(math.log2(len(inputs))) + 1
    last_stage_outputs = B_inputs[0:num_bits_needed]
    return last_stage_outputs
