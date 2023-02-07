def _create_full_adder(moddef, A, B, C, pass_index, adder_index):
    xor1_instance = "FA_XOR1_%i_%i" % (pass_index, adder_index)
    xor1_output = "fa_xor1_%i_%i" % (pass_index, adder_index)
    moddef.create_ilist("xor", xor1_instance, xor1_output, [A, B])

    and1_instance = "FA_AND1_%i_%i" % (pass_index, adder_index)
    and1_output = "fa_and1_%i_%i" % (pass_index, adder_index)
    moddef.create_ilist("and", and1_instance, and1_output, [A, B])

    if C == None:
        return (xor1_output, and1_output)
    else:
        xor2_instance = "FA_XOR2_%i_%i" % (pass_index, adder_index)
        xor2_output = "fa_xor2_%i_%i" % (pass_index, adder_index)
        xor2 = moddef.create_ilist("xor", xor2_instance, xor2_output, [xor1_output, C])

        and2_instance = "FA_AND2_%i_%i" % (pass_index, adder_index)
        and2_output = "fa_and2_%i_%i" % (pass_index, adder_index)
        and2 = moddef.create_ilist("and", and2_instance, and2_output, [xor1_output, C])

        or_instance = "FA_OR_%i_%i" % (pass_index, adder_index)
        or_output = "fa_or_%i_%i" % (pass_index, adder_index)
        moddef.create_ilist("or", or_instance, or_output, [and2_output, and1_output])

        return (xor2_output, or_output)

def create_adder(moddef, inputs1, inputs2, pass_index):
    outputs = []

    if len(inputs1) != len(inputs2):
        raise "Invalid input lengths"

    carry_in = None
    for i in range(len(inputs1)):
        sum_out, carry_out = _create_full_adder(inputs1[i], inputs2[i], carry_in, pass_index, i)
        carry_in = carry_out
        outputs[i] = sum_out

    return outputs
