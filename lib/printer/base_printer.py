from abc import ABC, abstractmethod
from pathlib import PurePath
# Own imports
from indent_manager import BaseIndentManager


class BasePrinter(ABC):
    @abstractmethod
    def set_indent_manager(self, indent_manager: BaseIndentManager):
        pass

    @abstractmethod
    def set_output_file_path(self, path: PurePath):
        pass

    @abstractmethod
    def register(self, iterable):
        pass

    @abstractmethod
    def print(self):
        pass
