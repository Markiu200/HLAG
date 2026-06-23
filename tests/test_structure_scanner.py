import unittest
import sys
from pathlib import PurePath
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


class TestStructureScanner(unittest.TestCase):
    def setUp(self):
        pass
        # # make actual scan
        # self.structure_scanner = StructureScanner(PurePath("D:\\hlag\\tests\\test_structure_for_structure_scanner"))
        # self.structure_scanner.scan()
        # # print(self.structure_scanner)
        #
        # # create reference tree
        # self.reference = DocumentTree(DocumentNode(PurePath("D:\\hlag\\tests\\test_structure_for_structure_scanner")))
        # parent_item = self.reference.root
        # parent_item.set_metadata((NodeMetadataKey.TITLE, "Start"))  # set in _title.txt metafile
        # parent_item.set_metadata((NodeMetadataKey.TYPE, NodeMetadataTypeValue.CONTAINER))  # not in file - needs to be added by scanner
        # parent_item.add_attribute(NodeAttribute.IN_OUTLINE)  # root always in outline
        #
        # new_item_1 = DocumentNode(PurePath("D:\\hlag\\tests\\test_structure_for_structure_scanner\\_dict.txt"))
        # new_item_1.set_metadata((NodeMetadataKey.TYPE, NodeMetadataTypeValue.DICTIONARY))  # set in file
        # new_item_1.add_attribute(NodeAttribute.IS_ESCAPED)  # escape character
        # parent_item.add_child(new_item_1)
        #
        # new_item_2 = DocumentNode(PurePath("D:\\hlag\\tests\\test_structure_for_structure_scanner\\_title.txt"))
        # new_item_2.set_metadata((NodeMetadataKey.TITLE, "Start"))  # set in file
        # new_item_2.set_metadata((NodeMetadataKey.TYPE, NodeMetadataTypeValue.METAFILE))  # not in file - needs to be added by scanner
        # new_item_2.add_attribute(NodeAttribute.IS_ESCAPED)  # escape character
        # parent_item.add_child(new_item_2)
        #
        # new_item_3 = DocumentNode(PurePath("D:\\hlag\\tests\\test_structure_for_structure_scanner\\000_header.txt"))
        # new_item_3.set_metadata((NodeMetadataKey.TYPE, NodeMetadataTypeValue.TEXT))  # not in file - needs to be added by scanner
        # parent_item.add_child(new_item_3)
        #
        # new_item_4 = DocumentNode(PurePath("D:\\hlag\\tests\\test_structure_for_structure_scanner\\010_body.txt"))
        # new_item_4.set_metadata((NodeMetadataKey.TYPE, NodeMetadataTypeValue.TEXT))  # not in file - needs to be added by scanner
        # parent_item.add_child(new_item_4)
        #
        # new_item_5 = DocumentNode(PurePath("D:\\hlag\\tests\\test_structure_for_structure_scanner\\020_image.png"))
        # new_item_5.set_metadata((NodeMetadataKey.TYPE, NodeMetadataTypeValue.IMAGE))  # needs to be added by scanner
        # parent_item.add_child(new_item_5)
        #
        # new_item_6 = DocumentNode(PurePath("D:\\hlag\\tests\\test_structure_for_structure_scanner\\030_footer.txt"))
        # new_item_6.set_metadata((NodeMetadataKey.TYPE, NodeMetadataTypeValue.TEXT))  # not in file - needs to be added by scanner
        # parent_item.add_child(new_item_6)
        #
        # new_item_article = DocumentNode(PurePath("D:\\hlag\\tests\\test_structure_for_structure_scanner\\100_article"))
        # new_item_article.add_attribute(NodeAttribute.IN_OUTLINE)
        # new_item_article.set_metadata((NodeMetadataKey.TITLE, "Article"))   # set in _title.txt metafile
        # new_item_article.set_metadata((NodeMetadataKey.TYPE, NodeMetadataTypeValue.CONTAINER))  # needs to be added by scanner
        # parent_item.add_child(new_item_article)
        #
        # new_item_8 = DocumentNode(PurePath("D:\\hlag\\tests\\test_structure_for_structure_scanner\\100_article\\_title.txt"))
        # new_item_8.set_metadata((NodeMetadataKey.TITLE, "Article"))  # set in file
        # new_item_8.set_metadata((NodeMetadataKey.TYPE, NodeMetadataTypeValue.METAFILE))  # not in file - needs to be added by scanner
        # new_item_article.add_child(new_item_8)
        #
        # new_item_9 = DocumentNode(PurePath("D:\\hlag\\tests\\test_structure_for_structure_scanner\\100_article\\article.txt"))
        # new_item_9.set_metadata((NodeMetadataKey.META, "metadata_for_module"))  # set in file
        # new_item_9.set_metadata((NodeMetadataKey.TYPE, NodeMetadataTypeValue.TEXT))  # not in file - needs to be added by scanner
        # new_item_article.add_child(new_item_8)
        #
        # new_item_escaped = DocumentNode(PurePath("D:\\hlag\\tests\\test_structure_for_structure_scanner\\_110_escaped"))
        # new_item_escaped.add_attribute(NodeAttribute.IS_ESCAPED)
        # new_item_escaped.set_metadata((NodeMetadataKey.TYPE, NodeMetadataTypeValue.CONTAINER))  # needs to be added by scanner
        # parent_item.add_child(new_item_escaped)
        #
        # new_item_10 = DocumentNode(PurePath("D:\\hlag\\tests\\test_structure_for_structure_scanner\\_110_escaped\\article.txt"))
        # new_item_10.add_attribute(NodeAttribute.IS_ESCAPED)  # not in file nor name - needs to be added by scanner (nested in escaped dir)
        # new_item_10.set_metadata((NodeMetadataKey.TYPE, NodeMetadataTypeValue.TEXT))  # not in file - needs to be added by scanner
        # new_item_escaped.add_child(new_item_10)
        #
        # #
        # self.root = self.structure_scanner.tree.get_root()
        # self.escaped = self.structure_scanner.tree.get_node_by_path(
        #     PurePath("D:\\hlag\\tests\\test_structure_for_structure_scanner\\_110_escaped"))
        # self.article = self.structure_scanner.tree.get_node_by_path(
        #     PurePath("D:\\hlag\\tests\\test_structure_for_structure_scanner\\100_article"))

    # def test_for_children_count(self):
    #     self.assertEqual(len(self.root.get_children()), 8)
    #     self.assertEqual(len(self.escaped.get_children()), 1)
    #     self.assertEqual(len(self.article.get_children()), 2)
    #
    # def test_similarity(self):
    #     for node in self.reference:
    #         result_node = self.structure_scanner.tree.get_node_by_path(node.path)
    #         self.assertTrue(result_node, f"Node {node.path} is not accounted for!")
    #         self.assertEqual(node, result_node, f"Node {node.path} does not match the reference node!\nExpected: {str(node)}\nActual: {str(result_node)}")

    def test_one_unsupported(self):
        structure_scanner = StructureScanner(PurePath("D:\\hlag\\tests\\test_structures_for_structure_scanner\\one_unsupported"))
        structure_scanner.register_node_checks(UnsupportedScan())
        structure_scanner.scan()

        checked_node = structure_scanner.tree.get_node_by_path(PurePath("D:\\hlag\\tests\\test_structures_for_structure_scanner\\one_unsupported\\unsupported.txt.old"))

        self.assertEqual(
            checked_node.get_metadata(NodeMetadataKey.TYPE), NodeMetadataTypeValue.UNSUPPORTED
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
    print()
