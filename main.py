import sys
import logging
from pathlib import Path, PurePath
# Own imports
from models.config import config
import gui
from module_manager import ModuleManager
from outline_manager import OutlineManager
from structure_reader_new import StructureReader
from printer.printer import Printer


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

    # todo module_manager is instantiated
    # Initialize module manager before GUI since GUI might need to know what modules exist
    modules_lib_directory = str(Path(Path.cwd(), "modules"))
    module_manager = ModuleManager(modules_lib_directory)

    # todo css_manager is instantiated
    # In case GUI gives any option to change default CSS, it is instantiated before GUI

    start_gui()

    # todo js_manager is instatiated

    # todo structure_scanner is instantiated

    # todo db_manager is instantiated

    # todo navigation_manager is instantiated

    # todo content_manager is instantiated

    # printer is instantiated
    # todo Output file can be changed in GUI and/or cmd argument
    printer = Printer()
    printer.set_output_file_path(PurePath(".", "document_output.txt"))

    # todo module_manager scans for modules
    # todo to be used when document elements are generated (get their generators)

    # todo structure_scanner scans structure
    # todo we get all metadata and attributes for the rest of modules

    # todo db_manager gets all dictionaries from structure_scanner

    # todo db_manager generates from structure_scanner data all 3-way tuples
    # todo (relPath, module, instance)

    # todo navigation manager gets document outline from structure_scanner
    # todo to craft a navigation JSON to be used by JS

    # todo if there's any outline, JS and CSS for navigation are registered
    # todo in js_manager and css_manager

    # todo content_manager gets generables from structure_scanner

    # todo content_manager produces 3-way tuples (module, instance, instructions)
    # todo for each generable and saves them internally

    # todo content manager registers in js_manager js for js manager (in HTML/js)

    # todo register everything in printer

    # todo default start snippet

    # todo css_manager registers all needed CSS and default CSS

    # todo middle snippet registered

    # todo js_manager register pre-content JS

    # todo navigation manager registers navigation

    # todo content_manager registers content

    # todo js_manager registers post-content JS

    # todo end snippet registered

    # todo print
    printer.print()

    # # After GUI we should have target directory
    # config.base_path_length = len(config.target_path.parts)
    #
    # structure_reader = StructureReader()
    #
    # outline_manager = OutlineManager()
    # structure_reader.set_outline_manager(outline_manager)
    #
    # # Go through the structure and feed other managers
    # structure_reader.scan()
    #
    # print(structure_reader)
    #
    # # todo Write result
    # # with open("output.txt", "w") as file:
    # #     file.write(site_builder.build())
    #
    # # printer = BasePrinter()
    #
    # # a = input()

