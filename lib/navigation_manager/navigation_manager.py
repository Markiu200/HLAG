import os
import json
from pathlib import PurePath
# Own imports
from structure_scanner import StructureScanner, DocumentNode


class WindowRecord:
    def __init__(self, ref_id: int, title: str, contents: list):
        self.ref_id = ref_id
        self.title = title
        self.contents = contents

    def get_as_js_map_record(self) -> str:
        return f'[{self.ref_id}, new WindowRecord({self.ref_id}, "{self.title}", {json.dumps(self.contents)})]'


class NavigationManager:
    nodes_is_outline: list[DocumentNode] = []
    window_map: list[WindowRecord] = []

    @classmethod
    def fetch_content_from_scanner(cls):
        for node in StructureScanner.tree:
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
        with open(PurePath(PurePath(__file__).parent, r"navigation.js")) as f:
            lines = f.readlines()
            for line in lines:
                if "//PLACEHOLDER_FOR_WINDOWMAP" in line:
                    parts = line.split("//PLACEHOLDER_FOR_WINDOWMAP")
                    yield from cls.print_window_map(parts[0])
                else:
                    yield line
