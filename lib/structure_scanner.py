import os
from pathlib import PurePath
# Own imports
if __name__ == '__main__':
    from sys import path as sys_path
    sys_path.append(str(PurePath(__file__).parent.parent))
from lib.document_node import DocumentNode
from lib.base_check import BaseCheck


class StructureScanner:
    def __init__(self, root_node: DocumentNode):
        self.root_node = root_node
        self.pre_dir_checks: list[BaseCheck] = []
        self.post_dir_checks: list[BaseCheck] = []
        self.node_checks: list[BaseCheck] = []

    @classmethod
    def _apply_checks(cls, node: DocumentNode, checks: list[BaseCheck]):
        for check in checks:
            check.check(node)

    def add_pre_directory_check(self, check: BaseCheck):
        self.pre_dir_checks.append(check)

    def add_post_directory_check(self, check: BaseCheck):
        self.post_dir_checks.append(check)

    def add_node_check(self, check: BaseCheck):
        self.node_checks.append(check)

    def scan(self):
        self._scan(self.root_node)

    def _scan(self, parent_node: DocumentNode):
        self._apply_checks(parent_node, self.pre_dir_checks)
        #
        with (os.scandir(parent_node.path) as contents):
            dirs = []
            for scanned_element in contents:
                current_full_path = PurePath(parent_node.path, scanned_element.name)
                new_node = DocumentNode(current_full_path, True)
                new_node.set_parent(parent_node)
                if scanned_element.is_dir():
                    dirs.append(new_node)
                if scanned_element.is_file():
                    self._apply_checks(new_node, self.node_checks)
                    parent_node.add_child(new_node)
            #
            self._apply_checks(parent_node, self.post_dir_checks)
            for dir_node in dirs:
                self._scan(dir_node)
                parent_node.add_child(dir_node)


__all__ = [StructureScanner]


if __name__ == '__main__':
    DocumentNode.set_root_path(PurePath(PurePath(__file__).parent.parent, "inputs"))
