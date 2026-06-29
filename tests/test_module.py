import unittest
# Own imports
from printer.string_printer import StringPrinter


class TestMetadataReader(unittest.TestCase):
    def setUp(self):
        self.printer = StringPrinter()

    def test_simple_file(self):
        expected = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
        file = r"D:\hlag\tests\test_module\text1.txt"


if __name__ == "__main__":
    unittest.main(verbosity=2)
    print()
