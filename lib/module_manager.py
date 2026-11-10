import importlib
import os
import logging
from sys import path as sys_path
from pathlib import PurePath
# Own imports
if __name__ == '__main__':
    sys_path.append(str(PurePath(__file__).parent.parent))
from lib.imodule import IModule
from lib.base_check import BaseCheck
from lib.n_config import Config
from lib.toolbox import Toolbox


class Module:
    def __init__(self, module_class: type, module_instance: IModule, module_info: dict, codename: str):
        self.module_class = module_class
        self.module_instance = module_instance
        self.module_info = module_info
        self.codename = codename


class ModuleManager:
    def __init__(self, config: Config, toolbox: Toolbox):
        self.config = config
        # Logger
        self.logger = None
        if self.config.get_base_config().get("logger_name"):
            self.logger = logging.getLogger(self.config.get_base_config().get("logger_name"))
        self.toolbox = toolbox
        #
        self.modules_dir_path = None
        self.registered_modules: list[Module] = []
        self.registered_prints: list[tuple] = []
        self.registered_checks: list[tuple] = []

    def initialize(self):
        modules_path = str(self.config.get_base_config().get("modules_path"))  # neither sys not importlib do PurePaths
        if os.path.isdir(modules_path):
            if self.logger:
                self.logger.info(f"Module directory found at {modules_path}.")
            self.modules_dir_path = modules_path
            sys_path.append(modules_path)
            self._fetch_modules()
            # Initialize modules
            for module in self.registered_modules:
                module.module_instance.pm_init()

        else:
            if self.logger:
                self.logger.critical(f"User module directory {modules_path} not found.")
            raise NotADirectoryError(f"User module directory {modules_path} not found.")

    def _fetch_modules(self):
        modules_directory_list = [f.name for f in os.scandir(self.modules_dir_path) if f.is_dir() and not f.name.startswith("_")]
        if self.logger:
            self.logger.info(f"Found {len(modules_directory_list)} user modules - {modules_directory_list}")
        try:
            for module_dir_name in modules_directory_list:

                # Step 1 - Check if main.py exists
                module_path = PurePath(self.modules_dir_path, module_dir_name)
                if not os.path.isfile(str(PurePath(module_path, "main.py"))):
                    if self.logger:
                        self.logger.error(f"Directory {module_dir_name} in module directory has no main.py file - skipping")
                    continue

                # Step 2 - Try to register
                try:
                    module_import = importlib.import_module(f"{module_dir_name}.main")
                    module_instance = module_import.register(self)
                    self.register_module(module_instance, fallback_name=module_dir_name)

                except ModuleNotFoundError as e:
                    if self.logger:
                        self.logger.critical(f"Error occurred during user modules import - module {module_dir_name}")
                    raise e
                except AttributeError:
                    if self.logger:
                        self.logger.error(f"Module {module_dir_name} has no register() method in main.py - skipping")
                    continue
        except Exception as e:
            if self.logger:
                self.logger.critical(f"Error occurred during user modules import.")
            raise e

    ################
    # Registration #
    ################
    def register_module(self, module: IModule, fallback_name: str = None):
        module_instance = module
        module_class = type(module)
        module_info = module.info
        codename = module.info.get("codename")
        if not codename:
            if not fallback_name:
                if self.logger:
                    self.logger.critical("Module registration error - no codename nor fallback name provided")
                    raise RuntimeError("Module registration error - no codename nor fallback name provided")
            else:
                codename = fallback_name
                if self.logger:
                    self.logger.warning(f"Module {fallback_name} fallback name used - no codename specified")
        #
        new_module = Module(
            module_class=module_class,
            module_instance=module_instance,
            module_info=module_info,
            codename=codename
        )
        #
        self.registered_modules.append(new_module)

    def register_print(self, codename: str, value, code_type: str, is_file: bool, is_delayed: bool):
        """Meant to be used by pmmodules in their __init__. 'codename' would be their codename."""
        self.registered_prints.append(
            (value, code_type, is_file, is_delayed)
        )

    def register_check(self, codename: str, check: BaseCheck, check_type: str):
        """Meant to be used by pmmodules in their __init__. 'codename' would be their codename."""
        self.registered_checks.append((codename, check, check_type))

    ###########
    # Getters #
    ###########
    # Modules
    def get_modules_list(self):
        return self.registered_modules

    def get_modules_dict_by_codename(self):
        keyed = dict()
        for module in self.registered_modules:
            keyed[module.codename] = module
        return keyed

    def get_check_list(self):
        priority_check_list = []
        sorted_check_list = []
        for registered_module in self.registered_modules.values():
            for check in registered_module.module_instance.checks:
                priority_check_list.append((registered_module.module_info.get("priority"), check))
        priority_check_list.sort(key=lambda pair: pair[0])
        for check_pair in priority_check_list:
            sorted_check_list.append(check_pair[1])
        return sorted_check_list

    def get_gui_widgets(self):
        widget_list = []
        for registered_module in self.registered_modules.values():
            module_config = self.config.get_config(registered_module.module_info.get("codename"))
            if module_config:
                widget = widget_list.append(module_config.get_widget())
                if widget:
                    widget_list.append(widget)
        return widget_list

    def get_module_object(self, codename: str) -> IModule:
        return self.registered_modules.get(codename).module_instance

    def get_registered_module(self, codename: str) -> Module:
        return self.registered_modules.get(codename)


__all__ = [ModuleManager, Module]

if __name__ == '__main__':
    from init_config import init_config, init_logger
    #
    init_logger()
    config_ = init_config(PurePath(__file__).parent.parent)
    toolbox_ = Toolbox()
    module_manager_ = ModuleManager(config_, toolbox_)
    module_manager_.initialize()
    #
    registered_modules_ = module_manager_.get_modules_dict_by_codename()
    print("Finished. Set breakpoint here.")
