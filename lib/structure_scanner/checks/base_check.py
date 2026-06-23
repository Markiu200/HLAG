from abc import ABC, abstractmethod
from structure_scanner.document_tree.document_node import DocumentNode
# Own imports
if __name__ == "__main__":
    from structure_scanner.structure_scanner import StructureScanner


class BaseCheck(ABC):
    @classmethod
    def set_scanner(cls, scanner: 'StructureScanner'):
        cls.scanner = scanner

    @abstractmethod
    def check(self, node: DocumentNode) -> tuple[dict, set]:
        pass
