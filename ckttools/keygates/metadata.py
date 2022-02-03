def parse_metadata(filename):
    with open(filename) as f:
        lines = f.readlines()

    metadata = {}
    for line in lines:
        if line.startswith("// [KeyGate]:"):
            raw_info = line.split(":")[1].split(",")

            m = {}
            m["key_gate_name"] = raw_info[0].strip()
            m["circuit_input_net"] = raw_info[1].strip()
            m["output_net"] = raw_info[2].strip()
            m["key_input_net"] = raw_info[3].strip()
            m["original_circuit_net"] = raw_info[4].strip()

            metadata[m["key_gate_name"]] = m

    return metadata
