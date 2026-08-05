from pathlib import PurePath
# Own imports
from module_facade import ModuleFacade, DocumentNode, Data, InstanceDBEntry
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
    def get_metadata_from_file(cls, node: DocumentNode) -> dict:
        return ModuleFacade.get_module("raw").get_metadata_from_file(node)

    @classmethod
    def get_metadata_from_data(cls, data: Data) -> dict:
        return ModuleFacade.get_module("raw").get_metadata_from_string(data)

    @classmethod
    def replace_orders(cls, data: Data) -> str:
        return ModuleFacade.get_module("raw").replace_orders(data)

    @classmethod
    def parse_file(cls, node: DocumentNode) -> InstanceDBEntry:
        past_meta_location = node.metadata.get("cursor", 0)
        with open(node.path) as f:
            f.seek(past_meta_location)
            content = f.read()
        return cls.parse_data(Data(content=content, meta=node.metadata))

    @classmethod
    def parse_data(cls, data: Data) -> InstanceDBEntry:
        content = cls.replace_orders(data)
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
        result = InstanceDBEntry(
            module=cls.get_info()["name"],
            data={"nodes": items},
            meta=data.meta
        )
        return result
