from outline_element import OutlineElement
from pathlib import PurePath


class OutlineNode:
    def __init__(self, element: OutlineElement):
        self.element = element
        self.children = []
        self.parent = None

    def walk(self):
        yield from self._walk(self)

    def _walk(self, node: 'OutlineNode'):
        for child in node.children:
            yield from self._walk(child)

    def add_child(self, element: 'OutlineNode'):
        element.parent = self
        self.children.append(element)

    def get_root(self) -> 'OutlineNode':
        if self.parent is None:
            return self
        self.parent.get_root()

    def get_parent(self) -> 'OutlineNode':
        return self.parent

    def get_element(self) -> OutlineElement:
        return self.element

    def get_size(self) -> int:
        return self._count_nodes(self)

    def _count_nodes(self, node: 'OutlineNode') -> int:
        count = 1
        for child in node.children:
            count += self._count_nodes(child)
        return count

    def is_leaf(self):
        return len(self.children) == 0

    def is_root(self):
        return self.parent is None

    def get_height(self):
        return self._get_height(self)

    def _get_height(self, node: 'OutlineNode'):
        if node.is_leaf():
            return 0

        max_child_height = 0
        for child in node.children:
            child_height = self._get_height(child)
            max_child_height = max(max_child_height, child_height)

        return max_child_height + 1

    def get_depth(self) -> int:
        depth = 0
        if self.is_root():
            return 0
        depth += self.parent.get_depth()
        return depth + 1

    def get_node_by_rel_path(self, rel_path: PurePath):
        return self._get_node(self, rel_path)

    def _get_node(self, node: 'OutlineNode', rel_path: PurePath):
        if node.element.rel_path == rel_path:
            return node

        for child in node.children:
            results = self._get_node(child, rel_path)
            if results:
                return results

        return None
