import sys
import logging
from pathlib import Path, PurePath
# Own imports
from config import config
from module_manager import ModuleManager
from snippet_provider import yield_snippet, yield_snippet_with_args
from js_manager import JSManager
from css_manager import CSSManager
from structure_scanner import StructureScanner
from content_manager import ContentManager
#
import gui

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

    # TEMPORARY CONFIG SETUP
    config.target_path = PurePath(r'D:\hlag\tests\test_module')
    config.output_path = PurePath(r'D:\hlag')
    config.assets_path = PurePath(r'D:\hlag\assets')
    config.modules_path = PurePath(r'D:\hlag\modules')
    config.output_name = "document_output.txt"
    config.document_title = "DocuTest"
    config.embed_images = True
    config.base_path_length = 2

    # todo module_manager is instantiated
    # Initialize module manager before GUI since GUI might need to know what modules exist
    modules_directory = PurePath(PurePath(__file__).parent, "modules")
    ModuleManager.set_module_dir_patch(modules_directory)
    ModuleManager.fetch_modules()
    ModuleManager.initiate_modules()

    # todo css_manager is instantiated
    # In case GUI gives any option to change default CSS, it is instantiated before GUI

    # Start GUI
    # start_gui()

    # printer is instantiated
    # todo consider making it singleton
    printer = Printer()
    printer.set_output_file_path(PurePath(".", "document_output.txt"))

    # Configure StructureScanner
    StructureScanner.set_root_directory(config.target_path)

    # todo db_manager is instantiated

    # todo navigation_manager is instantiated

    # todo module_manager scans for modules
    # todo to be used when document elements are generated (get their generators)

    # todo structure_scanner scans structure
    # todo we get all metadata and attributes for the rest of modules
    StructureScanner.scan()

    # todo db_manager gets all dictionaries from structure_scanner

    # todo db_manager generates from structure_scanner data all 3-way tuples
    # todo (relPath, module, instance)

    # todo navigation manager gets document outline from structure_scanner
    # todo to craft a navigation JSON to be used by JS

    # todo if there's any outline, JS and CSS for navigation are registered
    # todo in js_manager and css_manager

    # todo content_manager gets generables from structure_scanner
    ContentManager.fetch_content_from_scanner()

    # todo content_manager produces 3-way tuples (id, data, meta)
    ContentManager.parse_files()

    #
    #   REGISTERING EVERYTHING FOR PRINTING
    #   register them in appropriate order
    #

    # Register document beginnig for printing
    printer.register(yield_snippet("beginning", title="TestDocu"))

    # Register document CSS for printing
    CSSManager.register(PurePath(PurePath(__file__).parent, r"assets\css\default.css"))
    printer.register(CSSManager.print())

    # Register middle part of document (after style and before body) for printing
    printer.register(yield_snippet("after-style"))

    # todo navigation manager registers navigation

    # ContentManager registers it's container for printinf
    printer.register(ContentManager.print_html_container())

    # Register JS parts for printing
    JSManager.register_file(PurePath(PurePath(__file__).parent, r"assets\js\navigation.js"))
    JSManager.register_file(PurePath(PurePath(__file__).parent, r"assets\js\content_manager.js"))
    JSManager.register_file(PurePath(PurePath(__file__).parent, r"assets\js\reference_resolver.js"))
    JSManager.register_other_print(ContentManager.print())
    printer.register(JSManager.print())

    # Register document ending for printing
    printer.register(yield_snippet("ending"))

    # Print
    printer.print()
