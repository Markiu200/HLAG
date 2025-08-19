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
    def __init__(self, root_directory_path: Path, images_to_base64: bool = True):
        self.root_directory_path = root_directory_path
        self.structure_reader = StructureReader(self.root_directory_path)
        self.structure_reader.read()
        self.root_directory: Directory = self.structure_reader.root_node
        #
        self.navigation_builder = Navigation(self.root_directory)
        self.images_to_base64 = images_to_base64
        self.main_builder = MainBuilder(self.root_directory, images_to_base64=True)
        self.site_code = ""
        self.indent = ""

    def build(self) -> str:
        self.insert_beginning()
        self.insert_css()
        self.insert_transition_to_body()
        self.insert_navigation_html()
        self.insert_nav_space_allocator()
        self.insert_main()
        self.insert_navigation_js()
        self.insert_ending()

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

    def insert_transition_to_body(self):
        self.site_code += f"  </head>\n  <body>\n"

    def insert_navigation_html(self):
        indented_html = ""
        for line in self.navigation_builder.get_html(self.root_directory).splitlines():
            indented_html += self.indent + line + "\n"
        self.site_code += indented_html

    def insert_nav_space_allocator(self):
        self.site_code += f"{self.indent}<div style=\"float: left; width: 240px; height: 100%;\"></div>\n"

    def insert_main(self):
        indented_main = ""
        for line in self.main_builder.get_main(self.root_directory).splitlines():
            indented_main += self.indent + line + "\n"
        self.site_code += indented_main

    def insert_navigation_js(self):
        indented_js = ""
        for line in self.navigation_builder.get_js(self.root_directory).splitlines():
            indented_js += self.indent + line + "\n"
        self.site_code += indented_js

    def insert_ending(self):
        self.site_code += "  </body>\n</html>"
        self.indent = ""


site_builder = SiteBuilder(Path("./webpage"), images_to_base64=True)

with open("newfluence.html", "w") as file:
    file.write(site_builder.build())
