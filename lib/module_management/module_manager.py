import importlib
import os
import sys
# Own imports
from lib.module_management import IModule
from lib.n_config import Config


class Module:
    def __init__(self, name: str, module_import, module_main_class: IModule, module_info: dict):
        self.name = name
        self.module_import = module_import
        self.module_main_class = module_main_class
        self.module_info = module_info


class ModuleManager:
    def __init__(self, config: Config):
        self.config = config
        self.modules_dir_path = None
        self.modules_found = []
        self.logger = self.config.get_base_config().get("logger")

    def initialize(self):
        path = str(self.config.get_base_config().get("modules_path"))  # neither sys not importlib do PurePaths
        if os.path.isdir(path):
            if self.logger:
                self.logger.info(f"Module directory found at {path}.")
                self.modules_dir_path = path
                sys.path.append(path)
                self._fetch_modules()
        else:
            if self.logger:
                self.logger.critical(f"User module directory {path} not found.")
            raise NotADirectoryError(f"User module directory {path} not found.")

    def _fetch_modules(self):
        modules_directory_list = [f.name for f in os.scandir(self.modules_dir_path) if f.is_dir() and not f.name.startswith("_")]
        if self.logger:
            self.logger.info(f"Found {len(modules_directory_list)} user modules - {modules_directory_list}")

        try:
            for a_module in modules_directory_list:
                module_import = importlib.import_module(f"{a_module}.main")
                module_main_class = module_import.get_module_main_class()
                module_info = module_main_class.get_info()
                self.modules_found.append(Module(
                    name=module_info.get("name", a_module),
                    module_import=module_import,
                    module_main_class=module_main_class,
                    module_info=module_info
                ))
        except Exception as e:
            if self.logger:
                self.logger.critical(f"Error occurred during user modules import.")
            raise e

    def register_modules_checks(self):
        self.modules_found.sort(key=lambda a_module: a_module.module_info.get("priority", 0))
        for registered_module_item in self.modules_found:
            registered_module_item.module_main_class.register_checks()

    def get_module(self, module_name: str) -> IModule:
        for registered_module_item in self.modules_found:
            if registered_module_item.name == module_name:
                return registered_module_item.module_main_class
