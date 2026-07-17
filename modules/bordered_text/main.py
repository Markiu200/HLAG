import re
from pathlib import PurePath
# Own imports
from module_facade import ModuleFacade, DocumentNode
from base_module import IModule


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
            "jsmanager": "BorderedTextModuleManager"
        }

    @classmethod
    def register_checks(cls):
        pass

    @classmethod
    def register_files(cls):
        ModuleFacade.register_js(PurePath(cls.module_path, "js.js"))

    @classmethod
    def read_metadata_from_file(cls, node: DocumentNode) -> dict:
        # Use Text module methods
        return ModuleFacade.get_module("text").read_metadata_from_file(node)

    @classmethod
    def read_metadata_from_string(cls, content: str) -> dict:
        return ModuleFacade.get_module("text").read_metadata_from_string(content)

    @classmethod
    def replace_references(cls, content: str) -> str:
        return ModuleFacade.get_module("text").replace_references(content)

    @classmethod
    def parse_from_file(cls, node: DocumentNode) -> dict:
        return ModuleFacade.get_module("text").parse_from_file(node)

    @classmethod
    def parse_from_string(cls, content: str, meta: dict) -> dict:
        result = ModuleFacade.get_module("text").parse_from_string(content, meta)
        #
        result["module"] = "bordered_text"
        return result
