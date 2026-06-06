import unittest
from pathlib import PurePath
# Own imports
from data.node_type import NodeMetadataKey, NodeMetadataTypeValue
import structure_scanner.metadata_reader.metadata_reader as mr


class TestMetadataReader(unittest.TestCase):
    def setUp(self):
        self.metadata_reader = mr.MetadataReader()

    def test_empty_line(self):
        actual_meta = self.metadata_reader.get_metadata_from_line("")
        expected_meta = mr.ReadResults(
            metadata=dict(),
            has_leftovers=False,
            leftovers="",
            last_line=-1
        )
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for valid meta test.\nActual: {actual_meta}\nExpected: {expected_meta}")

    def test_single_line(self):
        actual_meta = self.metadata_reader.get_metadata_from_line("[%>title:Simple title]")
        expected_meta = mr.ReadResults(
            metadata={NodeMetadataKey.TITLE: "Simple title"},
            has_leftovers=False,
            leftovers="",
            last_line=0
        )
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for valid meta test.\nActual: {actual_meta}\nExpected: {expected_meta}")

    def test_single_line_multiple_tags(self):
        actual_meta = self.metadata_reader.get_metadata_from_line("[%>title:Simple title][%>meta:Some meta]")
        expected_meta = mr.ReadResults(
            metadata={
                         NodeMetadataKey.TITLE: "Simple title",
                         NodeMetadataKey.META: "Some meta"
                     },
            has_leftovers=False,
            leftovers="",
            last_line=0
        )
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for valid meta test.\nActual: {actual_meta}\nExpected: {expected_meta}")

    def test_single_line_multiple_tags_ended_with_other_text(self):
        actual_meta = self.metadata_reader.get_metadata_from_line("[%>title:Simple title][%>meta:Some meta]break")
        expected_meta = mr.ReadResults(
            metadata={
                         NodeMetadataKey.TITLE: "Simple title",
                         NodeMetadataKey.META: "Some meta"
                     },
            has_leftovers=True,
            leftovers="break",
            last_line=1
        )
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for valid meta test.\nActual: {actual_meta}\nExpected: {expected_meta}")

    def test_single_line_multiple_tags_separated(self):
        actual_meta = self.metadata_reader.get_metadata_from_line("[%>title:Simple title]break[%>meta:Some meta]")
        expected_meta = mr.ReadResults(
            metadata={
                         NodeMetadataKey.TITLE: "Simple title",
                     },
            has_leftovers=True,
            leftovers="break[%>meta:Some meta]",
            last_line=1
        )
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for valid meta test.\nActual: {actual_meta}\nExpected: {expected_meta}")

    def test_single_line_multiple_tags_separated_with_space(self):
        actual_meta = self.metadata_reader.get_metadata_from_line("[%>title:Simple title] [%>meta:Some meta]")
        expected_meta = mr.ReadResults(
            metadata={
                         NodeMetadataKey.TITLE: "Simple title",
                         NodeMetadataKey.META: "Some meta"
                     },
            has_leftovers=False,
            leftovers="",
            last_line=0
        )
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for valid meta test.\nActual: {actual_meta}\nExpected: {expected_meta}")

    def test_incorrect_tags(self):
        lines = [
            "title:incomplete tags",
            "[>meta:data]",
            "[%>type:dictionary",
            "%>title:the_title]"
        ]
        expected_meta = mr.ReadResults(
            metadata=dict(),
            has_leftovers=True,
            leftovers="",
            last_line=1
        )
        for line in lines:
            actual_meta = self.metadata_reader.get_metadata_from_line(line)
            expected_meta.leftovers = line
            self.assertEqual(actual_meta, expected_meta,
                             f"Metadata different from expected for valid meta test.\nActual: {actual_meta}\nExpected: {expected_meta}")

    def test_other_line_cases(self):
        actual_meta = self.metadata_reader.get_metadata_from_line("[%>title:[%>module]:This_random_case]")
        expected_meta = mr.ReadResults(
            metadata={
                         NodeMetadataKey.TITLE: "[%>module"
                     },
            has_leftovers=True,
            leftovers=":This_random_case]",
            last_line=1
        )
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for valid meta test.\nActual: {actual_meta}\nExpected: {expected_meta}")

    def test_tag_with_spaces(self):
        lines = ["[%> title:Title tag with space]", "[%>title :Title tag with space]"]
        expected_meta = mr.ReadResults(
            metadata=dict(),
            has_leftovers=False,
            leftovers="",
            last_line=0
        )
        for line in lines:
            actual_meta = self  .metadata_reader.get_metadata_from_line(line)
            self.assertEqual(actual_meta, expected_meta,
                             f"Metadata different from expected for valid meta test.\nActual: {actual_meta}\nExpected: {expected_meta}")

    def test_valid_meta(self):
        actual_meta = self.metadata_reader.get_metadata_from_file(
            PurePath("D:\\hlag\\tests\\test_structure_for_metadata_reader\\meta1.txt"))
        expected_meta = mr.ReadResults(
            metadata={
                         NodeMetadataKey.TITLE: "All meta types correctly",
                         NodeMetadataKey.TYPE: NodeMetadataTypeValue.METAFILE,
                         NodeMetadataKey.MODULE: "the_module",
                         NodeMetadataKey.META: "theMeta"
                     },
            has_leftovers=False,
            leftovers="",
            last_line=4
        )
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for valid meta test.\nActual: {actual_meta}\nExpected: {expected_meta}")

    def test_incorrect_keys(self):
        actual_meta = self.metadata_reader.get_metadata_from_file(
            PurePath("D:\\hlag\\tests\\test_structure_for_metadata_reader\\meta2.txt"))
        # Wrong keys are expected to be ignored (along with values)
        expected_meta = mr.ReadResults(
            metadata=dict(),
            has_leftovers=False,
            leftovers="",
            last_line=4
        )
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for incorrect keys test.\nActual: {actual_meta}\nExpected: {expected_meta}")

    def test_anything_else_on_new_line(self):
        actual_meta = self.metadata_reader.get_metadata_from_file(
            PurePath("D:\\hlag\\tests\\test_structure_for_metadata_reader\\meta3.txt"))
        expected_meta = mr.ReadResults(
            metadata={
                         NodeMetadataKey.TITLE: "Only title but leading new line and some untagged text after that"
                     },
            has_leftovers=False,
            leftovers="",
            last_line=1
        )
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for incorrect keys test.\nActual: {actual_meta}\nExpected: {expected_meta}")

    def test_anything_else_on_same_line(self):
        actual_meta = self.metadata_reader.get_metadata_from_file(
            PurePath("D:\\hlag\\tests\\test_structure_for_metadata_reader\\meta3a.txt"))
        expected_meta = mr.ReadResults(
            metadata={
                         NodeMetadataKey.TITLE: "Only title and some text after tag on the same line"
                     },
            has_leftovers=True,
            leftovers="hey",
            last_line=1
        )
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for incorrect keys test.\nActual: {actual_meta}\nExpected: {expected_meta}")

    def test_tag_after_empty_line(self):
        actual_meta = self.metadata_reader.get_metadata_from_file(
            PurePath("D:\\hlag\\tests\\test_structure_for_metadata_reader\\meta3b.txt"))
        expected_meta = mr.ReadResults(
            metadata={
                         NodeMetadataKey.TITLE: "Only title tag and type tag after new line"
                     },
            has_leftovers=False,
            leftovers="",
            last_line=1
        )
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for incorrect keys test.\nActual: {actual_meta}\nExpected: {expected_meta}")

    def test_valid_tag_and_then_new_line(self):
        actual_meta = self.metadata_reader.get_metadata_from_file(
            PurePath("D:\\hlag\\tests\\test_structure_for_metadata_reader\\meta4.txt"))
        expected_meta = mr.ReadResults(
            metadata={
                NodeMetadataKey.TITLE: "Only title and leading new line"
            },
            has_leftovers=False,
            leftovers="",
            last_line=1
        )
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for incorrect keys test.\nActual: {actual_meta}\nExpected: {expected_meta}")

    def test_wrong_type_value(self):
        actual_meta = self.metadata_reader.get_metadata_from_file(
            PurePath("D:\\hlag\\tests\\test_structure_for_metadata_reader\\meta5.txt"))
        expected_meta = mr.ReadResults(
            metadata={
                NodeMetadataKey.TITLE: "Title and type with wrong value"
            },
            has_leftovers=False,
            leftovers="",
            last_line=2
        )
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for incorrect keys test.\nActual: {actual_meta}\nExpected: {expected_meta}")

    def test_incorrect_tag_and_then_correct(self):
        actual_meta = self.metadata_reader.get_metadata_from_file(
            PurePath("D:\\hlag\\tests\\test_structure_for_metadata_reader\\meta5a.txt"))
        expected_meta = mr.ReadResults(
            metadata={
                NodeMetadataKey.TITLE: "Incorrect tag first, then correct one"
            },
            has_leftovers=False,
            leftovers="",
            last_line=2
        )
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for incorrect keys test.\nActual: {actual_meta}\nExpected: {expected_meta}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
    print()
