from abc import ABC, abstractmethod
from pathlib import PurePath


class Registerable(ABC):
    @abstractmethod
    def get(self):
        pass


class FileRegisterable(Registerable):
    def __init__(self, path: PurePath):
        self.path = path

    def get(self):
        with open(self.path) as f:
            return f.read()


class CodeRegisterable(Registerable):
    def __init__(self, code: str):
        self.code = code

    def get(self):
        return self.code


class DelayedFileRegisterable(FileRegisterable):
    def __init__(self, path: PurePath):
        super().__init__(path)


class DelayedCodeRegisterable(CodeRegisterable):
    def __init__(self, code: str):
        super().__init__(code)
