from pathlib import PurePath
from data.node_attribute import NodeAttribute


class DocumentNode:
    def __init__(self, path: PurePath):
        self.children: list['DocumentNode'] = []
        self.parent = None
        #
        self.path = path
        self.attributes = set()
        self.metadata = dict()
        self.references: list[str] = []

    def __eq__(self, other: 'DocumentNode'):
        return (self.path == other.path
                and self.attributes == other.attributes
                and self.metadata == other.metadata)

    def __str__(self):
        return f"parent:     {id(self.parent)}\npath:       {self.path}\nattributes: {self.attributes}\nmetadata:   {self.metadata}"

    def add_child(self, child_node: 'DocumentNode'):
        if not isinstance(child_node, DocumentNode):
            raise TypeError(f"Child node is of type {type(child_node)} when it should be {type(self)}")

        child_node.parent = self
        self.children.append(child_node)

    def get_parent(self):
        return self.parent

    def get_children(self):
        return self.children

    def add_attribute(self, attribute: NodeAttribute):
        self.attributes.add(attribute)

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
