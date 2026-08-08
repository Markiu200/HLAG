from pathlib import PurePath
# Own imports
from module_facade import ModuleFacade, Card, InstanceDBEntry
from module_management import IModule


def get_module():
    return Text


class Text(IModule):
    module_path = PurePath(__file__).parent

    @classmethod
    def get_info(cls) -> dict:
        return {
            "name": "text",
            "priority": 1,
            "dependencies": [],
            "controller": "TextModuleController"
        }

    @classmethod
    def register_checks(cls):
        pass

    @classmethod
    def register_files(cls):
        ModuleFacade.register_js(PurePath(cls.module_path, "js.js"))

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
        lines = []
        #
        current_line = ""
        for line in content.splitlines():
            if len(line) > 0:
                current_line = ("" if len(current_line) == 0 else "</br>").join([current_line, line])
            else:
                lines.append(current_line)
                current_line = ""
        lines.append(current_line)
        #
        result = InstanceDBEntry(
            module=cls.get_info()["name"],
            data={"nodes": lines},
            meta=card.meta
        )
        return result
