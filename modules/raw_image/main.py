from pathlib import PurePath
from importlib import import_module
# Own imports
from lib.module_facade import ModuleFacade, Card, InstanceDBEntry
from lib.module_management import IModule, ModuleManager
from lib.n_config import Config
from lib.registerables import FileRegisterable


def register(module_manager: ModuleManager):
    return RawImage(module_manager)


class RawImage(IModule):
    def __init__(self, module_manager: ModuleManager):
        super().__init__()
        self.module_path = PurePath(__file__).parent
        self.info = {
            "codename": "raw_image",
            "priority": 1,
            "controller": "RawModuleController"
        }
        self.module_manager = module_manager
        self.config: Config = module_manager.config
        # Checks
        # ModuleFacade.register_check(cls.img_check.ImgCheck())
        self.img_check = import_module(f"raw_image.img_check")
        self.checks = [self.img_check]
        # JS
        self.js = [FileRegisterable(PurePath(self.module_path, "js.js"))]
        # Register config items
        self.config_ns = module_manager.config.register_namespace(self.info.get("codename"))
        self.config_ns.set("base64", False)
        # GUI
        self.config_ns.set_widget(import_module(f"raw_image.gui_widget").ConfigWidget)

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
