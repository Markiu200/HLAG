import unittest
from pathlib import PurePath
# Own imports
from data.node_type import NodeMetadataKey, NodeMetadataTypeValue
from structure_scanner.metadata_reader.metadata_reader import get_metadata


class TestMetadataReader(unittest.TestCase):
    def test_valid_meta(self):
        actual_meta = get_metadata(PurePath("D:\\hlag\\tests\\test_structure_for_metadata_reader\\meta1.txt"))
        expected_meta = {
            NodeMetadataKey.TITLE: "All meta types correctly",
            NodeMetadataKey.TYPE: NodeMetadataTypeValue.METAFILE,
            NodeMetadataKey.MODULE: "the_module",
            NodeMetadataKey.META: "theMeta"
        }
        self.assertEqual(actual_meta, expected_meta, f"Metadata different from expected.\nActual: {actual_meta}\nExpected: {expected_meta}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
