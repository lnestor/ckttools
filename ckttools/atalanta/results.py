import collections

def _is_start_of_net(line):
    return line[0] != " "

def _parse_net_name(line):
    return line.split(" ")[0]

def _parse_pattern(line):
    pattern = line.split(":")[1]
    pattern = pattern.split(" ")[1]
    return pattern

def _start_of_test_patterns(lines):
    for i, line in enumerate(lines):
        if "* Test patterns and fault free responses:" in line:
            return lines[i:]

def parse_test_file(filename):
    with open(filename) as f:
        lines = f.readlines()

    patterns = collections.defaultdict(list)
    for line in _start_of_test_patterns(lines):
        if _is_start_of_net(line):
            current_net_name = _parse_net_name(line)
        else:
            pattern = _parse_pattern(line)
            patterns[current_net_name].append(pattern)

    return dict(patterns)
