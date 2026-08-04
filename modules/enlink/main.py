from pathlib import PurePath
# Own imports
from module_facade import ModuleFacade, DocumentNode
from module_management import IModule


def get_module():
    return Enlink


class Enlink(IModule):
    module_path = PurePath(__file__).parent

    @classmethod
    def get_info(cls) -> dict:
        return {
            "name": "enlink",
            "priority": 1,
            "dependencies": [],
            "jsmanager": "EnlinkModuleManager"
        }

    @classmethod
    def register_checks(cls):
        pass

    @classmethod
    def register_files(cls):
        ModuleFacade.register_js(PurePath(cls.module_path, "js.js"))
        ModuleFacade.register_css(PurePath(cls.module_path, "css.css"))

    @classmethod
    def read_metadata_from_file(cls, node: DocumentNode) -> dict:
        return ModuleFacade.get_module("raw").read_metadata_from_file(node)

    @classmethod
    def read_metadata_from_string(cls, content: str) -> dict:
        return ModuleFacade.get_module("raw").read_metadata_from_string(content)

    @classmethod
    def replace_references(cls, content: str) -> str:
        return ModuleFacade.get_module("raw").replace_references(content)

    @classmethod
    def parse_from_file(cls, node: DocumentNode) -> dict:
        past_meta_location = node.metadata.get("cursor", 0)
        with open(node.path) as f:
            f.seek(past_meta_location)
            return cls.parse_from_string(f.read(), node.metadata)

    @classmethod
    def change_property(cls, last_property: str, item_property: str):
        pass

    @classmethod
    def parse_from_string(cls, content: str, meta: dict) -> dict:
        content = cls.replace_references(content)
        #
        #  Format goes like this:
        #  title: About the topic
        #  link: https://thattopic.com/
        #  desc: Here is some good insight about the topic I like.
        #
        #  title: ...
        #
        #  Empty line is delimiter more such instances are desired.
        #  Parts can be skipped, but must be in order.
        #
        items = []
        item = {"title": "", "link": "", "desc": ""}
        value = ""
        last_property = ""
        item_started = False
        lines = content.splitlines()
        for line in lines:
            if line.startswith("//"):
                continue
            #
            if line.startswith("title: "):
                item_started = True
                parts = line.split(sep=": ")
                last_property = parts[0]
                value = parts[1]
            #
            elif line.startswith("link: "):
                item_started = True
                parts = line.split(sep=": ")
                item[last_property] = value
                last_property = parts[0]
                value = parts[1]
            #
            elif line.startswith("desc: "):
                item_started = True
                parts = line.split(sep=": ")
                item[last_property] = value
                last_property = parts[0]
                value = parts[1]
            #
            elif len(line) == 0 and item_started:
                item_started = False
                item[last_property] = value
                last_property = ""
                value = ""
                items.append(item)
                item = {"title": "", "link": "", "desc": ""}
            elif item_started:
                value = "".join([value, line])
        #
        if item_started:
            item[last_property] = value
            items.append(item)
        #
        result = {
            "module": "enlink",
            "data": {"nodes": items},
            "meta": meta
        }
        return result
