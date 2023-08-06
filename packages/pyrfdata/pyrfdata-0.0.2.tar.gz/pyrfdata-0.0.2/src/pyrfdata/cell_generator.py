import random
import string


class CellGenerator:
    def __init__(self, spec, last_sequence=None):
        self.spec = spec
        self.params = spec['params']

        self.min = 0 if "min" not in self.params else self.params["min"]
        self.max = 100 if "max" not in self.params else self.params["max"]
        self.length = 3 if "length" not in self.params else self.params["length"]

        self.last_sequence = self.min - 1 if not last_sequence else last_sequence

        self.generate = self.nada
        if spec["name"] == "random_integer":
            self.generate = self.random_integer
        elif spec["name"] == "random_float":
            self.generate = self.random_float
        elif spec["name"] == "random_string":
            self.generate = self.random_string
        elif spec["name"] == "integer_sequence":
            self.generate = self.integer_sequence
        elif spec["name"] == "distribution_of_integers":
            self.generate = self.distribution_of_integers

    def distribution_of_integers(self):
        ranges = self.params["ranges"]
        choices = []
        weights = []
        for r in ranges:
            choices.append(random.randint(r["start"], r["end"]))
            weights.append(int(r["weight"]))
        return self.add_prefix(self.pad(random.choices(choices, weights)[0]))

    def integer_sequence(self):
        prefix = self.params['prefix']
        self.last_sequence += 1
        return prefix + self.pad(self.last_sequence)

    def pad(self, n):
        if "padding" not in self.params:
            return str(n)
        length = self.params["padding"]["length"]
        pad_with = ""
        if "zero_or_space" in self.spec["params"]["padding"]:
            if "zero" == self.spec["params"]["padding"]["zero_or_space"]:
                pad_with = "0"
        padding_format = "{n:" + pad_with + str(length) + "}"
        return padding_format.format(n=n)

    def random_integer(self):
        r = random.randint(self.min, self.max)
        return self.add_prefix(r)

    def random_float(self):
        return self.add_prefix(random.uniform(self.min, self.max))

    def random_string(self):
        return self.add_prefix(''.join(random.choices(string.ascii_letters, k=self.length)))

    def nada(self):
        return ""

    def add_prefix(self, value):
        if 'prefix' in self.params:
            return self.params['prefix'] + str(value)
        else:
            return str(value)
