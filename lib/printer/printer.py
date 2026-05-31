from pathlib import PurePath
# Own imports
from indent_manager import BaseIndentManager
from printer.base_printer import BasePrinter


class Printer(BasePrinter):
    def __init__(self):
        self.indent_manager = None
        self.output_file_path = None
        self.registered_generators = []

    def set_indent_manager(self, indent_manager: BaseIndentManager):
        self.indent_manager = indent_manager

    def set_output_file_path(self, path: PurePath):
        self.output_file_path = path

    def register(self, iterable):
        self.registered_generators.append(iterable)

    def print(self):
        with open(self.output_file_path, "w") as f:
            for iterable in self.registered_generators:
                for line in iterable:
                    f.write(line)
