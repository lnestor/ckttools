def create_const_comparator(moddef, inputs, pattern, pass_index, inverted=False):
    """Creates a comparator that compares a pattern to the inputs

    If the inputs match the pattern, the output of the comparator is 1.
    If they do not match, the output is 0. The invert flag switches
    this behavior.

    TODO:
        - Support multiple patterns. This would require keeping track of
          each input being XORed with 0/1 so we can reuse those gates
          instead of making multiple copies of the same gate
        - Support inversion flag

    Parameters:
        moddef: the module definition AST node
        inputs (list): a list with the input names (str) to compare to the pattern
        pattern (str): a string of 0s and 1s where each index corresponds to
                       to the same index in the inputs list

    Returns:
        the name of the output gate of the comparator

    """
    if len(inputs) != len(pattern):
        print("ERROR: comparator input length doesn't match desired pattern")
        exit(-1)

    xnor_outputs = [None] * len(inputs)

    for i, input_pair in enumerate(zip(inputs, pattern)):
        output_name = "const_comp_xor_%i_%i" % (pass_index, i)
        instance_name = "CONST_COMP_XOR_%i_%i" % (pass_index, i)
        moddef.create_ilist("xnor", instance_name, output_name, input_pair)
        xnor_outputs[i] = output_name

    if inverted:
        output_name = "const_comp_nand_%i" % pass_index
        moddef.create_ilist("nand", "CONST_COMP_NAND_%i" % pass_index, output_name, xnor_outputs)
    else:
        output_name = "const_comp_and_%i" % pass_index
        moddef.create_ilist("and", "CONST_COMP_AND_%i" % pass_index, output_name, xnor_outputs)
    return output_name

def create_mult_const_comparator(moddef, inputs, patterns, pass_index):
    if any([len(inputs) != len(pattern) for pattern in patterns]):
        print("ERROR: comparator input length doesn't match one of the desired patterns")
        exit(-1)

    not_gates = [None] * len(inputs)
    buf_gates = [None] * len(inputs)
    and_gates = [None] * len(patterns)

    for pattern_index, pattern in enumerate(patterns):
        inputs_to_and = [None] * len(inputs)

        for input_index, bit in enumerate(pattern):
            if bit == "0":
                if not_gates[input_index] is None:
                    instance_name = "MULT_COMP_NOT_%i_%i" % (pass_index, input_index)
                    output_name = "mult_comp_not_%i_%i" % (pass_index, input_index)
                    moddef.create_ilist("not", instance_name, output_name, [inputs[input_index]])
                    not_gates[input_index] = output_name

                inputs_to_and[input_index] = not_gates[input_index]
            else:
                if buf_gates[input_index] is None:
                    instance_name = "MULT_COMP_BUF_%i_%i" % (pass_index, input_index)
                    output_name = "mult_comp_buf_%i_%i" % (pass_index, input_index)
                    moddef.create_ilist("buf", instance_name, output_name, [inputs[input_index]])
                    buf_gates[input_index] = output_name

                inputs_to_and[input_index] = buf_gates[input_index]

        instance_name = "MULT_COMP_AND_%i_%i" % (pass_index, pattern_index)
        output_name = "mult_comp_and_%i_%i" % (pass_index, pattern_index)
        moddef.create_ilist("and", instance_name, output_name, inputs_to_and)
        and_gates[pattern_index] = output_name

    gate_type = "or" if len(patterns) > 1 else "buf"
    instance_name = "MULT_COMP_OUTPUT_%i" % pass_index
    output_name = "mult_comp_output_%i" % pass_index
    moddef.create_ilist(gate_type, instance_name, output_name, and_gates)

    return output_name

