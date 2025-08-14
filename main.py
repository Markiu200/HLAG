import os
if __name__ == "__main__":
    from sys import path as syspath
    from pathlib import Path

    while "mylib" in os.getcwd():
        os.chdir("..")
    syspath.append(str(Path('./mylib/').absolute()))
    syspath.append(str(Path('./mylib/filetypes').absolute()))
from structure_reader import StructureReader
from navigation import Navigation
from main_builder import MainBuilder
from filetypes.directory import Directory
from filetypes.css_file import CSSFile


class SiteBuilder:
    def __init__(self, root_directory_path: Path):
        self.root_directory_path = root_directory_path
        self.structure_reader = StructureReader(self.root_directory_path)
        self.structure_reader.read()
        self.root_directory: Directory = self.structure_reader.root_node
        #
        self.navigation_builder = Navigation(self.root_directory)
        self.main_builder = MainBuilder(self.root_directory)
        self.site_code = ""
        self.indent = ""

    def build(self) -> str:
        # beginning
        self.insert_beginning()
        self.insert_css()
        self.insert_navigation_html()

        return self.site_code

    def insert_beginning(self):
        self.site_code += '''\
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Newfluence</title>
'''
        self.indent = "    "

    def insert_css(self):
        for node in self.root_directory.children:
            if isinstance(node, CSSFile):
                indented_css = ""
                for line in node.get_css().splitlines():
                    indented_css += self.indent + line + "\n"
                self.site_code += indented_css

    def insert_navigation_html(self):
        pass


site_builder = SiteBuilder(Path("./webpage"))

with open("newfluence.html", "w") as file:
    file.write(site_builder.build())
