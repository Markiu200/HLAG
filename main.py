import sys
import logging
from pathlib import Path, PurePath
# Own imports
from config import config
from module_manager import ModuleManager
from snippet_provider import yield_snippet
from js_manager import JSManager
from css_manager import CSSManager
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
    config.target_path = PurePath(r'D:\hlag\webpage')
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

    # todo metadata_reader is configured
    # MetadataReader.set_tag_regex(r'\[%>(.*?):(.*?)]')
    # MetadataReader.set_logger(config.logger)

    # todo structure_scanner is instantiated
    # structure_scanner = StructureScanner(config.target_path)
    # structure_scanner.register_text_type_extensions({".txt", ".md", ".html", ".json"})

    # todo db_manager is instantiated

    # todo navigation_manager is instantiated

    # todo content_manager is instantiated

    # todo module_manager scans for modules
    # todo to be used when document elements are generated (get their generators)

    # todo structure_scanner scans structure
    # todo we get all metadata and attributes for the rest of modules
    # structure_scanner.scan()

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

    # todo content_manager registers content

    # Register JS parts for printing
    JSManager.register(PurePath(PurePath(__file__).parent, r"assets\js\navigation.js"))
    JSManager.register(PurePath(PurePath(__file__).parent, r"assets\js\content_manager.js"))
    JSManager.register(PurePath(PurePath(__file__).parent, r"assets\js\reference_resolver.js"))
    printer.register(JSManager.print())

    # Register document ending for printing
    printer.register(yield_snippet("ending"))

    # Print
    printer.print()
