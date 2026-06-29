# Own imports
from printer.base_printer import BasePrinter


class StringPrinter(BasePrinter):
    def __init__(self):
        self.registered_generators = []
        self.result = ""

    def register(self, iterable):
        self.registered_generators.append(iterable)

    def print(self):
        for iterable in self.registered_generators:
            for line in iterable:
                self.result = "".join([self.result, line])
        return self.result
