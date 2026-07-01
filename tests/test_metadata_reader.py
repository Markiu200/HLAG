import unittest
from pathlib import PurePath
# Own imports
from data.node_type import NodeMetadataKey, NodeMetadataTypeValue
from structure_scanner.metadata_reader.metadata_reader import MetadataReader, ReadResults


class TestMetadataReader(unittest.TestCase):
    def setUp(self):
        MetadataReader.set_tag_regex(r'\[%>(.*?):(.*?)]')

    def test_empty_line(self):
        line = ""
        actual_meta = MetadataReader.get_metadata_from_string(line)
        actual_content = line[actual_meta.cursor:]
        expected_meta = ReadResults(
            metadata=dict(),
            cursor=0
        )
        expected_content = ""

        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for valid meta test.\nActual: {actual_meta}\nExpected: {expected_meta}")
        self.assertEqual(actual_content, expected_content,
                         f"Content different from expected.\nActual: {actual_content}\nExpected: {expected_content}")

    def test_single_line(self):
        line = "[%>title:Simple title]"
        actual_meta = MetadataReader.get_metadata_from_string(line)
        actual_content = line[actual_meta.cursor:]
        expected_meta = ReadResults(
            metadata={NodeMetadataKey.TITLE: "Simple title"},
            cursor=22
        )
        expected_content = ""
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for valid meta test.\nActual: {actual_meta}\nExpected: {expected_meta}")
        self.assertEqual(actual_content, expected_content,
                         f"Content different from expected.\nActual: {actual_content}\nExpected: {expected_content}")

    def test_single_line_multiple_tags(self):
        lines = ["[%>title:Simple title][%>meta:Some meta]"]
        actual_meta = MetadataReader.get_metadata_from_lines(lines)
        actual_content = "".join(lines)[actual_meta.cursor:]
        expected_meta = ReadResults(
            metadata={
                         NodeMetadataKey.TITLE: "Simple title",
                         NodeMetadataKey.META: "Some meta"
                     },
            cursor=40
        )
        expected_content = ""
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for valid meta test.\nActual: {actual_meta}\nExpected: {expected_meta}")
        self.assertEqual(actual_content, expected_content,
                         f"Content different from expected.\nActual: {actual_content}\nExpected: {expected_content}")

    def test_single_line_multiple_tags_ended_with_other_text(self):
        line = "[%>title:Simple title][%>meta:Some meta]break"
        actual_meta = MetadataReader.get_metadata_from_string(line)
        expected_meta = ReadResults(
            metadata={
                         NodeMetadataKey.TITLE: "Simple title",
                         NodeMetadataKey.META: "Some meta"
                     },
            cursor=40
        )
        actual_content = line[actual_meta.cursor:]
        expected_content = "break"
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for valid meta test.\nActual: {actual_meta}\nExpected: {expected_meta}")
        self.assertEqual(actual_content, expected_content,
                         f"Content different from expected.\nActual: {actual_content}\nExpected: {expected_content}")

    def test_single_line_multiple_tags_separated(self):
        line = "[%>title:Simple title]break[%>meta:Some meta]"
        actual_meta = MetadataReader.get_metadata_from_string(line)
        expected_meta = ReadResults(
            metadata={
                         NodeMetadataKey.TITLE: "Simple title",
                     },
            cursor=22
        )
        actual_content = line[actual_meta.cursor:]
        expected_content = "break[%>meta:Some meta]"
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for valid meta test.\nActual: {actual_meta}\nExpected: {expected_meta}")
        self.assertEqual(actual_content, expected_content,
                         f"Content different from expected.\nActual: {actual_content}\nExpected: {expected_content}")

    def test_single_line_multiple_tags_separated_with_space(self):
        line = "[%>title:Simple title] [%>meta:Some meta]"
        actual_meta = MetadataReader.get_metadata_from_string(line)
        expected_meta = ReadResults(
            metadata={
                         NodeMetadataKey.TITLE: "Simple title",
                         NodeMetadataKey.META: "Some meta"
                     },
            cursor=41
        )
        actual_content = line[actual_meta.cursor:]
        expected_content = ""
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for valid meta test.\nActual: {actual_meta}\nExpected: {expected_meta}")
        self.assertEqual(actual_content, expected_content,
                         f"Content different from expected.\nActual: {actual_content}\nExpected: {expected_content}")

    def test_incomplete_tags(self):
        lines = [
            "title:incomplete tags",
            "[>meta:data]",
            "[%>type:dictionary",
            "%>title:the_title]"
        ]
        expected_meta = ReadResults(
            metadata=dict(),
            cursor=0
        )
        for line in lines:
            actual_meta = MetadataReader.get_metadata_from_string(line)
            expected_meta.leftovers = line
            self.assertEqual(actual_meta, expected_meta,
                             f"Metadata different from expected for valid meta test.\nActual: {actual_meta}\nExpected: {expected_meta}")

    def test_other_line_cases(self):
        line = "[%>title:[%>module]:This_random_case]"
        actual_meta = MetadataReader.get_metadata_from_string(line)
        expected_meta = ReadResults(
            metadata={
                         NodeMetadataKey.TITLE: "[%>module"
                     },
            cursor=19
        )
        actual_content = line[actual_meta.cursor:]
        expected_content = ":This_random_case]"
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for valid meta test.\nActual: {actual_meta}\nExpected: {expected_meta}")
        self.assertEqual(actual_content, expected_content,
                         f"Content different from expected.\nActual: {actual_content}\nExpected: {expected_content}")

    def test_tag_with_spaces(self):
        lines = ["[%> title:Title tag with space]", "[%>title :Title tag with space]"]
        expected_meta = ReadResults(
            metadata=dict(),
            cursor=31
        )
        for line in lines:
            actual_meta = MetadataReader.get_metadata_from_string(line)
            self.assertEqual(actual_meta, expected_meta,
                             f"Metadata different from expected for valid meta test.\nActual: {actual_meta}\nExpected: {expected_meta}")

    def test_content_indentation_same_line(self):
        lines = ["[%> title:Test indentation - same line]  Indent of two"]
        actual_meta = MetadataReader.get_metadata_from_lines(lines)
        expected_meta = ReadResults(
            metadata=dict(),
            cursor=39
        )
        actual_content = "".join(lines)[actual_meta.cursor:]
        expected_content = "  Indent of two"
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for valid meta test.\nActual: {actual_meta}\nExpected: {expected_meta}")
        self.assertEqual(actual_content, expected_content,
                         f"Content different from expected.\nActual: {actual_content}\nExpected: {expected_content}")

    def test_content_indentation_next_lines(self):
        lines = ["[%> title:Test indentation - next lines]\r\n",  "  Indent of two\r\n", "  And two even after\r\n", "Then none."]
        actual_meta = MetadataReader.get_metadata_from_lines(lines)
        expected_meta = ReadResults(
            metadata=dict(),
            cursor=42
        )
        actual_content = "".join(lines)[actual_meta.cursor:]
        expected_content = "  Indent of two\r\n  And two even after\r\nThen none."
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for valid meta test.\nActual: {actual_meta}\nExpected: {expected_meta}")
        self.assertEqual(actual_content, expected_content,
                         f"Content different from expected.\nActual: {actual_content}\nExpected: {expected_content}")

    def test_valid_meta(self):
        actual_meta = MetadataReader.get_metadata_from_file(
            PurePath("D:\\hlag\\tests\\test_structure_for_metadata_reader\\meta1.txt"))
        expected_meta = ReadResults(
            metadata={
                         NodeMetadataKey.TITLE: "All meta types correctly",
                         NodeMetadataKey.TYPE: NodeMetadataTypeValue.METAFILE,
                         NodeMetadataKey.MODULE: "the_module",
                         NodeMetadataKey.META: "theMeta"
                     },
            cursor=94
        )
        with open(PurePath("D:\\hlag\\tests\\test_structure_for_metadata_reader\\meta1.txt")) as f:
            f.seek(actual_meta.cursor)
            actual_content = f.read()
        expected_content = ""
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for valid meta test.\nActual: {actual_meta}\nExpected: {expected_meta}")
        self.assertEqual(actual_content, expected_content,
                         f"Content different from expected.\nActual: {actual_content}\nExpected: {expected_content}")

    def test_incorrect_keys(self):
        actual_meta = MetadataReader.get_metadata_from_file(
            PurePath("D:\\hlag\\tests\\test_structure_for_metadata_reader\\meta2.txt"))
        # Wrong keys are expected to be ignored (along with values)
        expected_meta = ReadResults(
            metadata=dict(),
            cursor=72
        )
        with open(PurePath("D:\\hlag\\tests\\test_structure_for_metadata_reader\\meta2.txt")) as f:
            f.seek(actual_meta.cursor)
            actual_content = f.read()
        expected_content = ""
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for incorrect keys test.\nActual: {actual_meta}\nExpected: {expected_meta}")
        self.assertEqual(actual_content, expected_content,
                         f"Content different from expected.\nActual: {actual_content}\nExpected: {expected_content}")

    def test_anything_else_on_new_line(self):
        actual_meta = MetadataReader.get_metadata_from_file(
            PurePath("D:\\hlag\\tests\\test_structure_for_metadata_reader\\meta3.txt"))
        expected_meta = ReadResults(
            metadata={
                         NodeMetadataKey.TITLE: "Only title but leading new line and some untagged text after that"
                     },
            cursor=79
        )
        with open(PurePath("D:\\hlag\\tests\\test_structure_for_metadata_reader\\meta3.txt")) as f:
            f.seek(actual_meta.cursor)
            actual_content = f.read()
        expected_content = "hey"
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for incorrect keys test.\nActual: {actual_meta}\nExpected: {expected_meta}")
        self.assertEqual(actual_content, expected_content,
                         f"Content different from expected.\nActual: {actual_content}\nExpected: {expected_content}")

    def test_anything_else_on_same_line(self):
        actual_meta = MetadataReader.get_metadata_from_file(
            PurePath("D:\\hlag\\tests\\test_structure_for_metadata_reader\\meta3a.txt"))
        expected_meta = ReadResults(
            metadata={
                         NodeMetadataKey.TITLE: "Only title and some text after tag on the same line"
                     },
            cursor=61
        )
        with open(PurePath("D:\\hlag\\tests\\test_structure_for_metadata_reader\\meta3a.txt")) as f:
            f.seek(actual_meta.cursor)
            actual_content = f.read()
        expected_content = "hey"
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for incorrect keys test.\nActual: {actual_meta}\nExpected: {expected_meta}")
        self.assertEqual(actual_content, expected_content,
                         f"Content different from expected.\nActual: {actual_content}\nExpected: {expected_content}")

    def test_tag_after_empty_line(self):
        actual_meta = MetadataReader.get_metadata_from_file(
            PurePath("D:\\hlag\\tests\\test_structure_for_metadata_reader\\meta3b.txt"))
        expected_meta = ReadResults(
            metadata={
                         NodeMetadataKey.TITLE: "Only title tag and type tag after new line"
                     },
            cursor=56
        )
        with open(PurePath("D:\\hlag\\tests\\test_structure_for_metadata_reader\\meta3b.txt")) as f:
            f.seek(actual_meta.cursor)
            actual_content = f.read()
        expected_content = "[%>type:metafile]"
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for incorrect keys test.\nActual: {actual_meta}\nExpected: {expected_meta}")
        self.assertEqual(actual_content, expected_content,
                         f"Content different from expected.\nActual: {actual_content}\nExpected: {expected_content}")

    def test_valid_tag_and_then_new_line(self):
        actual_meta = MetadataReader.get_metadata_from_file(
            PurePath("D:\\hlag\\tests\\test_structure_for_metadata_reader\\meta4.txt"))
        expected_meta = ReadResults(
            metadata={
                NodeMetadataKey.TITLE: "Only title and leading new line"
            },
            cursor=43
        )
        with open(PurePath("D:\\hlag\\tests\\test_structure_for_metadata_reader\\meta4.txt")) as f:
            f.seek(actual_meta.cursor)
            actual_content = f.read()
        expected_content = ""
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for incorrect keys test.\nActual: {actual_meta}\nExpected: {expected_meta}")
        self.assertEqual(actual_content, expected_content,
                         f"Content different from expected.\nActual: {actual_content}\nExpected: {expected_content}")

    def test_wrong_type_value(self):
        actual_meta = MetadataReader.get_metadata_from_file(
            PurePath("D:\\hlag\\tests\\test_structure_for_metadata_reader\\meta5.txt"))
        expected_meta = ReadResults(
            metadata={
                NodeMetadataKey.TITLE: "Title and type with wrong value"
            },
            cursor=58
        )
        with open(PurePath("D:\\hlag\\tests\\test_structure_for_metadata_reader\\meta5.txt")) as f:
            f.seek(actual_meta.cursor)
            actual_content = f.read()
        expected_content = ""
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for incorrect keys test.\nActual: {actual_meta}\nExpected: {expected_meta}")
        self.assertEqual(actual_content, expected_content,
                         f"Content different from expected.\nActual: {actual_content}\nExpected: {expected_content}")

    def test_incorrect_tag_and_then_correct(self):
        actual_meta = MetadataReader.get_metadata_from_file(
            PurePath("D:\\hlag\\tests\\test_structure_for_metadata_reader\\meta5a.txt"))
        expected_meta = ReadResults(
            metadata={
                NodeMetadataKey.TITLE: "Incorrect tag first, then correct one"
            },
            cursor=63
        )
        with open(PurePath("D:\\hlag\\tests\\test_structure_for_metadata_reader\\meta5a.txt")) as f:
            f.seek(actual_meta.cursor)
            actual_content = f.read()
        expected_content = ""
        self.assertEqual(actual_meta, expected_meta,
                         f"Metadata different from expected for incorrect keys test.\nActual: {actual_meta}\nExpected: {expected_meta}")
        self.assertEqual(actual_content, expected_content,
                         f"Content different from expected.\nActual: {actual_content}\nExpected: {expected_content}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
    print()
