from atalanta import (
    create_fault_file,
    parse_test_file,
    run_atalanta
)
from bench.parse import parse_from_verilog
import copy
from .events import Events

def remove_duplicates(l):
    return list(set(l))

def get_pattern_map(input_names, input_pattern):
    return {name: val for name, val in zip(input_names, input_pattern)}

def create_test_bench_file(key_gate_info, input_pattern, primary_inputs, original_bench, output_filename):
    bench = copy.deepcopy(original_bench)

    bench.remove_inputs(primary_inputs)
    bench.remove_gates_recursive(key_gate_info["key_input_net"])
    bench.remove_gate(key_gate_info["key_gate_output_net"])

    bench.add_gate(key_gate_info["key_gate_output_net"], "buf", [key_gate_info["circuit_input_net"]])
    bench.apply_input_pattern(get_pattern_map(primary_inputs, input_pattern))

    with open(output_filename, "w") as f:
        f.write(str(bench))

def get_key_patterns(key_gate_info, input_pattern, primary_inputs, original_bench, iteration):
    bench_filename = "tmp/%s_%i.bench" % (key_gate_info["key_gate_name"], iteration)
    fault_filename = "tmp/%s.flt" % (key_gate_info["key_gate_name"])
    log_filename = "tmp/%s_%i.log" % (key_gate_info["key_gate_name"], iteration)
    test_filename = "tmp/%s_%i.test" % (key_gate_info["key_gate_name"], iteration)

    create_test_bench_file(key_gate_info, input_pattern, primary_inputs, original_bench, bench_filename)
    run_atalanta(bench_filename, fault_filename, log_filename, test_filename)

    key_patterns = parse_test_file(test_filename)[key_gate_info["key_gate_output_net"]]
    key_patterns = remove_duplicates([p[0:-1] for p in key_patterns])
    return key_patterns

def get_propagation_events(key_gate_info, locked_filename, primary_inputs, pattern_generator, num_samples):
    events = Events()
    original_bench = parse_from_verilog(locked_filename)
    create_fault_file("tmp/%s.flt" % key_gate_info["key_gate_name"], [key_gate_info["key_gate_output_net"]])

    for i, input_pattern in enumerate(pattern_generator.sample(num_samples)):
        key_patterns = get_key_patterns(key_gate_info, input_pattern, primary_inputs, original_bench, i)
        events.add(input_pattern, key_patterns)

    return events
