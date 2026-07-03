# Own imports
from base_module.base_module import BaseModule
from structure_scanner.document_tree.document_node import DocumentNode


class Text(BaseModule):
    def __init__(self, node: DocumentNode):
        super().__init__(node)

    def print(self):
        super().read()
        super().replace_references()
        yield super().write(self.content)
