from .pretty_print import pp
from tabulate import tabulate

INPUT_KEY = lambda x: int(x[1:])

class IterationData:
    def __init__(self, keybits):
        self.keybits = keybits
        self.data = []
        self.iterations = 0

    def add_iteration(self, dip, key1, key2, oracle_output):
        self.iterations += 1
        self.data.append((self.iterations, dip, key1, key2, oracle_output))

    def display(self):
        print("Full Iteration Data:\n")
        self._display_full()
        self._display_key_specific()

    def _display_full(self):
        header = ["Iteration", "Input", "Key1", "Key2", "Output"]
        rows = [self._full_row(i) for i in range(self.iterations)]
        print(tabulate(rows, headers=header))

    def _display_key_specific(self):
        header = ["Iteration", "Input", "Key1", "Key2"]

        for i, bits in enumerate(self.keybits):
            print("\nKey Gate %i Data:\n" % i)
            rows = [self._key_row(i, j, bits) for j in range(self.iterations)]
            print(tabulate(rows, headers=header))

    def _full_row(self, idx):
        data = self.data[idx]
        return [data[0], pp(data[1], key=INPUT_KEY), pp(data[2]), pp(data[3]), pp(data[4])]

    def _key_row(self, keygate_idx, iteration_idx, bits):
        data = self.data[iteration_idx]

        input_start_idx = int(sum([k / 2 for k in self.keybits[0:keygate_idx]]))
        input_end_idx = input_start_idx + int(bits / 2)

        key_start_idx = sum(self.keybits[0:keygate_idx])
        key_end_idx = key_start_idx + bits

        return [data[0], pp(data[1], key=INPUT_KEY)[input_start_idx:input_end_idx], pp(data[2])[key_start_idx:key_end_idx], pp(data[3])[key_start_idx:key_end_idx]]
