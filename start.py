from pathlib import PurePath

from lib.n_config import Config
from lib.print_logger import PrintLogger
from lib.module_management import ModuleManager
from lib.gui import gui


if __name__ == '__main__':
    logger = PrintLogger()

    # Start Config
    config = Config()
    base_config = config.base_config
    base_config.add_config_item("target_path", PurePath(PurePath(__file__).parent, "inputs"))
    base_config.add_config_item("output_path", PurePath(PurePath(__file__).parent, "outputs"))
    base_config.add_config_item("assets_path", PurePath(PurePath(__file__).parent, "outputs"))
    base_config.add_config_item("modules_path", PurePath(PurePath(__file__).parent, "modules"))
    base_config.add_config_item("assets_dir_name", "assets")
    base_config.add_config_item("output_name", "output.html")
    base_config.add_config_item("output_title", "DocuMaker")
    base_config.add_config_item("logger", logger)

    # Start ModuleManager and check for modules
    module_manager = ModuleManager(config)
    module_manager.initialize()

    # Start GUI
    gui.start()

    # main(config, module_manager)
