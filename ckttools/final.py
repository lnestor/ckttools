import csv
import re
import os
import random
import shutil
import subprocess
import yaml

from flip.calculator import calculate_flip_probability_independent
from vast.graph_search import get_key_inputs_from_subcircuit
from vast.moddef import get_moddef_from_verilog
from vast.search import get_ilist_inputs

MIN_INPUTS_PER_KEYGATE = 3
MAX_INPUTS_PER_KEYGATE = 8

def _choose_circuit(original_path, locked_path):
    originals = os.listdir(original_path)
    lockeds = os.listdir(locked_path)

    to_be_done = [circuit for circuit in originals if circuit not in lockeds]

    if len(to_be_done) == 0:
        raise "No circuits need to be analyzed"

    print("Choosing from %i circuits..." % len(to_be_done))

    basename = random.choice(to_be_done)
    return original_path + "/" + basename

def _choose_keybit_amounts(contents, verilog_filename):
    number_inputs = len(get_moddef_from_verilog(verilog_filename).inputs)
    inputs_used = 0

    for i in range(contents.count("XX")):
        if inputs_used == number_inputs:
            raise "Not enough inputs for locking (%i inputs)" % number_inputs

        max_inputs_to_use = min(number_inputs - inputs_used, MAX_INPUTS_PER_KEYGATE)
        inputs_to_use = random.randint(MIN_INPUTS_PER_KEYGATE, max_inputs_to_use)
        inputs_used += inputs_to_use

        keys = inputs_to_use * 2 # ensure even
        contents = contents.replace("XX", str(keys), 1)

    return contents

def _choose_locking_type(contents):
    # TODO: replace Ys with AntiSAT/SARLock
    # TODO: print small description of locking type (gate type/# keys)
    return contents

def _get_locking_config(path, verilog_filename):
    choices = os.listdir(path)
    choices = ["config6.yaml"]
    base_config = path + "/" + random.choice(choices)

    print("Choosing from %i configuration files..." % len(choices))

    with open(base_config) as f:
        contents = f.read()

    contents = _choose_keybit_amounts(contents, verilog_filename)
    contents = _choose_locking_type(contents)

    working_filename = "./tmp/circuits/working_configs/%s.yaml" % os.path.basename(verilog_filename)[0:-2]
    with open(working_filename, "w") as f:
        f.write(contents)

    return working_filename

def _lock_circuit(unlocked_filename, config, output_path):
    filename = os.path.basename(unlocked_filename)
    output_filename = "%s/%s" % (output_path, filename)

    cmd = [
        "python3",
        "ckttools/easylock.py",
        unlocked_filename,
        "--config",
        config,
        "--output",
        output_filename
    ]

    subprocess.run(cmd)
    return output_filename

def _run_sat_attack(locked_filename, unlocked_filename, log_path):
    savedir, filename = os.path.split(locked_filename)
    csv_filename = "./tmp/circuits/temp_metrics.csv"
    log_filename = "%s/%s.log" % (log_path, filename[0:-2])

    cmd = [
        "python3",
        "ckttools/sat_attack.py",
        locked_filename,
        unlocked_filename,
        "--csv",
        csv_filename
    ]

    with open(log_filename, "w") as f:
        subprocess.run(cmd, stdout=f)

    iterations = -1
    with open(csv_filename) as f:
        reader = csv.reader(f)
        for row in reader:
            iterations = int(row[1])
            break

    os.remove(csv_filename)
    return iterations

def _get_incorrect_keys(net_name, total_key_inputs):
    if "antisat" in net_name:
        return 2**total_key_inputs - 2**int(total_key_inputs / 2)
    else:
        raise

def _measure_single_key_iterations(moddef):
    keygates = moddef.keygates
    key_facing_nets = [get_ilist_inputs(k)[0] for k in keygates]

    flip_probs = [calculate_flip_probability_independent(moddef, n) for n in key_facing_nets]
    total_key_inputs = [len(get_key_inputs_from_subcircuit(moddef, n)) for n in key_facing_nets]
    incorrect_keys = [_get_incorrect_keys(n, t) for n, t in zip(key_facing_nets, total_key_inputs)]

    iterations = [i / (2**t * f) for i, t, f in zip(incorrect_keys, total_key_inputs, flip_probs)]

    return iterations

def _measure_no_interference_iterations(groups):
    return max(groups)

def _measure_direct_interference_iterations(group):
    dip_group_1 = max(group)
    dip_group_2 = max(group) - 1

    return dip_group_1 + dip_group_2

def _measure_min_iterations(circuit_filename):
    moddef = get_moddef_from_verilog(circuit_filename)
    single_key_iterations = _measure_single_key_iterations(moddef)

    # TODO: Need to also include direct interference
    return int(_measure_no_interference_iterations(single_key_iterations))

def main():
    unlocked_path = "./tmp/circuits/original"
    locked_path = "./tmp/circuits/locked"
    log_path = "./tmp/circuits/logs"
    metrics_filename = "./tmp/circuits/metrics.csv"

    unlocked_filename = _choose_circuit(unlocked_path, locked_path)
    print("Chose circuit %s\n" % os.path.basename(unlocked_filename))

    # TODO: synthesize circuit

    locking_config = _get_locking_config("./tmp/circuits/configs", unlocked_filename)
    with open(locking_config, "r") as f:
        basename = os.path.basename(locking_config)
        description = f.readlines()[0][6:-1]
        print("Chose config %s (%s)\n" % (basename, description))

    print("Locking circuit...\n")
    locked_filename = _lock_circuit(unlocked_filename, locking_config, locked_path)

    print("Running SAT attack...")
    actual_iterations = _run_sat_attack(locked_filename, unlocked_filename, log_path)
    print("SAT attack finished in %i iterations\n" % actual_iterations)

    print("Measuring minimum # iterations...\n")
    min_iterations = _measure_min_iterations(locked_filename)
    print("Mininimum # iterations: %i" % min_iterations)

    print("Logging to file...\n")
    with open(metrics_filename, "a") as f:
        f.write("%s,%i,%i\n" % (os.path.basename(unlocked_filename), actual_iterations, min_iterations))
    print("Program complete.\n")

if __name__ == "__main__":
    main()
