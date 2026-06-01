from pathlib import PurePath


class DocumentNode:
    def __init__(self, path: PurePath):
        self.children = []
        self.parent = None
        #
        self.path = path
        self.attributes = set()
        self.metadata = dict()

    def add_child(self, child_node: 'DocumentNode'):
        if not isinstance(child_node, DocumentNode):
            raise TypeError(f"Child node is of type {type(child_node)} whereas it should be {type(self)}")

        child_node.parent = self
        self.children.append(child_node)

    def get_parent(self):
        return self.parent

    def get_children(self):
        return self.children

    def add_attribute(self, attribute: str):
        self.attributes.add(attribute)

    def get_attributes(self):
        return self.attributes

    def set_metadata(self, metadata_tuple: (str,str)):
        self.metadata[metadata_tuple[0]] = metadata_tuple[1]

    def get_metadata(self, key):
        if key in self.metadata:
            return self.metadata[key]
        return None
