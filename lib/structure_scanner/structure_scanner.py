import os
from pathlib import PurePath
# Own imports
from models.config import config
from data.node_attribute import NodeAttribute
from data.node_type import NodeMetadataKey, NodeMetadataTypeValue
from structure_scanner.document_tree.document_tree import DocumentTree
from structure_scanner.document_tree.document_node import DocumentNode
import structure_scanner.metadata_reader.metadata_reader as mr
from structure_scanner.checks.base_check import BaseCheck


class StructureScanner:
    @classmethod
    def _is_escaped(cls, name: str):
        return name.startswith((".", "_"))

    def __init__(self, root_directory: PurePath):
        self.tree = DocumentTree(root=DocumentNode(path=root_directory))
        self.metadata_reader = mr.MetadataReader(config.logger)
        #
        self.pre_dir_checks: list[BaseCheck] = []
        self.post_dir_checks: list[BaseCheck] = []
        self.node_checks: list[BaseCheck] = []
        #
        self.text_type_extensions = set()

    def register_text_type_extensions(self, ext_list: list[str] | tuple[str] | set[[str]]):
        for item in ext_list:
            if not item.startswith("."):
                item = "".join((".", item)).strip()
            self.text_type_extensions.add(item)

    def register_pre_directory_checks(self, check: BaseCheck):
        self.pre_dir_checks.append(check)

    def register_post_directory_checks(self, check: BaseCheck):
        self.post_dir_checks.append(check)

    def register_node_checks(self, check: BaseCheck):
        self.node_checks.append(check)

    def scan(self):
        self._scan(self.tree.get_root())

    def _apply_directory_metadata(self, container: DocumentNode):
        for child in container.children:
            if (child.get_metadata(NodeMetadataKey.TYPE) == NodeMetadataTypeValue.METAFILE
                    and child.get_metadata(NodeMetadataKey.TITLE) is not None):
                container.set_metadata((NodeMetadataKey.TITLE, child.get_metadata(NodeMetadataKey.TITLE)))

    def _apply_checks(self, node: DocumentNode, checks: list[BaseCheck]):
        for check in checks:
            check.check(node)

    def _scan(self, parent_node: DocumentNode):
        self._apply_checks(parent_node, self.pre_dir_checks)
        with (os.scandir(parent_node.path) as contents):
            for scanned_element in contents:
                current_full_path = PurePath(parent_node.path, scanned_element.name)
                new_node = DocumentNode(path=current_full_path)
                if scanned_element.is_dir():
                    self._scan(new_node)
                if scanned_element.is_file():
                    self._apply_checks(new_node, self.node_checks)
                    parent_node.add_child(new_node)
        self._apply_checks(parent_node, self.post_dir_checks)

        # # all directories are containers
        # parent_node.set_metadata((NodeMetadataKey.TYPE, NodeMetadataTypeValue.CONTAINER))
        # # check if current folder is escaped
        # if (self._is_escaped(parent_node.path.name)
        #         or (parent_node.get_parent() is not None
        #             and NodeAttribute.IS_ESCAPED in parent_node.get_parent().get_attributes())):
        #     parent_node.add_attribute(NodeAttribute.IS_ESCAPED)
        # else:
        #     # otherwise it is in outline
        #     parent_node.add_attribute(NodeAttribute.IN_OUTLINE)
        #
        # with (os.scandir(parent_node.path) as contents):
        #     for scanned_element in contents:
        #         current_full_path = PurePath(parent_node.path, scanned_element.name)
        #
        #         if scanned_element.is_file():
        #             self._scan_file(parent_node, current_full_path)
        #
        #         if scanned_element.is_dir():
        #             new_node = DocumentNode(path=current_full_path)
        #             parent_node.add_child(new_node)
        #             self._scan(new_node)
        #
        #     # apply metadata to directory itself - just title so far
        #     self._apply_directory_metadata(parent_node)

    def _scan_file(self, parent_node: DocumentNode, path: PurePath):
        new_node = DocumentNode(path=path)
        file_extension = path.suffix
        # in readable files, read metadata
        if file_extension.lower() in self.text_type_extensions:
            got_meta = self.metadata_reader.get_metadata_from_file(path)
            new_node.metadata = dict(got_meta.metadata)
            # check if type was already set by method above
            if new_node.get_metadata(NodeMetadataKey.TYPE) is None:
                new_node.set_metadata((NodeMetadataKey.TYPE, NodeMetadataTypeValue.TEXT))

        # check if it is image file
        # todo include in tests
        if file_extension.lower() in self.text_type_extensions:
            new_node.set_metadata((NodeMetadataKey.TYPE, NodeMetadataTypeValue.IMAGE))

        # if file did not match any supported extensions list
        # todo include in tests
        if new_node.get_metadata(NodeMetadataKey.TYPE) is None:
            new_node.set_metadata((NodeMetadataKey.TYPE, NodeMetadataTypeValue.UNSUPPORTED))

        # check if it is escaped directly or through parent node
        if NodeAttribute.IS_ESCAPED in parent_node.get_attributes() or self._is_escaped(path.name):
            new_node.add_attribute(NodeAttribute.IS_ESCAPED)

        # after all checks, add ready node
        parent_node.add_child(new_node)
