from pathlib import Path, PurePath
if __name__ == "__main__":
    from sys import path as syspath
    import os

    while "mylib" in os.getcwd():
        os.chdir("..")
    syspath.append(str(Path('./mylib/').absolute()))
    syspath.append(str(Path('./mylib/filetypes').absolute()))
from filetypes.directory import Directory
from filetypes.meta_file import MetaFile
from filetypes.html_file import HTMLFile


class Article:
    """Cratfs entire article consisting of one or more HTML files (or no files at all).
    Gives them id for DOM and display title from meta.txt file"""
    def __init__(self, directory: Directory, images_to_base64: bool = True):
        self.directory = directory
        self.title = None
        self.dom_id = None
        self.get_title()
        self.get_dom_id()
        self.images_to_base64 = images_to_base64

    def get_title(self):
        for file in self.directory.children:
            if isinstance(file, MetaFile):
                self.title = file.get_title()
                break

    def get_dom_id(self):
        pure = PurePath(self.directory.path)
        parts = pure.parts
        index = parts.index('webpage') + 1
        names = parts[index:]
        self.dom_id = str.join("-", names)

    def get_article(self) -> str:
        result = f"<article id=\"{self.dom_id}\" class='js-article'>\n"
        for file in self.directory.children:
            if isinstance(file, HTMLFile):
                if self.images_to_base64:
                    result += file.to_string()
                else:
                    file.images_to_base64 = False
                    result += file.to_string()
        result += "</article>\n"
        return result


if __name__ == "__main__":
    pure_ = PurePath(Path("D:/hlag/webpage/020_ticket_tracker/010_current_ticket.html"))
    print(pure_.parts)
    names_ = pure_.parts[3:]
    print(names_)
    id_ = str.join(".", names_)
    print(id_)
