from pathlib import PurePath
from os.path import sep
from typing import Union
from os import path as os_path
# Own imports
if __name__ == '__main__':
    from sys import path as sys_path
    sys_path.append(str(PurePath(__file__).parent.parent))
from lib.models.dn_ref import Ref
from lib.models.dn_data import Data


class DocumentNode:
    root_path = None

    @classmethod
    def set_root_path(cls, root_path: PurePath):
        if not os_path.isdir(str(root_path)):
            raise NotADirectoryError()
        cls.root_path = root_path

    def __init__(self, path: PurePath, is_file: bool):
        self.children: list['DocumentNode'] = []
        self.parent = None
        #
        self.path = path
        self.attributes = set()
        self.metadata = dict()
        self.is_file = is_file
        self.ref: None | Ref = None
        self.nested_refs: list[Ref] = []
        self.record: str | None = None  # JSON record that pm module controller can use to create HTML object
        #
        self.set_metadata("relPath", self.get_rel_path())
        self.set_metadata("hostPath", self.get_metadata("relPath"))

    def __iter__(self):
        for child in self.children:
            if len(child.children) > 0:
                yield from child
            yield child

    def compare_node(self, other: 'DocumentNode'):
        return (self.path == other.path
                and self.attributes == other.attributes
                and self.metadata == other.metadata
                and self.is_file == other.is_file)

    def compare_tree(self, other: 'DocumentNode'):
        own_nodes = [node for node in self]
        other_nodes = [node for node in other]
        #
        length_difference = len(own_nodes) - len(other_nodes)
        if length_difference != 0:
            return False
        #
        for own_node in own_nodes:
            other_node = other.get_node_by_path(own_node.path)
            if own_node != other_node:
                return False
        return True

    def get_node_by_path(self, path: PurePath) -> Union['DocumentNode', None]:
        if self.path == path:
            return self
        return self._get_node_by_path(path, self)

    def _get_node_by_path(self, path: PurePath, node: 'DocumentNode') -> Union['DocumentNode', None]:
        for cur_node in node.get_children():
            if cur_node.path == path:
                return cur_node
            if len(cur_node.get_children()) > 0:
                self._get_node_by_path(path, cur_node)

    def get_rel_path(self):
        return str(self.path).replace(str(DocumentNode.root_path), "_").replace(sep, "_")

    def add_child(self, child_node: 'DocumentNode'):
        if not isinstance(child_node, type(self)):
            raise TypeError(f"Child node is of type {type(child_node)} when it should be {type(self)}")
        child_node.parent = self
        self.children.append(child_node)

    def get_parent(self):
        return self.parent

    def set_parent(self, parent_node: 'DocumentNode'):
        self.parent = parent_node

    def get_children(self):
        return self.children

    def add_attribute(self, attribute):
        self.attributes.add(attribute)

    def remove_attribute(self, attribute):
        self.attributes.remove(attribute)

    def has_attribute(self, attribute: str) -> bool:
        return attribute in self.attributes

    def get_attributes(self) -> set:
        return self.attributes

    def set_metadata(self, key: str, value):
        self.metadata[key] = value

    def add_metadata(self, metadata: dict):
        # todo proper logging
        for key, value in metadata.items():
            self.metadata[key] = value

    def get_metadata(self, key: str):
        if key in self.metadata:
            return self.metadata[key]
        return None


__all__ = [DocumentNode]
