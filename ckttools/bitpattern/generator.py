import random

class Generator:
    def __init__(self, seed_patterns):
        self.seeds = seed_patterns

    def sample(self, number_samples):
        self.number = min(number_samples, self.size())
        return iter(self)

    def generate(self):
        pattern = seed = random.choice(self.seeds)

        for i in range(seed.count("x")):
            pattern = pattern.replace("x", random.choice(["0", "1"]), 1)

        return pattern

    def size(self):
        count = 0
        for seed in self.seeds:
            dont_cares = seed.count("x")
            count += 2**dont_cares

        return count

    def __iter__(self):
        self.generated = set()
        return self

    def __next__(self):
        if len(self.generated) >= self.number:
            raise StopIteration

        while True:
            # TODO: issues could arise if # samples is close to # patterns
            #       where this would take forever. Is there a way to narrow
            #       search space? Probably doesn't matter since we'll never
            #       be asking for that many samples unless small circuits
            candidate = self.generate()

            if candidate not in self.generated:
                self.generated.add(candidate)
                return candidate
