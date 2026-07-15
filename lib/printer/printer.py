from pathlib import PurePath
import re
import os
# Own imports
from printer.base_printer import BasePrinter
from IndentTracker import IndentTracker


class Printer(BasePrinter):
    def __init__(self):
        self.indent_manager = None
        self.output_file_path = None
        self.registered_generators = []

    def set_output_file_path(self, path: PurePath):
        self.output_file_path = path

    def register(self, iterable):
        self.registered_generators.append(iterable)

    def print(self):
        with open(self.output_file_path, "w") as f:
            for iterable in self.registered_generators:
                for line in iterable:
                    f.write(line)
