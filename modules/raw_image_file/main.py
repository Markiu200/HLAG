from pathlib import PurePath
# Own imports
from module_facade import ModuleFacade, DocumentNode
from module_management import IModule
#
from img_check import ImgCheck


def get_module():
    return RawImageFile


class RawImageFile(IModule):
    module_path = PurePath(__file__).parent

    @classmethod
    def get_info(cls) -> dict:
        return {
            "name": "raw_image_file",
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
    def read_metadata_from_file(cls, node: DocumentNode) -> dict:
        return dict()

    @classmethod
    def read_metadata_from_string(cls, content: str) -> dict:
        return dict()

    @classmethod
    def parse_from_file(cls, node: DocumentNode) -> dict:
        return cls.parse_from_string(str(node.path), node.metadata)

    @classmethod
    def parse_from_string(cls, content: str, meta: dict) -> dict:
        items = [ModuleFacade.get_assets_manager().register_asset(PurePath(content))]
        #
        result = {
            "module": cls.get_info()["name"],
            "data": {"nodes": items},
            "meta": meta
        }
        return result
