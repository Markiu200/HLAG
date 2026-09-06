from pathlib import PurePath
# Own imports
from lib.n_config import Config
from lib.print_logger import PrintLogger
from lib.module_management import ModuleManager
from lib.gui.gui import UserGUI
from lib.base_gui_widget import BaseConfigWidget
from lib.toolbox import Toolbox


if __name__ == '__main__':
    logger = PrintLogger()

    # Start Config
    config_ = Config()
    base_config = config_.base_config
    base_path = PurePath(__file__).parent
    base_config.add_config_item("base_path", base_path)
    base_config.add_config_item("target_path", PurePath(base_path, "inputs"))
    base_config.add_config_item("output_path", PurePath(base_path, "outputs"))
    base_config.add_config_item("assets_path", PurePath(base_path, "outputs"))
    base_config.add_config_item("modules_path", PurePath(base_path, "modules"))
    base_config.add_config_item("assets_dir_name", "assets")
    base_config.add_config_item("output_name", "output.html")
    base_config.add_config_item("output_title", "Pagemaker")
    base_config.add_config_item("logger", logger)
    base_config.add_config_item("logger_level", 20)

    # Initialize Toolbox
    toolbox = Toolbox()

    # Start ModuleManager and check for modules
    module_manager = ModuleManager(config_, toolbox)
    module_manager.initialize()

    # Start GUI
    gui = UserGUI(config_)
    gui.add_config_widget(BaseConfigWidget)
    for widget in module_manager.get_gui_widgets():
        gui.add_config_widget(widget)
    gui.start()

    print(config_)
    # main(config, module_manager)
