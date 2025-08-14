from directory import Directory
from article import Article


class MainBuilder:
    def __init__(self, root_directory: Directory):
        self.root_directory = root_directory
        self.main_html = ""

    def get_main(self, directory: Directory = None) -> str:
        if directory is None:
            directory = self.root_directory
        self.main_html = '''\
<main>
'''
        self.__get_main_recursive(directory.children)
        self.main_html += '''\
</main>'''
        return self.main_html

    def __get_main_recursive(self, directory: Directory):
        for node in directory.children:
            if isinstance(node, Directory):
                self.main_html += Article(node).get_article()
                if len(node.children > 0):
                    self.__get_main_recursive(node)
