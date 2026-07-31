from abc import ABC, abstractmethod
from structure_scanner.document_node import DocumentNode


class BaseCheck(ABC):
    @abstractmethod
    def check(self, node: DocumentNode):
        pass
