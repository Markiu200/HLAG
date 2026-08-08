import json
from pathlib import PurePath
# Own imports
from module_facade import ModuleFacade, Card, InstanceDBEntry
from module_management import IModule


def get_module():
    return Enlink


def replace_characters(line: str):
    line = line.replace('"', '\\"')
    line = line.replace("'", "\\'")
    line = line.replace("/", "\\/")
    return line


class Item:
    def __init__(self):
        pass

    def add(self, value: str):
        pass

    def get(self) -> str:
        return ""


class TextItem(Item):
    def __init__(self):
        super().__init__()
        self.result = ""

    def add(self, value: str):
        self.result = "".join([self.result, value])

    def get(self):
        return replace_characters(self.result)


class ImageItem(Item):
    node_full_path = ""

    def __init__(self):
        super().__init__()
        self.images = []

    def add(self, value: str):
        pass
        for image in value.split():
            image_full_path = PurePath(ImageItem.node_full_path, image)
            rel_path = ModuleFacade.get_assets_manager().register_asset(image_full_path)
            self.images.append(json.dumps(rel_path))

    def get(self):
        images_as_json = ", ".join(self.images)
        if len(images_as_json) > 0:
            return "".join(["[", images_as_json, "]"])
        return 'null'


class Record:
    def __init__(self):
        self.title = TextItem()
        self.link = TextItem()
        self.desc = TextItem()
        self.images = ImageItem()
        self.started = False

    def add_part(self, item: str, value: str):
        self.started = True
        if item == "title":
            self.title.add(value)
        if item == "link":
            self.link.add(value)
        if item == "desc":
            self.desc.add(value)
        if item == "images":
            self.images.add(value)

    def get(self):
        record_json = (f'"title": "{self.title.get()}", '
                       f'"link": "{self.link.get()}", '
                       f'"desc": "{self.desc.get()}", '
                       f'"images": {self.images.get()}')
        return "".join(["{", record_json, "}"])


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
        #  images: rel_path rel_path ...
        #
        #  title: ...
        #
        #  Empty line is delimiter more such instances are desired.
        #  Parts can be skipped, but must be in order.
        #
        records = []
        current_record = Record()
        last_property = ""
        ImageItem.node_full_path = card.node.get_parent().path

        lines = content.splitlines()
        for line in lines:
            if line.startswith("//"):
                continue
            #
            if (line.startswith("title: ") or
                    line.startswith("link: ") or
                    line.startswith("desc: ") or
                    line.startswith("images: ")):
                parts = line.split(sep=": ")
                last_property = parts[0]
                current_record.add_part(last_property, parts[1])
            #
            elif len(line) == 0:
                last_property = ""
                if current_record.started:
                    records.append(current_record)
                current_record = Record()
            else:
                current_record.add_part(last_property, line)
        #
        if current_record.started:
            records.append(current_record)
        #
        result_data = ", ".join(['{"nodes": [', *[record.get() for record in records], "]}"])

        result = InstanceDBEntry(
            module=cls.get_info()["name"],
            data=result_data,
            meta=json.dumps(card.meta)
        )
        return result
