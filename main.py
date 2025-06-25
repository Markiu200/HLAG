import os
from enum import Enum


class WebpageFile:
    def __init__(self, path: str, file_type: str):
        self.path = path
        self.file_type = file_type
    
    def get_file_string(self) -> str:
        if self.file_type == ".html":
            return self.__create_div_from_html()
        if self.file_type == ".css":
            return self.__create_style_from_css()
        raise Exception

    def __create_div_from_html(self) -> str:
        """For HTML files, only return contents of &lt;body&gt; as is."""
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
    
    def __create_style_from_css(self) -> str:
        """For CSS files, return whole file but encase it in &lt;style&gt; tags"""
        result = "<style>\r\n"
        with open(self.path) as f:
            for line in f:
                result += line
        result += "</style>\r\n"
        return result


class Section:
    def __init__(self, webpage_files: list[WebpageFile], id: str):
        self.webpage_files = webpage_files
        self.id = id
        self.parent = None
        self.children = None
    
    def create_section(self) -> str:
        result = f"<section id=\"{self.id}\">"
        for file in self.webpage_files:
            result += file.get_file_string()
        result += "</section>"
        return result


class Page:
    def __init__(self, sections: list[Section], css: str, navigation: str):
        self.css = css
        self.sections = sections
        self.navigation = navigation

    def create_page(self):
        all_sections = ""
        for section in self.sections:
            all_sections += section.create_section()
        return """<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Newfluence</title>""" + self.css + """
        </head>
    <body>""" + self.navigation + all_sections + """</body>
</html>"""


class NavigationItem:
    def __init__(self, title: str, section: list[Section], parent: Section):
        self.title = title
        self.section = section
        self.parent = parent
        self.children = None


class Navigation:
    def __init__(self, section_list: list[Section]):
        self.section_list = section_list
    
    def get_navigation_html_as_string(self) -> str:
        result = "<nav>"
        for section in self.section_list:
            result += f"<button>${section.id}</button>"
        return result


class FileStructureReader:
    def __init__(self, webpage_path):
        self.webpage_path = webpage_path
        self.all_sections: list[Section] = []
        self.root_section = Section([], "root")
        self.__get_root_files_and_sections(self.webpage_path, self.root_section)

    def __get_root_files_and_sections(self, path: str, section: Section, parent: Section = None) -> Section:
        section.parent = parent
        for file in os.listdir(path):
            full_path = os.path.join(path, file)
            if os.path.isfile(full_path):
                _, ext = os.path.splitext(full_path)
                section.webpage_files.append(WebpageFile(full_path, ext))
            else:
                section.children = self.__get_root_files_and_sections(full_path, Section([], file), section)
        self.all_sections.append(section)


class PageBuilder:
    def __init__(self, navigation: Navigation, dir_structure: FileStructureReader):
        self.navigation = navigation
        self.dir_structure = dir_structure

    def build(self):
        # get root files - css
        css = None
        for file in self.dir_structure.root_section.webpage_files:
            if file.file_type == ".css":
                css = file
        # get page contents
        page_contents = ""
        for sections in self.dir_structure.all_sections:
            if sections.id == "root":
                continue
            for file in sections.webpage_files:
                page_contents += file.get_file_string()
        # generate
        result = """<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Newfluence</title>""" + css.get_file_string() + """
        </head>
    <body>""" + page_contents + """</body>
</html>"""
        return result
        


structure_reader = FileStructureReader(os.path.join(os.getcwd(), "webpage"))
navigation = Navigation(structure_reader.all_sections)
page_builder = PageBuilder(navigation, structure_reader)

#print(navigation.get_navigation_html_as_string())
print(page_builder.build())
with open("newfluence.html", "w") as file:
    file.write(page_builder.build())





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

PageBuilder bylby tworzyl calosc strony - przyjmowalby Navigator i PageContents, oraz zawartosc katalogu root.
Tworzylby wtedy cala otoczke HTML, i head, wklejalby CSS w head

PageContents w zasadzie tylko udostepni wszystkie sekcje jako tekst

Navigator udostepni nawigacje jako tekst, ale JS musialby byc osobno zeby moc go dodac na sam dol strony (tak zeby cala strona 
wraz z sekcjami juz byla zaladowana, zeby getElementById zalapywal wszystko)

W tej sytuacji FileStructureReader musialby:
 * udostepniac pliki tylko w root
 * udostepniac cale sekcje jako sekcje
 * jakos zbierac informacje o tym jak sekcje sa zagniezdzone zeby odzwierciedlac to w nawigacji

Wiec co do zbierania - algorytm moglby akceptowac jakis Section - root bylby specjalnym Section na ta okazje. 
Sekcje beda zapisywane na liste sekcji, ale wraz z utworzeniem kazdej z nich, pole parent w sekcji bedzie zaludniane parentem wlasnie

Osobna metoda moglaby przejsc liste sekcji i zczytywac jaki jest parent - to odroznie pliki z roota od faktycznych sekcji

Pole children dla sekcji? Tak jest



"""