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

    def print(self):
        # [link, {"parent": null, "type": type, "link": link, "title": title, "children": [*children], "instances": [*instances]}]
        result = "".join(['["',
                          self.link,
                          '", {"parent": null, "children": ',
                          self.children,
                          ', "type": ',
                          self.nav_type,
                          ', "title": ',
                          self.title,
                          ', "instances": [',
                          self.instances_as_string(),
                          ']}]'])
        return result

    def instances_as_string(self):
        instances_list = []
        for instance in self.instances:
            instances_list.append("".join(['{"module": "', instance.module, '", "instance_id": ', str(instance.ref_id), '}']))
        return ", ".join(instances_list)


# class Leaf(NavItem):
#     def __init__(self, parent, link: str, title: str):
#         super().__init__(parent, link, title)
#
#
# class Branch(NavItem):
#     def __init__(self, parent, link: str, title: str):
#         super().__init__(parent, link, title)
#
#
# class Separator(NavItem):
#     def __init__(self, parent, link: str, title: str):
#         super().__init__(parent, link, title)
#
#
# class Header(NavItem):
#     def __init__(self, parent, link: str, title: str):
#         super().__init__(parent, link, title)


class PyDocNavigation(IModule):
    module_path = PurePath(__file__).parent
    navigation_meta_check = import_module(f"navigation.navigation_meta_check")
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
        nav_root = NavItem(parent=None, nav_type="root", title=title, link=link)
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

            if os.path.isfile(str(node.path)) and node.has_attribute("escaped") and node.metadata.get("nav-separator"):
                # If file and is escaped - Separator item
                title = node.metadata.get("title") if node.metadata.get("title") else node.path.name
                link = ""
                new_item = NavItem(parent=node, nav_type="separator", link=link, title=title)
                nav_item.children.append(new_item)

            if os.path.isfile(str(node.path)) and not node.has_attribute("escaped") and node.metadata.get("nav-header"):
                # If file and is not escaped - Header item. It is supposed to scroll to that position after being clicked
                title = node.metadata.get("title") if node.metadata.get("title") else node.path.name
                link = node.metadata.get("relPath")
                new_item = NavItem(parent=node, nav_type="header", link=link, title=title)
                nav_item.children.append(new_item)

    # @classmethod
    # def generate_window_map(cls):
    #     for i, node in enumerate(cls.nodes_is_outline):
    #         record_title = node.metadata.get("title") if node.metadata.get("title") else node.path.name
    #         #
    #         record_contents = []
    #         for child_node in node.get_children():
    #             if child_node.ref:
    #                 # This dictionary will be translated to JSON by json.dumps() at print method
    #                 record_contents.append({
    #                     "module": child_node.ref.module,
    #                     "id": child_node.ref.ref_id
    #                 })
    #         #
    #         cls.window_map.append(WindowRecord(
    #             ref_id=i,
    #             title=record_title,
    #             contents=record_contents
    #         ))
    #         #
    #     return cls.window_map
    #
    # @classmethod
    # def print_window_map(cls, beginning: str):
    #     cls.generate_window_map()
    #     indented_beginning = "".join(["  ", beginning])
    #     yield f"{beginning}static windowMap = new Map([\n"
    #     for i, window_record in enumerate(cls.window_map):
    #         if i < len(cls.window_map) - 1:
    #             yield f"{indented_beginning}{window_record.get_as_js_map_record()},\n"
    #         else:
    #             yield f"{indented_beginning}{window_record.get_as_js_map_record()}\n"
    #     yield f"{beginning}]);"

    @classmethod
    def print_js(cls):
        # Content using this data will be printed later.
        # Print is already queued in JSManager, and will trigger cls.print_js(),
        # which in turn refers to that data.
        #
        cls.build()
        #
        yield ""
        # with open(PurePath(PurePath(__file__).parent, r"js.js")) as f:
        #     lines = f.readlines()
        #     for line in lines:
        #         if "//PLACEHOLDER_FOR_WINDOWMAP" in line:
        #             parts = line.split("//PLACEHOLDER_FOR_WINDOWMAP")
        #             yield from cls.print_window_map(parts[0])
        #         else:
        #             yield line

