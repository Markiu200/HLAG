import unittest
from pathlib import PurePath
# Own imports
from data.node_type import NodeMetadataKey, NodeMetadataTypeValue
from structure_scanner.metadata_reader.metadata_reader import MetadataReader


class TestMetadataReader(unittest.TestCase):
    def setUp(self):
        self.metadata_reader = MetadataReader()

    def test_single_line(self):
        actual_meta = self.metadata_reader.get_metadata_from_line("[%>title:Simple title]")
        expected_meta = ({
                             NodeMetadataKey.TITLE: "Simple title"
                         }, False)
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for valid meta test.\nActual: {actual_meta}\nExpected: {expected_meta}")

    def test_single_line_multiple_tags(self):
        actual_meta = self.metadata_reader.get_metadata_from_line("[%>title:Simple title][%>meta:Some meta]")
        expected_meta = ({
                             NodeMetadataKey.TITLE: "Simple title",
                             NodeMetadataKey.META: "Some meta"
                         }, False)
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for valid meta test.\nActual: {actual_meta}\nExpected: {expected_meta}")

    def test_single_line_multiple_tags_ended_with_other_text(self):
        actual_meta = self.metadata_reader.get_metadata_from_line("[%>title:Simple title][%>meta:Some meta]break")
        expected_meta = ({
                             NodeMetadataKey.TITLE: "Simple title",
                             NodeMetadataKey.META: "Some meta"
                         }, True)
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for valid meta test.\nActual: {actual_meta}\nExpected: {expected_meta}")

    def test_single_line_multiple_tags_separated(self):
        actual_meta = self.metadata_reader.get_metadata_from_line("[%>title:Simple title]break[%>meta:Some meta]")
        expected_meta = ({
                             NodeMetadataKey.TITLE: "Simple title",
                         }, True)
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for valid meta test.\nActual: {actual_meta}\nExpected: {expected_meta}")

    def test_single_line_multiple_tags_separated_with_space(self):
        actual_meta = self.metadata_reader.get_metadata_from_line("[%>title:Simple title] [%>meta:Some meta]")
        expected_meta = ({
                             NodeMetadataKey.TITLE: "Simple title",
                             NodeMetadataKey.META: "Some meta"
                         }, False)
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for valid meta test.\nActual: {actual_meta}\nExpected: {expected_meta}")

    def test_incorrect_tags(self):
        lines = [
            "title:incomplete tags",
            "[>meta:data]",
            "[%>type:dictionary",
            "%>title:the_title]"
        ]
        actual_data = self.metadata_reader.get_metadata_from_lines(lines)
        expected_data = [
            (dict(), True),
            (dict(), True),
            (dict(), True),
            (dict(), True)
        ]
        self.assertEqual(actual_data, expected_data,
                         f"Metadata different from expected for valid meta test.\nActual: {actual_data}\nExpected: {expected_data}")

    def test_other_line_cases(self):
        actual_data = self.metadata_reader.get_metadata_from_line("[%>title:[%>module]:This_random_case]")
        expected_data = ({
                             NodeMetadataKey.TITLE: "[%>module"
                         }, True)
        self.assertEqual(actual_data, expected_data,
                         f"Metadata different from expected for valid meta test.\nActual: {actual_data}\nExpected: {expected_data}")

    def test_tag_with_spaces(self):
        actual_data = self.metadata_reader.get_metadata_from_lines(
            ("[%> title:Title tag with space]", "[%>title :Title tag with space]"))
        expected_data = [
            (dict(), False),
            (dict(), False)
        ]
        self.assertEqual(actual_data, expected_data,
                         f"Metadata different from expected for valid meta test.\nActual: {actual_data}\nExpected: {expected_data}")

    def test_valid_meta(self):
        actual_meta = self.metadata_reader.get_metadata_from_file(
            PurePath("D:\\hlag\\tests\\test_structure_for_metadata_reader\\meta1.txt"))
        expected_meta = ({
                             NodeMetadataKey.TITLE: "All meta types correctly",
                             NodeMetadataKey.TYPE: NodeMetadataTypeValue.METAFILE,
                             NodeMetadataKey.MODULE: "the_module",
                             NodeMetadataKey.META: "theMeta"
                         }, False)
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for valid meta test.\nActual: {actual_meta}\nExpected: {expected_meta}")

    def test_incorrect_keys(self):
        actual_meta = self.metadata_reader.get_metadata_from_file(
            PurePath("D:\\hlag\\tests\\test_structure_for_metadata_reader\\meta2.txt"))
        # Wrong keys are expected to be ignored (along with values)
        expected_meta = (dict(), False)
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for incorrect keys test.\nActual: {actual_meta}\nExpected: {expected_meta}")

    def test_anything_else_on_new_line(self):
        actual_meta = self.metadata_reader.get_metadata_from_file(
            PurePath("D:\\hlag\\tests\\test_structure_for_metadata_reader\\meta3.txt"))
        expected_meta = ({
                             NodeMetadataKey.TITLE: "Only title but leading new line and some untagged text after that"
                         }, True)
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for incorrect keys test.\nActual: {actual_meta}\nExpected: {expected_meta}")

    def test_anything_else_on_same_line(self):
        actual_meta = self.metadata_reader.get_metadata_from_file(
            PurePath("D:\\hlag\\tests\\test_structure_for_metadata_reader\\meta3a.txt"))
        expected_meta = ({
                             NodeMetadataKey.TITLE: "Only title and some text after tag on the same line"
                         }, True)
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for incorrect keys test.\nActual: {actual_meta}\nExpected: {expected_meta}")

    def test_vaild_tag_and_then_new_line(self):
        actual_meta = self.metadata_reader.get_metadata_from_file(
            PurePath("D:\\hlag\\tests\\test_structure_for_metadata_reader\\meta4.txt"))
        expected_meta = ({
                             NodeMetadataKey.TITLE: "Only title and leading new line"
                         }, False)
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for incorrect keys test.\nActual: {actual_meta}\nExpected: {expected_meta}")

    def test_wrong_type_value(self):
        actual_meta = self.metadata_reader.get_metadata_from_file(
            PurePath("D:\\hlag\\tests\\test_structure_for_metadata_reader\\meta5.txt"))
        expected_meta = ({
                             NodeMetadataKey.TITLE: "Title and type with wrong value"
                         }, False)
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for incorrect keys test.\nActual: {actual_meta}\nExpected: {expected_meta}")

    def test_incorrect_tag_and_then_correct(self):
        actual_meta = self.metadata_reader.get_metadata_from_file(
            PurePath("D:\\hlag\\tests\\test_structure_for_metadata_reader\\meta5.txt"))
        expected_meta = ({
                             NodeMetadataKey.TITLE: "Title and type with wrong value"
                         }, False)
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for incorrect keys test.\nActual: {actual_meta}\nExpected: {expected_meta}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
    print()
