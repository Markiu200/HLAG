from abc import ABC, abstractmethod


class BasePrinter(ABC):
    @abstractmethod
    def register(self, iterable):
        pass

    @abstractmethod
    def print(self):
        pass
