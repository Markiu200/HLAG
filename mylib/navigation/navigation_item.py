class NavigationItem:
    def __init__(self, title: str, section: list[Section], parent: Section):
        self.title = title
        self.section = section
        self.parent = parent
        self.children = None