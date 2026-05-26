import sys
import logging
from pathlib import Path
# Own imports
from models.config import config
import gui
from module_manager import ModuleManager
from outline_manager import OutlineManager
from structure_reader_new import StructureReader


def initialize_logger():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        handlers=[
            logging.FileHandler("logs.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    config.logger = logging.getLogger(__name__)


def start_gui():
    # Read config from user input
    # todo Launch part - make it launchable w/o GUI
    # import argparse
    gui.start()

    # assuming it is not checked at input level, do the extra directory scan
    if not Path(config.target_path).exists():
        config.logger.error(f"Root directory of {config.target_path} does not exist!")
        raise FileExistsError("File or directory of targeted path not found")
    if Path(config.target_path) == Path.cwd():
        config.logger.error(f"Root directory of {config.target_path} not allowed! Choose another.")
        raise IsADirectoryError(f"Root directory of {config.target_path} not allowed!")

    config.logger.info(f"Root directory set to {config.target_path}.")


if __name__ == "__main__":
    initialize_logger()

    # Initialize module manager before GUI since GUI might need to know what modules exist
    modules_lib_directory = str(Path(Path.cwd(), "modules"))
    module_manager = ModuleManager(modules_lib_directory)

    start_gui()

    # After GUI we should have target directory
    config.base_path_length = len(config.target_path.parts)

    structure_reader = StructureReader()

    outline_manager = OutlineManager()
    structure_reader.set_outline_manager(outline_manager)

    # Go through the structure and feed other managers
    structure_reader.scan()

    print(structure_reader)


# todo Write result
# with open("output.html", "w") as file:
#     file.write(site_builder.build())
