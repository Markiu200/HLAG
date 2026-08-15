import importlib
import os
import sys
import logging
from pathlib import PurePath
# Own imports
from module_management import IModule

logger = logging.getLogger(__name__)


class Module:
    def __init__(self, name: str, module_file, module_class: IModule, module_info: dict):
        self.name = name
        self.module_file = module_file
        self.module_class = module_class
        self.module_info = module_info


class ModuleManager:
    modules_dir_path = ""
    found_modules = []

    @classmethod
    def set_module_dir_patch(cls, path):
        # todo new logger
        path = str(path)  # neither sys not importlib do PurePaths
        if os.path.isdir(path):
            logger.info(f"Module directory found at {path}.")
            cls.modules_dir_path = path
            sys.path.append(path)
        else:
            logger.critical(f"User module directory {path} not found.")
            raise NotADirectoryError(f"User module directory {path} not found.")

    @classmethod
    def fetch_modules(cls):
        modules_directory_list = [f.name for f in os.scandir(cls.modules_dir_path) if f.is_dir() and not f.name.startswith("_")]
        logger.info(f"Found {len(modules_directory_list)} user modules - {modules_directory_list}")

        try:
            for a_module in modules_directory_list:
                module_file = importlib.import_module(f"{a_module}.main")
                module = module_file.get_module_main_class()
                module_info = module.get_info()
                cls.found_modules.append(Module(
                    name=module_info.get("name", a_module),
                    module_file=module_file,
                    module_class=module,
                    module_info=module_info
                ))
        except Exception as e:
            logger.critical(f"Error occurred during user modules import.")
            raise e

    @classmethod
    def initiate_modules(cls):
        cls.found_modules.sort(key=lambda a_module: a_module.module_info.get("priority", 0))
        for registered_module_item in cls.found_modules:
            registered_module_item.module_class.register_checks()

    @classmethod
    def get_module(cls, module_name: str) -> IModule:
        for registered_module_item in cls.found_modules:
            if registered_module_item.name == module_name:
                return registered_module_item.module_class
