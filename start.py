from pathlib import PurePath

from lib.n_config import Config
from lib.print_logger import PrintLogger
from lib.module_management import ModuleManager
from print_logger import PrintLogger


if __name__ == '__main__':
    logger = PrintLogger()

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

    main(config)
