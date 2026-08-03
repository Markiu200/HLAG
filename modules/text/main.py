import re
from pathlib import PurePath
# Own imports
from module_facade import ModuleFacade, DocumentNode
from module_management import IModule
#
from txt_check import TXTCheck


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
            "jsmanager": "TextModuleManager"
        }

    @classmethod
    def register_checks(cls):
        # ModuleFacade.register_check(TXTCheck())
        pass

    @classmethod
    def register_files(cls):
        ModuleFacade.register_js(PurePath(cls.module_path, "js.js"))

    @classmethod
    def read_metadata_from_file(cls, node: DocumentNode) -> dict:
        return ModuleFacade.get_module("raw").read_metadata_from_file(node)

    @classmethod
    def read_metadata_from_string(cls, content: str) -> dict:
        return ModuleFacade.get_module("raw").read_metadata_from_string(content)

    @classmethod
    def replace_references(cls, content: str) -> str:
        return ModuleFacade.get_module("raw").replace_references(content)

    @classmethod
    def parse_from_file(cls, node: DocumentNode) -> dict:
        return ModuleFacade.get_module("raw").parse_from_file(node)

    @classmethod
    def parse_from_string(cls, content: str, meta: dict) -> dict:
        content = cls.replace_references(content)
        lines = []
        last_ref_location = 0
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
        result = {
            "module": "text",
            "data": {"nodes": lines},
            "meta": meta
        }
        return result
