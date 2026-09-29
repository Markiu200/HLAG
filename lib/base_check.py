from abc import ABC, abstractmethod
# Own imports
from lib.document_node import DocumentNode


class BaseCheck(ABC):
    @abstractmethod
    def check(self, node: DocumentNode):
        pass
