import os
from pathlib import PurePath
# Own imports
from .document_tree import DocumentNode, DocumentTree
from structure_scanner.metadata_reader.metadata_reader import MetadataReader
from structure_scanner.checks.base_check import BaseCheck


class StructureScanner:
    root_directory = None
    tree = None
    #
    pre_dir_checks: list[BaseCheck] = []
    post_dir_checks: list[BaseCheck] = []
    pre_metaread_node_checks: list[BaseCheck] = []
    post_metaread_node_checks: list[BaseCheck] = []

    @classmethod
    def _is_escaped(cls, name: str):
        return name.startswith((".", "_"))

    @classmethod
    def set_root_directory(cls, path: PurePath):
        cls.root_directory = path

    @classmethod
    def _apply_checks(cls, node: DocumentNode, checks: list[BaseCheck]):
        for check in checks:
            check.check(node)

    @classmethod
    def register_pre_directory_check(cls, check: BaseCheck):
        cls.pre_dir_checks.append(check)

    @classmethod
    def register_post_directory_check(cls, check: BaseCheck):
        cls.post_dir_checks.append(check)

    @classmethod
    def register_pre_metaread_node_check(cls, check: BaseCheck):
        cls.pre_metaread_node_checks.append(check)

    @classmethod
    def register_post_metaread_node_check(cls, check: BaseCheck):
        cls.post_metaread_node_checks.append(check)

    @classmethod
    def scan(cls):
        cls.tree = DocumentTree(root=DocumentNode(path=cls.root_directory))
        cls._scan(cls.tree.get_root())

    @classmethod
    def _scan(cls, parent_node: DocumentNode):
        cls._apply_checks(parent_node, cls.pre_dir_checks)
        with (os.scandir(parent_node.path) as contents):
            for scanned_element in contents:
                current_full_path = PurePath(parent_node.path, scanned_element.name)
                new_node = DocumentNode(path=current_full_path)
                if scanned_element.is_dir():
                    cls._scan(new_node)
                if scanned_element.is_file():
                    # pre_meta_checks
                    cls._apply_checks(new_node, cls.pre_metaread_node_checks)
                    # meta read
                    # got_meta = MetadataReader.get_metadata_from_file(current_full_path)
                    # new_node.add_metadata(got_meta.metadata)
                    # new_node.set_metadata("cursor", got_meta.cursor)
                    # post meta checks
                    cls._apply_checks(new_node, cls.post_metaread_node_checks)
                    parent_node.add_child(new_node)
        cls._apply_checks(parent_node, cls.post_dir_checks)
