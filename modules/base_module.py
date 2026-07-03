from abc import ABC
from structure_scanner.document_tree.document_node import DocumentNode
from module_manager import ModuleManager


class BaseModule(ABC):
    module_manager = None

    @classmethod
    def set_module_manager(cls, module_manager: ModuleManager):
        cls.module_manager = module_manager

    def __init__(self, node: DocumentNode):
        self.node = node
        self.content: str = ""

    def read(self):
        with open(self.node.path) as f:
            f.seek(self.node.metadata["cursor"])
            self.content = f.read()

    def replace_references(self):
        pass

    def write(self):
    def write(self, output: str) -> str:
        # todo: replacing references
        return output

    @abstractmethod
    def print(self):
        pass
