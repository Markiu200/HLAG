import os
import json
# Own imports
from structure_scanner import StructureScanner, DocumentNode


class NavigationManager:
    nodes_is_outline: list[DocumentNode] = []
    jswindows = []
    last_jswindow_id = 0

    @classmethod
    def fetch_content_from_scanner(cls):
        for node in StructureScanner.tree:
            if os.path.isdir(str(node.path)) and not node.has_attribute("escaped"):
                cls.nodes_is_outline.append(node)
                print(f"Navigation - node found in outline: {node.path}")

    @classmethod
    def generate_jswindows(cls):
        """Here, a flat list of jswindow is generated, meant to be placed flat
        in the final document, outside of any JS class."""
        for node in cls.nodes_is_outline:
            jswindow = {
                "id": cls.last_jswindow_id,
                "title": f"windowid{cls.last_jswindow_id}"
            }
            cls.last_jswindow_id += 1
            #
            if node.metadata.get("title"):
                jswindow["title"] = node.metadata.get("title")
            #
            contents = []
            for child_node in node.get_children():
                if child_node.ref:
                    contents.append({
                        "module": child_node.ref.module,
                        "id": child_node.ref.ref_id
                    })
            jswindow["contents"] = contents
            #
            cls.jswindows.append(jswindow)
        print(json.dumps(cls.jswindows))
        return cls.jswindows

    @classmethod
    def generate_nav_tree(cls):
        """Here is generated tree-like structure of menu items, used by Navigation
        class to present it's menu items in a pretty way."""
        pass

    @classmethod
    def print_html(cls):
        # todo this
        yield '<nav id="nav"></nav>'

    @classmethod
    def print_js_manager(cls):
        # todo this
        yield "class Navigation {}"

    @classmethod
    def print_jswindows(cls):
        res = f"let windows = {cls.generate_jswindows()};"
        yield res

    @classmethod
    def print_js_data(cls):
        # todo this
        yield """let windows = [
      {id: 0, title: "Home", contents: [{module: "text", id: 0}, {module: "text", id: 2}]},
      {id: 1, title: "Data", contents: [{module: "text", id: 1}]},
      {id: 2, title: "Referenced", contents: [{module: "text", id: 3}]},
    ];"""
