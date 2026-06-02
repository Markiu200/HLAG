from pathlib import PurePath
# Own imports
from structure_scanner.document_tree.document_node import DocumentNode


class DocumentTree:
    def __init__(self, root: DocumentNode):
        self.root = root

    def __iter__(self):
        yield self.root
        yield from self._iter_loop(self.root)

    def _iter_loop(self, node: DocumentNode):
        for child in node.children:
            yield child
            if len(child.children) > 0:
                self._iter_loop(child)

    def get_root(self):
        return self.root

    def get_node_by_path(self, path: PurePath) -> DocumentNode | None:
        if self.root.path == path:
            return self.root
        return self._get_node_by_path(path, self.root)

    def _get_node_by_path(self, path: PurePath, node: DocumentNode):
        for cur_node in node.get_children():
            if cur_node.path == path:
                return cur_node
            if len(cur_node.get_children()) > 0:
                self._get_node_by_path(path, cur_node)
