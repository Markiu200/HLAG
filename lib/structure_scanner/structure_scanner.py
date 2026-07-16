import os
from pathlib import PurePath
# Own imports
from document_tree import DocumentNode, DocumentTree
from structure_scanner.checks.base_check import BaseCheck


class StructureScanner:
    root_directory = None
    tree: DocumentTree = None
    #
    pre_dir_checks: list[BaseCheck] = []
    post_dir_checks: list[BaseCheck] = []
    node_checks: list[BaseCheck] = []

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
    def register_node_check(cls, check: BaseCheck):
        cls.node_checks.append(check)

    @classmethod
    def scan(cls):
        cls.tree = DocumentTree(root=DocumentNode(path=cls.root_directory))
        cls._scan(cls.tree.get_root())

    @classmethod
    def _scan(cls, parent_node: DocumentNode):
        cls._apply_checks(parent_node, cls.pre_dir_checks)
        with (os.scandir(parent_node.path) as contents):
            for scanned_element in contents:
                dirs = []
                current_full_path = PurePath(parent_node.path, scanned_element.name)
                new_node = DocumentNode(path=current_full_path)
                if scanned_element.is_dir():
                    dirs.append(new_node)
                if scanned_element.is_file():
                    cls._apply_checks(new_node, cls.node_checks)
                    parent_node.add_child(new_node)
            #
            cls._apply_checks(parent_node, cls.post_dir_checks)
            for dir_node in dirs:
                cls._scan(dir_node)
