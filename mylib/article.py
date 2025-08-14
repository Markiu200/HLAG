if __name__ == "__main__":
    from pathlib import Path, PurePath
    from sys import path as syspath
    import os

    while "mylib" in os.getcwd():
        os.chdir("..")
    syspath.append(str(Path('./mylib/').absolute()))
    syspath.append(str(Path('./mylib/filetypes').absolute()))
from filetypes.directory import Directory
from filetypes.meta_file import MetaFile


class Article:
    """Cratfs entire article consisting of one or more HTML files (or no files at all).
    Gives them id for DOM and display title from meta.txt file"""
    def __init__(self, directory: Directory):
        self.directory = directory
        self.title = None
        self.dom_id = None
        self.get_title()
        self.get_dom_id()

    def get_title(self):
        for file in self.directory.children:
            if isinstance(file, MetaFile):
                self.title = file.get_title()
                break

    def get_dom_id(self):
        pure = PurePath(self.directory.path)
        names = pure.parts[3:0]
        self.dom_id = str.join("-", names)

    def get_article(self) -> str:
        result = f"<article id=\"{self.dom_id}\" class='js-article'>"
        for file in self.directory.children:
            if not isinstance(file, Directory):
                result += file.to_string()
        result += "</article>"
        return result


if __name__ == "__main__":
    pure_ = PurePath(Path("D:/hlag/webpage/020_ticket_tracker/010_current_ticket.html"))
    print(pure_.parts)
    names_ = pure_.parts[3:]
    print(names_)
    id_ = str.join(".", names_)
    print(id_)
