from pathlib import PurePath
# Own imports
from js_manager import JSManager


class ModuleFacade:
    @classmethod
    def register_js(cls, path: PurePath):
        JSManager.register(path)
