from pathlib import PurePath
# Own imports
from module_facade import ModuleFacade, Card, InstanceDBEntry
from module_management import IModule
#
from img_check import ImgCheck


def get_module_main_class():
    return RawImage


class RawImage(IModule):
    module_path = PurePath(__file__).parent

    @classmethod
    def get_info(cls) -> dict:
        return {
            "name": "raw_image",
            "priority": 1,
            "dependencies": [],
            "controller": "RawImageModuleController"
        }

    @classmethod
    def register_checks(cls):
        ModuleFacade.register_check(ImgCheck())

    @classmethod
    def register_files(cls):
        ModuleFacade.register_js(PurePath(cls.module_path, "js.js"))

    @classmethod
    def get_metadata_from_file(cls, card: Card) -> dict:
        return dict()

    @classmethod
    def get_metadata_from_data(cls, card: Card) -> dict:
        return dict()

    @classmethod
    def parse_file(cls, card: Card) -> InstanceDBEntry:
        card.node.set_metadata("imgSrc", "file")
        card.file = False
        return cls.parse_data(card)

    @classmethod
    def parse_data(cls, card: Card) -> InstanceDBEntry:
        items = []
        if card.meta.get("imgSrc") == "file":
            items.append(ModuleFacade.get_assets_manager().register_asset(card.node.path))
        else:
            line = card.content.strip()
            image_full_path = PurePath(card.node.get_parent().path, line)
            rel_path = ModuleFacade.get_assets_manager().register_asset(image_full_path)
            items.append(rel_path)
        #
        result = InstanceDBEntry(
            module=cls.get_info()["name"],
            data={"nodes": items},
            meta=card.meta
        )
        return result
