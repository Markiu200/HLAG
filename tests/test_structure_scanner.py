import unittest
import sys
from pathlib import PurePath
from enum import Enum
# Own imports
sys.path.append("D:\\hlag")
sys.path.append("D:\\hlag\\lib")

from structure_scanner.structure_scanner import StructureScanner
from data.node_attribute import NodeAttribute
from data.node_type import NodeMetadataKey, NodeMetadataTypeValue
from structure_scanner.document_tree.document_node import DocumentNode
from structure_scanner.document_tree.document_tree import DocumentTree
# Checks
sys.path.append("D:\\hlag\\lib\\structure_scanner\\checks")
from structure_scanner.checks.unsupported_scan import UnsupportedScan

global_root = ""


def prt(path: PurePath | str | None) -> PurePath:
    """Prepend root"""
    if path is None:
        return PurePath(global_root)
    return PurePath(global_root, path)


def wch(parent: DocumentNode, children: list[DocumentNode]) -> DocumentNode:
    """With children"""
    for child in children:
        parent.add_child(child)
    return parent


def wmt(node: DocumentNode, metadata: dict) -> DocumentNode:
    """With metadata"""
    node.add_metadata(metadata)
    return node


def wat(node: DocumentNode, attributes: set) -> DocumentNode:
    """With attributes"""
    for attribute in attributes:
        node.add_attribute(attribute)
    return node


class TestStructureScanner(unittest.TestCase):
    def setUp(self):
        global global_root
        global_root = PurePath("D:\\hlag\\tests\\test_structures_for_structure_scanner")

    def test_one_unsupported(self):
        structure_scanner = StructureScanner(PurePath("D:\\hlag\\tests\\test_structures_for_structure_scanner\\one_unsupported"))
        structure_scanner.register_node_checks(UnsupportedScan())
        structure_scanner.scan()

        expected_tree = DocumentTree(
            wch(DocumentNode(PurePath(prt("one_unsupported"))), [
                wmt(DocumentNode(PurePath(prt("one_unsupported\\unsupported.txt.old"))), {NodeMetadataKey.TYPE: NodeMetadataTypeValue.UNSUPPORTED})
            ])
        )

        self.assertEqual(structure_scanner.tree, expected_tree)


if __name__ == "__main__":
    unittest.main(verbosity=2)
    print()
