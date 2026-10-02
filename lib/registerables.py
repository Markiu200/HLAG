from abc import ABC, abstractmethod
from pathlib import PurePath


class Registerable(ABC):
    def is_delayed(self) -> bool:
        return False

    def is_file(self) -> bool:
        return False

    @abstractmethod
    def get(self):
        pass


class FileRegisterable(Registerable):
    def __init__(self, path: PurePath):
        self.path = path

    def is_file(self) -> bool:
        return True

    def get(self):
        with open(self.path) as f:
            return f.read()


class CodeRegisterable(Registerable):
    def __init__(self, code: str):
        self.code = code

    def get(self):
        return self.code


class DelayedFileRegisterable(FileRegisterable):
    def is_delayed(self) -> bool:
        return True

    def is_file(self) -> bool:
        return True

    def __init__(self, path: PurePath):
        super().__init__(path)


class DelayedCodeRegisterable(CodeRegisterable):
    def is_delayed(self) -> bool:
        return True

    def __init__(self, code: str):
        super().__init__(code)
