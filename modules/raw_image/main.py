from pathlib import PurePath
# Own imports
from module_facade import ModuleFacade, DocumentNode, Data, InstanceDBEntry
from module_management import IModule
#
from img_check import ImgCheck


def get_module():
    return RawImage


class RawImage(IModule):
    module_path = PurePath(__file__).parent

    @classmethod
    def get_info(cls) -> dict:
        return {
            "name": "raw_image",
            "priority": 1,
            "dependencies": [],
            "jsmanager": "RawImageModuleManager"
        }

    @classmethod
    def register_checks(cls):
        ModuleFacade.register_check(ImgCheck())

    @classmethod
    def register_files(cls):
        ModuleFacade.register_js(PurePath(cls.module_path, "js.js"))

    @classmethod
    def get_metadata_from_file(cls, node: DocumentNode) -> dict:
        return dict()

    @classmethod
    def get_metadata_from_data(cls, data: Data) -> dict:
        return dict()

    @classmethod
    def parse_file(cls, node: DocumentNode) -> InstanceDBEntry:
        node.set_metadata("imgSrc", "file")
        return cls.parse_data(Data(str(node.path), node.metadata))

    @classmethod
    def parse_data(cls, data: Data) -> InstanceDBEntry:
        items = []
        if data.meta.get("imgSrc") == "file":
            items.append(ModuleFacade.get_assets_manager().register_asset(PurePath(data.content)))
        else:
            # todo If it is used as order
            pass
        #
        result = InstanceDBEntry(
            module=cls.get_info()["name"],
            data={"nodes": items},
            meta=data.meta
        )
        return result
