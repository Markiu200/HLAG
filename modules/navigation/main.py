from pathlib import PurePath
from importlib import import_module
import os
# Own imports
from module_facade import ModuleFacade, Card, InstanceDBEntry, Ref
from module_management import IModule


def get_module_main_class():
    return PyDocNavigation


class NavItem:
    def __init__(self, parent, nav_type: str, link: str, title: str):
        self.parent = parent
        self.nav_type = nav_type
        self.link = link
        self.title = title
        self.children: list['NavItem'] = []
        self.instances: list[Ref] = []

    @classmethod
    def copy(cls, other: 'NavItem'):
        new_nav_item = NavItem(
            parent=other.parent,
            nav_type=other.nav_type,
            link=other.link,
            title=other.title,
        )
        new_nav_item.children = list(other.children)
        new_nav_item.instances = list(other.instances)
        return new_nav_item

    def as_string(self):
        # [link, {"hostDir": hostDir, "children": [*children], "type": type, "title": title, "instances": [*instances]}]
        result = "".join(['["',
                          self.link,
                          '", {"hostDir": `', self.parent.metadata.get("hostPath"), '`, "children": [',
                          self.children_as_string(),
                          '], "type": `',
                          self.nav_type,
                          '`, "title": `',
                          self.title,
                          '`, "instances": [',
                          self.instances_as_string(),
                          ']}]'])
        return result

    def children_as_string(self) -> str:
        children_string_list = []
        for child in self.children:
            children_string_list.append(child.as_string())
        return ", ".join(children_string_list)

    def instances_as_string(self) -> str:
        instances_list = []
        for instance in self.instances:
            instances_list.append("".join(['{"module": "', instance.module, '", "id": ', str(instance.ref_id), '}']))
        return ", ".join(instances_list)


class PyDocNavigation(IModule):
    module_path = PurePath(__file__).parent
    navigation_meta_check = import_module(f"navigation.navigation_meta_check")
    nav_separator_check = import_module(f"navigation.nav_separator_check")
    nav_tree: NavItem = None

    @classmethod
    def get_info(cls) -> dict:
        return {
            "name": "py_doc_navigation",
            "priority": 15,
            "dependencies": None,
            "controller": "null"
        }

    @classmethod
    def register_checks(cls):
        ModuleFacade.register_final_dir_check(cls.navigation_meta_check.NavigationMetaCheck())
        ModuleFacade.register_final_dir_check(cls.nav_separator_check.NavSeparatorCheck())

    @classmethod
    def register_files(cls):
        ModuleFacade.get_js_manager().register_print_delayed(cls.print_js())
        ModuleFacade.register_css(PurePath(cls.module_path, "style.css"))

    @classmethod
    def get_metadata_from_file(cls, card: Card) -> dict:
        return dict()

    @classmethod
    def get_metadata_from_data(cls, card: Card) -> dict:
        return dict()

    @classmethod
    def parse_file(cls, card: Card) -> InstanceDBEntry:
        return cls.parse_data(card)

    @classmethod
    def parse_data(cls, card: Card) -> InstanceDBEntry:
        return InstanceDBEntry(
            module=cls.get_info()["name"],
            data="``",
            meta=dict()
        )

    #
    #   Logics
    #

    @classmethod
    def build(cls):
        structure_scanner = ModuleFacade.get_structure_scanner()
        # Create root element
        root = structure_scanner.tree.root
        title = root.metadata.get("title") if root.metadata.get("title") else root.path.name
        link = root.metadata.get("relPath")
        nav_root = NavItem(parent=root, nav_type="root", title=title, link=link)
        cls.collect_refs(root, nav_root)
        cls.nav_tree = nav_root
        # Scan
        cls._scan(root, cls.nav_tree)

    @classmethod
    def is_branching(cls, node) -> bool:
        for child in node.get_children():
            if os.path.isdir(str(child.path)):
                return True
        return False

    @classmethod
    def collect_refs(cls, node, nav_item: NavItem):
        for child in node.get_children():
            if not child.has_attribute("escaped") and child.ref and os.path.isfile(child.path):
                nav_item.instances.append(child.ref)

    @classmethod
    def _scan(cls, parent, nav_item):
        for node in parent.children:
            if os.path.isdir(str(node.path)) and not node.has_attribute("escaped"):

                if cls.is_branching(node):  # If directory and has children directories - Branch item
                    title = node.metadata.get("title") if node.metadata.get("title") else node.path.name
                    link = node.metadata.get("relPath")
                    new_item = NavItem(parent=node, nav_type="branch", link=link, title=title)
                    nav_item.children.append(new_item)
                    cls.collect_refs(node, new_item)
                    cls._scan(node, new_item)

                else:  # If directory and has no children - Leaf item
                    title = node.metadata.get("title") if node.metadata.get("title") else node.path.name
                    link = node.metadata.get("relPath")
                    new_item = NavItem(parent=node, nav_type="leaf", link=link, title=title)
                    nav_item.children.append(new_item)
                    cls.collect_refs(node, new_item)

            if os.path.isdir(str(node.path)) and node.has_attribute("escaped") and node.metadata.get("nav-separator"):
                # If file and is escaped - Separator item
                title = node.metadata.get("nav-separator") if node.metadata.get("nav-separator") else node.path.name
                link = node.metadata.get("relPath")
                new_item = NavItem(parent=node, nav_type="separator", link=link, title=title)
                nav_item.children.append(new_item)

            if os.path.isfile(str(node.path)) and not node.has_attribute("escaped") and node.metadata.get("nav-header"):
                # If file and is not escaped - Header item. It is supposed to scroll to that position after being clicked
                title = node.metadata.get("title") if node.metadata.get("title") else node.path.name
                link = node.metadata.get("relPath")
                new_item = NavItem(parent=node, nav_type="header", link=link, title=title)
                nav_item.children.append(new_item)

    @classmethod
    def separate_home(cls) -> list[NavItem]:
        home = NavItem.copy(cls.nav_tree)
        rest = home.children
        home.children = []
        outline = [home, *rest]
        return outline

    @classmethod
    def as_js_map(cls):
        outline_as_string = ", ".join((item.as_string() for item in cls.separate_home()))
        return "".join(['static menuMap = new Map([', outline_as_string, ']);\n'])

    @classmethod
    def print_js(cls):
        # Content using this data will be printed later.
        # Print is already queued in JSManager, and will trigger cls.print_js(),
        # which in turn refers to that data.
        #
        cls.build()
        #
        with open(PurePath(PurePath(__file__).parent, r"js.js")) as f:
            lines = f.readlines()
            for line in lines:
                if "//PLACEHOLDER_FOR_MENUMAP" in line:
                    parts = line.split("//PLACEHOLDER_FOR_MENUMAP")
                    yield "".join([parts[0], cls.as_js_map()])
                else:
                    yield line
