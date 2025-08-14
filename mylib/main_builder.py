from filetypes.directory import Directory
from filetypes.html_file import HTMLFile
from article import Article


class MainBuilder:
    def __init__(self, root_directory: Directory):
        self.root_directory = root_directory
        self.main_html = "<main>\n"

    def get_main(self, directory: Directory = None) -> str:
        if directory is None:
            directory = self.root_directory

        self.__get_main_recursive(directory)
        self.main_html += "</main>\n"
        return self.main_html

    def __get_main_recursive(self, directory: Directory):
        if isinstance(directory, Directory):
            for node in directory.children:
                if isinstance(node, Directory):
                    # insert and indent
                    got_article = ""
                    for line in Article(node).get_article().splitlines():
                        got_article += "  " + line + "\n"
                    self.main_html += got_article
                    #
                    if len(node.children) > 0:
                        self.__get_main_recursive(node)
