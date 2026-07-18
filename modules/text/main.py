import re
from pathlib import PurePath
# Own imports
from module_facade import ModuleFacade, DocumentNode
from base_module import IModule
#
from txt_check import TXTCheck
import replace_references as rr
import read_metadata_from_file as rmff
import read_metadata_from_lines as rmfl


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
        ModuleFacade.register_check(TXTCheck())

    @classmethod
    def register_files(cls):
        ModuleFacade.register_js(PurePath(cls.module_path, "js.js"))

    @classmethod
    def read_metadata_from_file(cls, node: DocumentNode) -> dict:
        return rmff.get_metadata_from_file(node.path)

    @classmethod
    def read_metadata_from_string(cls, content: str) -> dict:
        return rmfl.read_metadata_from_lines([content])

    @classmethod
    def replace_references(cls, content: str) -> str:
        return rr.replace_references(content)

    @classmethod
    def parse_from_file(cls, node: DocumentNode) -> dict:
        past_meta_location = node.metadata.get("cursor", 0)
        with open(node.path) as f:
            f.seek(past_meta_location)
            return cls.parse_from_string(f.read(), node.metadata)

    @classmethod
    def parse_from_string(cls, content: str, meta: dict) -> dict:
        content = cls.replace_references(content)
        lines = []
        last_ref_location = 0
        while True:
            search = re.search(r'\[%JSREF\(.*?\)%]', content[last_ref_location:])
            if not search:
                break
            lines.append(content[last_ref_location:search.regs[0][0]+last_ref_location])
            lines.append(content[search.regs[0][0]+last_ref_location:search.regs[0][1]+last_ref_location])
            last_ref_location += search.regs[0][1]
        lines.append(content[last_ref_location:])
        #
        result = {
            "module": "text",
            "data": {"nodes": lines},
            "meta": meta
        }
        return result
