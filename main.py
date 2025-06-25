import os
from enum import Enum


class FileType(Enum):
    html = 1
    xml = 2
    css = 3


class WebpageFile:
    def __init__(self, path: str, file_type: FileType):
        self.path = path
        self.file_type = file_type
    
    def create_div(self) -> str:
        if self.file_type == FileType.html:
            return self.__create_div_from_html()
        else:
            raise Exception

    def __create_div_from_html(self) -> str:
        """For HTML files, only return contents of \<body\> as is."""
        result = ""
        save_flag = False
        with open(self.path) as f:
            for line in f:
                if "<body>" in line:
                    save_flag = True
                    continue
                if "</body>" in line:
                    break
                if save_flag:
                    result += line
        result = f"<div>{result}</div>"
        return result


class Section:
    def __init__(self, webpage_files: list[WebpageFile]):
        self.webpage_files = webpage_files


class NavigationItem:
    def __init__(self, title: str, section: list[Section], parent: Section):
        self.title = title
        self.section = section
        self.parent = parent


class WebpageBuilder:
    def __init__(self, webpage_path):
        self.webpage_path = webpage_path
        self.directory_structure = self.get_directory_structure(self.webpage_path)

    def get_directory_structure(self, path: str) -> list:
        local_array = []
        for file in os.listdir(path):
            full_path = os.path.join(path, file)
            if os.path.isfile(full_path):
                local_array.append(full_path)
            else:
                local_array.append(self.get_directory_structure(full_path))
        return local_array

    def create_navigation_structure(self):
        pass


webpage_builder = WebpageBuilder(os.path.join(os.getcwd(), "webpage"))

test_webpage_file = WebpageFile("D:\\Dane_Gits\\HLAG\\webpage\\020_home\\010_home.html", FileType.html)
print(test_webpage_file.create_div())

test_section = Section([
    WebpageFile("D:\\Dane_Gits\\HLAG\\webpage\\020_home\\010_home.html", FileType.html),
    WebpageFile("D:\\Dane_Gits\\HLAG\\webpage\\020_home\\015_some_appendix.html", FileType.html),
])







# https://www.datacamp.com/tutorial/python-get-the-current-directory?dc_referrer=https%3A%2F%2Fwww.google.com%2F
current_location = os.getcwd()
webpage_location = os.path.join(current_location, "webpage")

# for (dirpath, dirnames, filenames) in os.walk(webpage_location):
#     print(dirpath, dirnames, filenames)

# print(webpage_location)
# print(os.path.isfile(os.path.join(webpage_location, "010_start.txt")))

def go_through(path):
    local_array = []
    for file in os.listdir(path):
        full_path = os.path.join(path, file)
        if os.path.isfile(full_path):
            # print(full_path)
            local_array.append(full_path)
        else:
            # print(full_path + " --> ")
            local_array.append(go_through(full_path))
    return local_array

file_array = go_through(webpage_location)
# print(file_array)



class FolderStructure:

    def read_contents(path):
        pass
        # got through all files in this directory
            # if file, add to the list
            # if directory, enter that and do read_contents

"""
na podstawie zagnizdzonej strukturze folderow budowany bedzie navigator
same strony beda wszystkie na tym samym poziomie - ich widocznosc bedzie sterowana z navigatora - tylko pozorne zagniezdzenie

struktura - kazdy folder w webpage_location to pozycja w nawigatorze
pliki w folderach beda zawierac zawartosci tych stron

pliki xml - okreslaja tylko co ma byc na stronie - html, css, javascript generowany w Pythonie
pliki html - tylko <body> bedzie kopiowany (w <body> będzie <script> jesli bedzie taka potrzeba)
css w katalogu glownym - podstrony beda go zaciagac na czas edycji, ale bedzie tylko jeden po utworzeniu strony
pliki w katalogu glownym - beda zawierac globalne definicje - musza byc zaladowane przed pierwszym katalogiem!
strona glowna tez jako katalog - pierwszy w numeracji

mozliwy mix miedzy xml i html - kazdy "kawalek" strony to swoj wlasny div, beda nakladane jeden na drugi w kolejnosci numeracji


"""