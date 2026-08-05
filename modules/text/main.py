import re
from pathlib import PurePath
# Own imports
from module_facade import ModuleFacade, DocumentNode, Data, InstanceDBEntry
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
        pass

    @classmethod
    def register_files(cls):
        ModuleFacade.register_js(PurePath(cls.module_path, "js.js"))

    @classmethod
    def get_metadata_from_file(cls, node: DocumentNode) -> dict:
        return ModuleFacade.get_module("raw").get_metadata_from_file(node)

    @classmethod
    def get_metadata_from_data(cls, data: Data) -> dict:
        return ModuleFacade.get_module("raw").get_metadata_from_string(data)

    @classmethod
    def replace_orders(cls, data: Data) -> str:
        return ModuleFacade.get_module("raw").replace_orders(data)

    @classmethod
    def parse_file(cls, node: DocumentNode) -> InstanceDBEntry:
        past_meta_location = node.metadata.get("cursor", 0)
        with open(node.path) as f:
            f.seek(past_meta_location)
            content = f.read()
        return cls.parse_data(Data(content=content, meta=node.metadata))

    @classmethod
    def parse_data(cls, data: Data) -> InstanceDBEntry:
        content = cls.replace_orders(data)
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
            meta=data.meta
        )
        return result
