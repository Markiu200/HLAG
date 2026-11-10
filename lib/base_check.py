from abc import ABC, abstractmethod
# Own imports
from lib.document_node import DocumentNode


class BaseCheck(ABC):
    def __init__(self):
        self.check_priority = 10

    @abstractmethod
    def check(self, node: DocumentNode):
        pass
