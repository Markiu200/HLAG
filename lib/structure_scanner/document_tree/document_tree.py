from structure_scanner.document_tree.document_node import DocumentNode


class DocumentTree:
    def __init__(self, root: DocumentNode):
        self.root = root

    def get_root(self):
        return self.root
