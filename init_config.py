import logging
from pathlib import PurePath
from sys import stdout
# Own imports
if __name__ == '__main__':
    from sys import path as sys_path
    sys_path.append(str(PurePath(__file__).parent.parent))
from lib.n_config import Config


def init_config() -> Config:
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
    #
    return config_


def init_logger():
    # Configure logger
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s',
        handlers=[
            logging.FileHandler("logs.log"),
            logging.StreamHandler(stdout),
        ]
    )
