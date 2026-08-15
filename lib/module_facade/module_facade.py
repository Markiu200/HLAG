from pathlib import PurePath
# Own imports
from js_manager import JSManager
from css_manager import CSSManager
from structure_scanner import StructureScanner
from content_manager import ContentManager
from module_management import ModuleManager
from assets_manager import AssetsManager


class ModuleFacade:
    """This class is here to be used by modules - a simple way to get the "singleton"
    kind of classes, and one place to import other stuff from."""
    content_manager = ContentManager

    @classmethod
    def register_js(cls, path: PurePath):
        JSManager.register_file(path)

    @classmethod
    def register_css(cls, path: PurePath):
        CSSManager.register(path)

    @classmethod
    def register_check(cls, check):
        StructureScanner.register_node_check(check)

    @classmethod
    def register_initial_dir_check(cls, check):
        StructureScanner.register_pre_directory_check(check)

    @classmethod
    def register_final_dir_check(cls, check):
        StructureScanner.register_post_directory_check(check)

    @classmethod
    def get_content_manager(cls):
        return ContentManager

    @classmethod
    def get_js_manager(cls):
        return JSManager

    @classmethod
    def get_css_manager(cls):
        return CSSManager

    @classmethod
    def get_structure_scanner(cls):
        return StructureScanner

    @classmethod
    def get_assets_manager(cls):
        return AssetsManager

    @classmethod
    def get_module(cls, module_name: str):
        return ModuleManager.get_module(module_name)
