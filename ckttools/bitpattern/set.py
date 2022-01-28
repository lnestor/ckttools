from .bit_pattern import BitPattern

class Set:
    def __init__(self, patterns):
        if len(patterns) == 0:
            self.patterns = []
        elif isinstance(patterns[0], str):
            self.patterns = [BitPattern(p) for p in patterns]
        elif isinstance(patterns[0], BitPattern):
            self.patterns = patterns

    def intersection(self, other):
        intersections = []
        for p1 in other.patterns:
            for p2 in self.patterns:
                single_intersection = p1.intersection(p2)

                if single_intersection.count() > 0:
                    intersections.append(single_intersection)

        return Set(intersections)

    def pattern_length(self):
        return len(self.patterns[0])

    def total_possible_patterns(self):
        return 2**self.pattern_length()

    def count(self):
        return sum(p.count() for p in self.patterns)

    def __eq__(self, other):
        for pattern in self.patterns:
            if pattern not in other.patterns:
                return False

        for pattern in other.patterns:
            if pattern not in self.patterns:
                return False

        return True
