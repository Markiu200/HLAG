from pathlib import PurePath
# Own imports
from module_facade import ModuleFacade, Card, InstanceDBEntry
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
            "controller": "EnlinkModuleController"
        }

    @classmethod
    def register_checks(cls):
        pass

    @classmethod
    def register_files(cls):
        ModuleFacade.register_js(PurePath(cls.module_path, "js.js"))
        ModuleFacade.register_css(PurePath(cls.module_path, "css.css"))

    @classmethod
    def get_metadata_from_file(cls, card: Card) -> dict:
        return ModuleFacade.get_module("raw").get_metadata_from_file(card)

    @classmethod
    def get_metadata_from_data(cls, card: Card) -> dict:
        return ModuleFacade.get_module("raw").get_metadata_from_string(card)

    @classmethod
    def replace_orders(cls, card: Card) -> str:
        return ModuleFacade.get_module("raw").replace_orders(card)

    @classmethod
    def parse_file(cls, card: Card) -> InstanceDBEntry:
        past_meta_location = card.node.metadata.get("cursor", 0)
        with open(card.node.path) as f:
            f.seek(past_meta_location)
            card.content = f.read()
        card.file = False
        return cls.parse_data(card)

    @classmethod
    def parse_data(cls, card: Card) -> InstanceDBEntry:
        content = cls.replace_orders(card)
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
            meta=json.dumps(card.meta)
        )
        return result
