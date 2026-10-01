from pathlib import PurePath
# Own imports
from lib.module_manager import ModuleManager
from lib.base_gui_widget import BaseConfigWidget
from lib.toolbox import Toolbox
from gui import UserGUI
from main import main
from init_config import init_config, init_logger


if __name__ == '__main__':
    # Configure logger
    init_logger()

    # Start Config
    config_ = init_config(PurePath(__file__).parent)

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

    main(config_, module_manager)
