from pathlib import PurePath
import logging
from sys import stdout
# Own imports
from lib.n_config import Config
from lib.module_management import ModuleManager
from lib.base_gui_widget import BaseConfigWidget
from lib.toolbox import Toolbox
from gui import UserGUI


if __name__ == '__main__':
    # Configure logger
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s',
        handlers=[
            logging.FileHandler("logs.log"),
            logging.StreamHandler(stdout),
        ]
    )

    # Start Config
    Config.set_base_name("base_config")
    config_ = Config()
    base_config = config_.get_base_config()
    base_path = PurePath(__file__).parent
    base_config.set("base_path", str(base_path))
    base_config.set("target_path", str(PurePath(base_path, "inputs")))
    base_config.set("output_path", str(PurePath(base_path, "outputs")))
    base_config.set("assets_path", str(PurePath(base_path, "outputs")))
    base_config.set("modules_path", str(PurePath(base_path, "modules")))
    base_config.set("assets_dir_name", "assets")
    base_config.set("output_name", "output.html")
    base_config.set("output_title", "Pagemaker")
    base_config.set("logger_name", __name__)
    base_config.set("logger_level", logging.DEBUG)

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
