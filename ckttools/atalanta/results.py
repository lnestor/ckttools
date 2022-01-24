import collections

def is_start_of_net(line):
    return line[0] != " "

def parse_net_name(line):
    return line.split(" ")[0]

def parse_pattern(line):
    pattern = line.split(":")[1]
    pattern = pattern.split(" ")[1]
    return pattern

def parse_test_file(filename):
    with open(filename) as f:
        lines = f.readlines()

    patterns = collections.defaultdict(list)
    for line in lines[9:]:
        if is_start_of_net(line):
            current_net_name = parse_net_name(line)

        else:
            pattern = parse_pattern(line)
            patterns[current_net_name].append(pattern)

    return dict(patterns)
