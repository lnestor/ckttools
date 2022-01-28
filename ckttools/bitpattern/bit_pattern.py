class BitPattern:
    def __init__(self, pattern_str):
        self.pattern_str = pattern_str

    def is_subset_of(self, other):
        if not isinstance(other, BitPattern):
            return False

        if len(self.pattern_str) != len(other.pattern_str):
            return False

        for i in range(len(self.pattern_str)):
            if self.pattern_str[i] == "1" and other.pattern_str[i] == "0":
                return False
            elif self.pattern_str[i] == "0" and other.pattern_str[i] == "1":
                return False
            elif self.pattern_str[i] == "x" and other.pattern_str[i] != "x":
                return False

        return True

    def intersection(self, other):
        if len(self.pattern_str) != len(other.pattern_str):
            raise

        intersect_pattern = ""
        for i in range(len(self.pattern_str)):
            if self.pattern_str[i] == other.pattern_str[i]:
                intersect_pattern += self.pattern_str[i]
            elif self.pattern_str[i] == "1" and other.pattern_str[i] == "x":
                intersect_pattern += "1"
            elif self.pattern_str[i] == "0" and other.pattern_str[i] == "x":
                intersect_pattern += "0"
            elif self.pattern_str[i] == "x" and other.pattern_str[i] == "1":
                intersect_pattern += "1"
            elif self.pattern_str[i] == "x" and other.pattern_str[i] == "0":
                intersect_pattern += "0"
            else:
                return BitPattern("")

        return BitPattern(intersect_pattern)

    def count(self):
        if len(self.pattern_str) == 0:
            return 0
        else:
            return 2**self.pattern_str.count("x")

    def __len__(self):
        return len(self.pattern_str)

    def __str__(self):
        return self.pattern_str

    def __eq__(self, other):
        return self.pattern_str == other.pattern_str
