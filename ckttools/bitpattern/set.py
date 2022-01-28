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
        return self.patterns[0].pattern_length()

    def pattern_space_size(self):
        return 2**self.pattern_length()

    def count(self):
        return sum(p.count() for p in self.patterns)
