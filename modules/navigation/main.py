from pathlib import PurePath
import json
from importlib import import_module
import os
# Own imports
from module_facade import ModuleFacade, Card, InstanceDBEntry, DocumentNode
from module_management import IModule


def get_module_main_class():
    return PyDocNavigation


class WindowRecord:
    def __init__(self, ref_id: int, title: str, contents: list):
        self.ref_id = ref_id
        self.title = title
        self.contents = contents

    def get_as_js_map_record(self) -> str:
        return f'[{self.ref_id}, new WindowRecord({self.ref_id}, "{self.title}", {json.dumps(self.contents)})]'


class PyDocNavigation(IModule):
    module_path = PurePath(__file__).parent
    navigation_meta_check = import_module(f"navigation.navigation_meta_check")

    nodes_is_outline: list[DocumentNode] = []
    window_map: list[WindowRecord] = []

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

    #
    #   Non-metadata reading methods
    #
    #

    @classmethod
    def fetch_content_from_scanner(cls):
        structure_scanner = ModuleFacade.get_structure_scanner()
        for node in structure_scanner.tree:
            if os.path.isdir(str(node.path)) and not node.has_attribute("escaped"):
                cls.nodes_is_outline.append(node)
                print(f"Navigation - node found in outline: {node.path}")

    @classmethod
    def generate_window_map(cls):
        for i, node in enumerate(cls.nodes_is_outline):
            record_title = node.metadata.get("title") if node.metadata.get("title") else node.path.name
            #
            record_contents = []
            for child_node in node.get_children():
                if child_node.ref:
                    # This dictionary will be translated to JSON by json.dumps() at print method
                    record_contents.append({
                        "module": child_node.ref.module,
                        "id": child_node.ref.ref_id
                    })
            #
            cls.window_map.append(WindowRecord(
                ref_id=i,
                title=record_title,
                contents=record_contents
            ))
            #
        return cls.window_map

    @classmethod
    def print_html(cls):
        yield '    <nav id="nav"></nav>\n'

    @classmethod
    def print_window_map(cls, beginning: str):
        cls.generate_window_map()
        indented_beginning = "".join(["  ", beginning])
        yield f"{beginning}static windowMap = new Map([\n"
        for i, window_record in enumerate(cls.window_map):
            if i < len(cls.window_map) - 1:
                yield f"{indented_beginning}{window_record.get_as_js_map_record()},\n"
            else:
                yield f"{indented_beginning}{window_record.get_as_js_map_record()}\n"
        yield f"{beginning}]);"

    @classmethod
    def print_js(cls):
        with open(PurePath(PurePath(__file__).parent, r"js.js")) as f:
            lines = f.readlines()
            for line in lines:
                if "//PLACEHOLDER_FOR_WINDOWMAP" in line:
                    parts = line.split("//PLACEHOLDER_FOR_WINDOWMAP")
                    yield from cls.print_window_map(parts[0])
                else:
                    yield line

    @classmethod
    def parse_file(cls, card: Card) -> InstanceDBEntry:
        return cls.parse_data(card)

    @classmethod
    def parse_data(cls, card: Card) -> InstanceDBEntry:
        # Content using this data will be printed later.
        # Print is already queued in JSManager, and will trigger cls.print_js(),
        # which in turn refers to that data.
        cls.fetch_content_from_scanner()
        #
        return InstanceDBEntry(
            module=cls.get_info()["name"],
            data="``",
            meta=dict()
        )
