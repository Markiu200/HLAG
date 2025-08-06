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
        page_contents = "<main>\r\n"
        for section in self.dir_structure.all_sections:
            if section.id == "root":
                continue
            page_contents += section.create_section()
        page_contents += "</main>\r\n"
        # generate
        result = \
"""<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Newfluence</title>""" + css.get_file_string() + """
        </head>
    <body>
""" + self.navigation.get_navigation_html_as_string() + """
        <div style="float: left; width: 240px; height: 100%;"></div>""" + page_contents + \
            self.navigation.get_navigation_js_as_string() + """
    </body>
</html>"""
        return result