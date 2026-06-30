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

    def read(self):
        pass

    def replace_references(self):
        pass

    def write(self):
        pass
