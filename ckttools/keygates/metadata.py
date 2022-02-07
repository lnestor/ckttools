def parse_metadata(filename):
    with open(filename) as f:
        lines = f.readlines()

    key_gate_metadata = {}
    non_flip_key_inputs = []
    number_incorrect_keys = None

    for line in lines:
        if line.startswith("// [KeyGate]:"):
            raw_info = line.split(":")[1].split(",")

            m = {}
            m["key_gate_name"] = raw_info[0].strip()
            m["circuit_input_net"] = raw_info[1].strip()
            m["output_net"] = raw_info[2].strip()
            m["key_input_net"] = raw_info[3].strip()
            m["original_circuit_net"] = raw_info[4].strip()

            key_gate_metadata[m["key_gate_name"]] = m

        if line.startswith("// [NonFlipKeyInput]:"):
            key = line.split(":")[1].strip()
            non_flip_key_inputs.append(key)

        if line.startswith("// [IncorrectKeys]:"):
            number_incorrect_keys = int(line.split(":")[1])

    return {"key_gates": key_gate_metadata, "non_flip_key_inputs": non_flip_key_inputs, "number_incorrect_keys": number_incorrect_keys}
