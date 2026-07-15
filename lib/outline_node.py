from pathlib import PurePath
from os import sep as system_separator
# Own imports
from config import config


class OutlineNode:
    """Represents node in a tree. It is used to assembly JS navigation.

    Attributes:
        full_path: PurePath - full path of directory or file
    """
    @classmethod
    def get_potential_parent(cls, full_path: PurePath):
        return full_path.parent

    def __init__(self, full_path: PurePath):
        self.children = []
        self.parent = None
        #
        self.full_path = full_path
        #
        self.dom_id_link = None
        self.create_dom_id_link()

    def get_full_rel_path(self):
        return PurePath(*self.full_path.parts[config.base_path_length:])

    def create_dom_id_link(self):
        link_id = str(self.get_full_rel_path()).replace(system_separator, "-")
        if link_id == ".":
            link_id = "root"
        link_id = "".join(["js-link-for-", link_id])
        self.dom_id_link = link_id

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

    def get_node_by_full_path(self, full_path: PurePath):
        return self._get_node(self, full_path)

    def _get_node(self, node: 'OutlineNode', full_path: PurePath):
        if node.full_path == full_path:
            return node

        for child in node.children:
            results = self._get_node(child, full_path)
            if results:
                return results

        return None

    #
    #   Somewhat unused
    #
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
