import unittest
from pathlib import PurePath
# Own imports
from data.node_type import NodeMetadataKey, NodeMetadataTypeValue
from structure_scanner.metadata_reader.metadata_reader import get_metadata


class TestMetadataReader(unittest.TestCase):
    def test_valid_meta(self):
        actual_meta = get_metadata(PurePath("D:\\hlag\\tests\\test_structure_for_metadata_reader\\meta1.txt"))
        expected_meta = ({
            NodeMetadataKey.TITLE: "All meta types correctly",
            NodeMetadataKey.TYPE: NodeMetadataTypeValue.METAFILE,
            NodeMetadataKey.MODULE: "the_module",
            NodeMetadataKey.META: "theMeta"
        }, False)
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for valid meta test.\nActual: {actual_meta}\nExpected: {expected_meta}")

    def test_incorrect_keys(self):
        actual_meta = get_metadata(PurePath("D:\\hlag\\tests\\test_structure_for_metadata_reader\\meta2.txt"))
        # Wrong keys are expected to be ignored (along with values)
        expected_meta = (dict(), False)
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for incorrect keys test.\nActual: {actual_meta}\nExpected: {expected_meta}")

    def test_anything_else_on_new_line(self):
        actual_meta = get_metadata(PurePath("D:\\hlag\\tests\\test_structure_for_metadata_reader\\meta3.txt"))
        expected_meta = ({
            NodeMetadataKey.TITLE: "Only title but leading new line and some untagged text after that"
        }, True)

    def test_anything_else_on_same_line(self):
        actual_meta = get_metadata(PurePath("D:\\hlag\\tests\\test_structure_for_metadata_reader\\meta3a.txt"))
        expected_meta = ({
            NodeMetadataKey.TITLE: "Only title and some text after tag on the same line"
        }, True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
