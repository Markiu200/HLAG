import importlib
import os
import sys
import logging

logger = logging.getLogger(__name__)


class Module:
    def __init__(self, name: str, module):
        self.name = name
        self.module = module


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
                cls.found_modules.append(Module(
                    name=a_module,
                    module=importlib.import_module(f"{a_module}.main")
                ))
        except Exception as e:
            logger.critical(f"Error occurred during user modules import.")
            raise e

    @classmethod
    def initiate_modules(cls):
        for module in cls.found_modules:
            module.module.init()

    @classmethod
    def get_print_method(cls, module_name: str):
        for module in cls.found_modules:
            if module.name == module_name:
                return module.module.parse
