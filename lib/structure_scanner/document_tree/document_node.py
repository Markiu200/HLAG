from pathlib import PurePath
from data.node_attribute import NodeAttribute
from data.node_type import NodeMetadataTypeValue, NodeMetadataKey


class DocumentNode:
    def __init__(self, path: PurePath):
        self.children: list['DocumentNode'] = []
        self.parent = None
        #
        self.path = path
        self.attributes = set()
        self.metadata = dict()

    def __eq__(self, other: 'DocumentNode'):
        return (self.path == other.path
                and self.attributes == other.attributes
                and self.metadata == other.metadata)

    def __str__(self):
        return f"parent:     {id(self.parent)}\npath:       {self.path}\nattributes: {self.attributes}\nmetadata:   {self.metadata}"

    def add_child(self, child_node: 'DocumentNode'):
        if not isinstance(child_node, DocumentNode):
            raise TypeError(f"Child node is of type {type(child_node)} whereas it should be {type(self)}")

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

    def set_metadata(self, metadata_tuple: (str | NodeMetadataKey, str | NodeMetadataTypeValue)):
        self.metadata[metadata_tuple[0]] = metadata_tuple[1]

    def add_metadata(self, metadata: dict):
        # todo proper logging
        for key, value in metadata.items():
            if key in NodeMetadataKey:
                if key == NodeMetadataKey.TYPE:
                    if value in NodeMetadataTypeValue:
                        self.metadata[key] = value
                    else:
                        print(f"Warning: value of \"{value}\" for node metadata type is not recognized and is skipped.")
                self.metadata[key] = value
            else:
                raise KeyError(f"Error while attempting to add \"{key}\" to node metadata - key not supported")

    def get_metadata(self, key: str | NodeMetadataKey) -> str | NodeMetadataTypeValue | None:
        if key in self.metadata:
            return self.metadata[key]
        return None
