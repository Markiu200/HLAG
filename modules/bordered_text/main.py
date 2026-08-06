from pathlib import PurePath
# Own imports
from module_facade import ModuleFacade, DocumentNode, Data, InstanceDBEntry
from module_management import IModule


def get_module():
    return BorderedText


class BorderedText(IModule):
    module_path = PurePath(__file__).parent

    @classmethod
    def get_info(cls) -> dict:
        return {
            "name": "bordered_text",
            "priority": -1,
            "dependencies": ["text"],
            "controller": "BorderedTextModuleController"
        }

    @classmethod
    def register_checks(cls):
        pass

    @classmethod
    def register_files(cls):
        ModuleFacade.register_js(PurePath(cls.module_path, "js.js"))

    @classmethod
    def get_metadata_from_file(cls, node: DocumentNode) -> dict:
        # Use Raw module methods
        return ModuleFacade.get_module("raw").get_metadata_from_file(node)

    @classmethod
    def get_metadata_from_data(cls, data: Data) -> dict:
        return ModuleFacade.get_module("raw").get_metadata_from_data(data)

    @classmethod
    def replace_orders(cls, data: Data) -> str:
        return ModuleFacade.get_module("raw").replace_orders(data)

    @classmethod
    def parse_file(cls, node: DocumentNode) -> InstanceDBEntry:
        return ModuleFacade.get_module("raw").parse_file(node)

    @classmethod
    def parse_data(cls, data: Data) -> InstanceDBEntry:
        result = ModuleFacade.get_module("raw").parse_data(data)
        #
        result.meta["module"] = "bordered_text"
        result.module = "bordered_text"
        return result
