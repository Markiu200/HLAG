import sys
import logging
from pathlib import Path, PurePath
# Own imports
from config import config
from module_management import ModuleManager
from assets_manager import AssetsManager
from snippet_provider import yield_snippet, yield_snippet_with_args
from js_manager import JSManager
from css_manager import CSSManager
from structure_scanner import StructureScanner
from content_manager import ContentManager
from navigation_manager import NavigationManager
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
    config.target_path = PurePath(
        r'C:\Users\ksmforest\OneDrive\Dokumenty\_OD_przestrzenRobocza\wspolne\_html_docs\hlag_links\structure')
    config.output_path = PurePath(
        r'C:\Users\ksmforest\OneDrive\Dokumenty\_OD_przestrzenRobocza\wspolne\_html_docs\hlag_links')
    config.assets_path = PurePath(
        r'C:\Users\ksmforest\OneDrive\Dokumenty\_OD_przestrzenRobocza\wspolne\_html_docs\hlag_links')
    config.assets_dir_name = "assets"
    config.modules_path = PurePath(r'D:\hlag\modules')
    config.output_name = "used_links.html"
    config.document_title = "Links used for HLAG project"
    config.embed_images = True
    config.base_path_length = len(config.target_path.parts)

    # todo module_manager is instantiated
    # Initialize module manager before GUI since GUI might need to know what modules exist
    modules_directory = PurePath(PurePath(__file__).parent, "modules")
    ModuleManager.set_module_dir_patch(modules_directory)
    ModuleManager.fetch_modules()

    # Register Checks from modules before structure scan goes
    ModuleManager.initiate_modules()

    # todo css_manager is instantiated
    # In case GUI gives any option to change default CSS, it is instantiated before GUI

    # todo GUI for selecting target directory and other stuff
    # Start GUI
    # start_gui()

    # Initialize assets folder
    AssetsManager.initialize()

    # printer is instantiated
    # todo consider making it singleton
    printer = Printer()
    printer.set_output_file_path(PurePath(config.output_path, config.output_name))

    # Configure StructureScanner
    StructureScanner.set_root_directory(config.target_path)

    # Scan the structure
    StructureScanner.scan()

    # todo db_manager gets all dictionaries from structure_scanner

    # Content manager gets the files it can use from structure scanner
    ContentManager.fetch_content_from_scanner()

    # Content manager translates files to JSREF things
    ContentManager.parse_files()

    # todo navigation manager gets document outline from structure_scanner
    # todo to craft a navigation JSON to be used by JS
    NavigationManager.fetch_content_from_scanner()

    #
    #   REGISTERING EVERYTHING FOR PRINTING
    #   register them in appropriate order
    #

    # Register document beginnig for printing
    printer.register(yield_snippet_with_args("beginning", title=config.document_title))

    this_file_dir = PurePath(__file__).parent

    # Register document CSS for printing
    CSSManager.register(PurePath(this_file_dir, r"assets\css\default.css"))
    CSSManager.register(PurePath(this_file_dir, r"lib\navigation_manager\navigation.css"))
    printer.register(CSSManager.print())

    # Register middle part of document (after style and open body) for printing
    printer.register(yield_snippet("middle"))

    # Register navigation for printing
    printer.register(NavigationManager.print_html())

    # ContentManager registers it's container for printing
    printer.register(ContentManager.print_html())

    # Register JS parts for printing
    # state manager
    JSManager.register_file(PurePath(this_file_dir, r"assets\js\state_manager.js"))
    JSManager.register_file_delayed(PurePath(this_file_dir, r"assets\js\state_manager_delayed.js"))
    # ReferenceResolver
    JSManager.register_file(PurePath(this_file_dir, r"lib\content_manager\ref_resolver.js"))
    # Modules dependencies
    JSManager.register_file(PurePath(this_file_dir, r"lib\content_manager\dependencies.js"))
    # Modules
    ContentManager.queue_module_printing()
    # ContentManager
    JSManager.register_print(ContentManager.print_js())
    # Navigation
    JSManager.register_print(NavigationManager.print_js())
    # All of that to the printer
    printer.register(JSManager.print())

    # Register document ending for printing
    printer.register(yield_snippet("ending"))

    # Print
    printer.print()
    print("Done")
