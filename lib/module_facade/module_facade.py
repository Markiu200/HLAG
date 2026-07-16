from pathlib import PurePath
# Own imports
from js_manager import JSManager
from structure_scanner import StructureScanner
from structure_scanner import BaseCheck
from structure_scanner import DocumentNode


class ModuleFacade:
    @classmethod
    def register_js(cls, path: PurePath):
        JSManager.register(path)

    @classmethod
    def register_check(cls, callback):
        StructureScanner.register_pre_metaread_node_check(callback)
