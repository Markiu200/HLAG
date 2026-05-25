import importlib
import os
import sys
import logging

logger = logging.getLogger(__name__)


class ModuleManager:
    def __init__(self, module_dir_path):
        self.module_dir_path = ""
        self.modules = []

        self.set_module_dir_patch(module_dir_path)
        self.fetch_modules()

    def set_module_dir_patch(self, path):
        if os.path.isdir(path):
            logger.info(f"Module directory found at {path}.")
            self.module_dir_path = path
            sys.path.append(path)
        else:
            logger.critical(f"User module directory {path} not found.")
            raise NotADirectoryError(f"User module directory {path} not found.")

    def fetch_modules(self):
        modules_directory_list = [f.name for f in os.scandir(self.module_dir_path) if f.is_dir() and not f.name.startswith("_")]
        logger.info(f"Found {len(modules_directory_list)} user modules - {modules_directory_list}")

        try:
            for a_module in modules_directory_list:
                self.modules.append((a_module, importlib.import_module(f"{a_module}.main", self.module_dir_path)))
        except Exception as e:
            logger.critical(f"Error occurred during user modules import.")
            raise e

    def get_module_names(self):
        return [x[0] for x in self.modules]

    def get_module_objects(self):
        return [x[1] for x in self.modules]
