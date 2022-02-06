import bitpattern
from .input_patterns import get_input_patterns
from .key_patterns import get_propagation_events

def measure_propagation_events(moddef, key_metadata, num_samples):
    input_patterns_per_key = get_input_patterns(moddef, key_metadata, num_samples)

    events_per_key = {}
    for key_gate_name in input_patterns_per_key:
        seed_input_patterns = input_patterns_per_key[key_gate_name]
        pattern_generator = bitpattern.Generator(seed_input_patterns)

        events = get_propagation_events(key_metadata["key_gates"][key_gate_name], moddef, pattern_generator, num_samples)
        events_per_key[key_gate_name] = events

    return events_per_key
