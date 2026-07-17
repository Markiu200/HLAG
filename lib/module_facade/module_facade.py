from pathlib import PurePath
# Own imports
from js_manager import JSManager
from css_manager import CSSManager
from structure_scanner import StructureScanner
from structure_scanner import BaseCheck
from structure_scanner import DocumentNode
from content_manager import ContentManager
from module_manager import ModuleManager


class ModuleFacade:
    """This class is here to be used by modules - a simple way to get the "singleton"
    kind of classes, and one place to import other stuff from."""

    @classmethod
    def register_js(cls, path: PurePath):
        JSManager.register_file(path)

    @classmethod
    def register_css(cls, path: PurePath):
        CSSManager.register(path)

    @classmethod
    def register_check(cls, callback):
        StructureScanner.register_node_check(callback)

    @classmethod
    def get_content_manager(cls):
        return ContentManager

    @classmethod
    def get_module(cls, module_name: str):
        return ModuleManager.get_module(module_name)
