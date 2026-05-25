import os
from pathlib import Path

if __name__ == "__main__":
    from sys import path as syspath

    while "mylib" in os.getcwd():
        os.chdir("..")
    syspath.append(str(Path('lib/').absolute()))
    syspath.append(str(Path('lib/filetypes').absolute()))
from filetypes.meta_file import MetaFile
from filetypes.html_file import HTMLFile
from filetypes.css_file import CSSFile
from filetypes.directory import Directory
from filetypes.png_file import PNGFile
from filetypes.js_file import JSFile


class StructureReader:
    def __init__(self, site_files_folder_path: Path):
        self.site_files_folder_path = site_files_folder_path
        self.root_node: Directory = Directory(self.site_files_folder_path, parent=None)
        self.config_dir: Directory | None = None

    def read(self, directory=None) -> None:
        in_root = False
        if not directory:
            in_root = True
            directory = self.root_node

        for pathstr in os.listdir(directory.path):
            abspath = directory.path / pathstr
            # global folder
            if pathstr.startswith("_global"):
                self.config_dir = Directory(path=abspath, parent=directory)
                self.read(self.config_dir)
                continue
            #
            if os.path.isfile(abspath):
                if pathstr == "meta.txt":
                    if in_root:
                        continue
                    else:
                        directory.children.append(MetaFile(abspath, parent=directory))
                        continue
                _, extension = os.path.splitext(pathstr)
                if extension == ".html":
                    directory.children.append(HTMLFile(abspath, parent=directory))
                if extension == ".css":
                    directory.children.append(CSSFile(abspath, parent=directory))
                if extension == ".png":
                    directory.children.append(PNGFile(abspath, parent=directory))
                if extension == ".js":
                    directory.children.append(JSFile(abspath, parent=directory))
            #
            if os.path.isdir(abspath):
                new_children = Directory(abspath, parent=directory)
                directory.children.append(new_children)
                self.read(new_children)

    def print_structure(self, directory: Directory = None, indent=''):
        node_children = directory.children if directory else self.root_node.children
        new_indent = indent + "--"
        #
        for node in node_children:
            print(indent + str(node.path))
            if isinstance(node, Directory):
                self.print_structure(node, new_indent)


if __name__ == "__main__":
    structure_reader = StructureReader(Path("./webpage").absolute())
    structure_reader.read()
    print("this is config_dir")
    print(structure_reader.config_dir.children)
    print("this is root:")
    print(structure_reader.root_node.children)
