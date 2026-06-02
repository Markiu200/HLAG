import os
from pathlib import PurePath
# Own imports
from models.config import config
from data.node_attributes import NodeAttribute
from structure_scanner.document_tree.document_tree import DocumentTree
from structure_scanner.document_tree.document_node import DocumentNode
from structure_scanner.metadata_reader.metadata_reader import get_metadata


class StructureScanner:
    @classmethod
    def _is_escaped(cls, name: str):
        return name.startswith((".", "_"))

    def __init__(self, root_directory: PurePath):
        self.tree = DocumentTree(root=DocumentNode(path=root_directory))
        #
        self.supported_readable_files_extensions = (".txt", ".json", ".html")

    def scan(self):
        self._scan(self.tree.get_root())

    def _scan(self, parent_node: DocumentNode):
        # check if current folder is escaped
        if (self._is_escaped(parent_node.path.name)
                or (parent_node.get_parent() is not None
                    and NodeAttribute.IS_ESCAPED in parent_node.get_parent().get_attributes())):
            parent_node.add_attribute(NodeAttribute.IS_ESCAPED)
        # otherwise it is in outline
        else:
            parent_node.add_attribute(NodeAttribute.IN_OUTLINE)

        with os.scandir(parent_node.path) as contents:
            for scanned_element in contents:
                current_full_path = PurePath(parent_node.path, scanned_element)

                if scanned_element.is_file():
                    self._scan_file(parent_node, current_full_path)

                if scanned_element.is_dir():
                    new_node = DocumentNode(path=current_full_path)
                    parent_node.add_child(new_node)
                    self._scan(new_node)

                # apply metadata to directory itself - just title so far
                for child in parent_node.children:
                    if child.get_metadata("type") == "metafile" and child.get_metadata("title") is not None:
                        parent_node.set_metadata(("title", child.get_metadata("title")))

    def _scan_file(self, parent_node: DocumentNode, path: PurePath):
        new_node = DocumentNode(path=path)
        file_extension = path.suffix
        if file_extension in self.supported_readable_files_extensions:
            new_node.metadata = dict(get_metadata(path, config.logger))

            if NodeAttribute.IS_ESCAPED in parent_node.get_attributes() or self._is_escaped(path.name):
                new_node.add_attribute(NodeAttribute.IS_ESCAPED)
        parent_node.add_child(new_node)
