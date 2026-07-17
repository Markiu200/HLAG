import unittest
import sys
from pathlib import PurePath

# Own imports
sys.path.append("D:\\hlag")
sys.path.append("D:\\hlag\\lib")

from structure_scanner.structure_scanner import StructureScanner
from data.node_type import NodeMetadataKey, NodeMetadataTypeValue
from structure_scanner.document_node import DocumentNode
from structure_scanner.document_tree import DocumentTree
# Checks
sys.path.append("D:\\hlag\\lib\\structure_scanner\\checks")
from structure_scanner.checks.unsupported_check import UnsupportedCheck

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


def wmnat(node: DocumentNode, metadata: dict, attributes: set) -> DocumentNode:
    """With metadata and attributes"""
    node = wmt(node, metadata)
    node = wat(node, attributes)
    return node


def wall(node: DocumentNode, metadata: dict, attributes: set, children: list[DocumentNode]) -> DocumentNode:
    """With all - metadata, attributes, children"""
    node = wmt(node, metadata)
    node = wat(node, attributes)
    node = wch(node, children)
    return node


class TestStructureScanner(unittest.TestCase):
    def setUp(self):
        global global_root
        global_root = PurePath("D:\\hlag\\tests\\test_structures_for_structure_scanner")
        self.structure_scanner = StructureScanner(PurePath())

    def test_one_unsupported(self):
        self.structure_scanner.root_directory = PurePath("D:\\hlag\\tests\\test_structures_for_structure_scanner\\one_unsupported")
        self.structure_scanner.register_pre_metaread_node_check(UnsupportedCheck())
        self.structure_scanner.scan()

        expected_tree = DocumentTree(
            wch(DocumentNode(PurePath(prt("one_unsupported"))), [
                wmt(DocumentNode(PurePath(prt("one_unsupported\\unsupported.txt.old"))), {NodeMetadataKey.TYPE: NodeMetadataTypeValue.UNSUPPORTED})
            ])
        )

        self.assertEqual(self.structure_scanner.tree, expected_tree)

    # def test_full(self):
    #     structure_scanner = StructureScanner(PurePath("D:\\hlag\\tests\\test_structures_for_structure_scanner\\full"))
    #     structure_scanner.register_pre_metaread_node_check(UnsupportedScan())
    #     structure_scanner.scan()
    #
    #     expected_tree = DocumentTree(
    #         wall(DocumentNode(PurePath(prt("full"))),
    #              metadata={NodeMetadataKey.TYPE: NodeMetadataTypeValue.UNSUPPORTED},
    #              attributes={NodeAttribute.IN_OUTLINE},
    #              children=[
    #                  wall(DocumentNode(PurePath(prt("full\\_dict.txt"))),
    #                       metadata={NodeMetadataKey.TYPE: NodeMetadataTypeValue.DICTIONARY},
    #                       attributes={NodeAttribute.IS_ESCAPED},
    #                       children=[]),
    #                  wall(DocumentNode(PurePath(prt("full\\_title.txt"))),
    #                       metadata={NodeMetadataKey.TITLE: "Start"},
    #                       attributes={NodeAttribute.IS_ESCAPED},
    #                       children=[]),
    #                  wall(DocumentNode(PurePath(prt("full\\000_header.txt"))),
    #                       metadata={NodeMetadataKey.TYPE: NodeMetadataTypeValue.TEXT},
    #                       attributes={NodeAttribute.IS_ESCAPED},
    #                       children=[]),
    #                  wall(DocumentNode(PurePath(prt("full\\_title.txt"))),
    #                       metadata={NodeMetadataKey.TITLE: "Start"},
    #                       attributes={NodeAttribute.IS_ESCAPED},
    #                       children=[]),
    #                  wall(DocumentNode(PurePath(prt("full\\_title.txt"))),
    #                       metadata={NodeMetadataKey.TITLE: "Start"},
    #                       attributes={NodeAttribute.IS_ESCAPED},
    #                       children=[]),
    #              ])
    #     )


if __name__ == "__main__":
    unittest.main(verbosity=2)
    print()
