from pathlib import PurePath
from os import path as os_path
import logging
# Own imports
from init_config import init_config, init_logger
from lib.n_config import Config
from lib.module_manager import ModuleManager
# from lib.assets_manager.assets_manager import AssetsManager
from lib.toolbox import Toolbox
# from lib.snippet_provider import yield_snippet, yield_snippet_with_args
# from lib.js_manager import JSManager
# from lib.css_manager import CSSManager
from lib.structure_scanner import StructureScanner
from lib.document_node import DocumentNode
# from lib.content_manager import ContentManager
# from lib.linker import Linker
# from lib.printer.printer import Printer
from init_config import init_config, init_logger


# todo asset manager doesn't create assets folder if not needed
# todo output directory created if doesn't exist
# todo documentation on usage of modules
# todo add config for "Home" in outline

def main(config: Config, module_manager: ModuleManager):
    config_ns = config.get_base_config()

    # Set up logger
    logger = None
    if config_ns.get("logger_name"):
        logger = logging.getLogger(config.get_base_config().get("logger_name"))

    # Set up root node
    root_node = None
    try:
        if not os_path.isdir(str(config_ns.get("target_path"))):
            raise NotADirectoryError()
        DocumentNode.set_root_path(config_ns.get("target_path"))
        root_node = DocumentNode(config_ns.get("target_path"), True)
        root_node.set_metadata("title", "Home")
        # root_node.set_metadata("relPath", "_")
        # root_node.set_metadata("hostPath", "_")
        # root_node.set_metadata("relLink", "_")
        #
    except NotADirectoryError as e:
        if logger:
            logger.critical(f"Source path {config.get_base_config().get('target_path')} is not an directory")
            raise e

    # Structure scanner part
    try:
        if root_node:
            structure_scanner = StructureScanner(root_node)
            structure_scanner.scan()
    except NotADirectoryError as e:
        if logger:
            logger.critical(f"Source path {config.get_base_config().get('target_path')} is not an directory")
            raise e

    return 0




    # Module manager is instantiated
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
    start_gui()

    # Initialize assets manager
    assets_manager = AssetsManager(config)
    assets_manager.initialize()

    # Printer is instantiated
    printer = Printer()
    printer.set_output_file_path(PurePath(
        config.get_base_config().get("output_path"),
        config.get_base_config().get("output_name"))
    )

    # Configure StructureScanner
    StructureScanner.set_root_directory(config.get_base_config().get("target_path"))

    # Scan the structure
    StructureScanner.scan()

    # todo db_manager gets all dictionaries from structure_scanner

    # Content manager gets the files it can use from structure scanner
    ContentManager.fetch_content_from_scanner()

    # Content manager translates files to JSREF things
    ContentManager.parse_files()

    #
    #   REGISTERING EVERYTHING FOR PRINTING
    #   register them in appropriate order
    #

    # Register document beginnig for printing
    printer.register(yield_snippet_with_args("beginning", title=config.get_base_config().get("output_title")))

    this_file_dir = PurePath(__file__).parent

    # Register document CSS for printing
    CSSManager.register(PurePath(this_file_dir, r"assets\css\default.css"))
    printer.register(CSSManager.print())

    # Register middle part of document (after style and open body) for printing
    printer.register(yield_snippet("middle"))

    # Register navigation for printing
    printer.register(yield_snippet("nav"))

    # ContentManager registers it's container for printing
    printer.register(ContentManager.print_html())

    # Register JS parts for printing
    # state manager
    JSManager.register_file(PurePath(this_file_dir, r"assets\js\state_manager.js"))
    JSManager.register_file_delayed(PurePath(this_file_dir, r"assets\js\state_manager_delayed.js"))
    # Linker
    JSManager.register_print(Linker.print_js())
    # ReferenceResolver
    JSManager.register_file(PurePath(this_file_dir, r"lib\content_manager\ref_resolver.js"))
    # Modules dependencies
    JSManager.register_file(PurePath(this_file_dir, r"lib\content_manager\dependencies.js"))
    # Modules
    ContentManager.queue_module_printing()
    # ContentManager
    JSManager.register_print(ContentManager.print_js())
    # All of that to the printer
    printer.register(JSManager.print())

    # Register document ending for printing
    printer.register(yield_snippet("ending"))

    # Print
    # printer.print()
    print("Done")


if __name__ == "__main__":
    # Configure logger
    init_logger()

    # Start Config
    config_ = init_config(PurePath(__file__).parent)

    # Initialize Toolbox
    toolbox = Toolbox()

    # Start ModuleManager and check for modules
    module_manager_ = ModuleManager(config_, toolbox)
    module_manager_.initialize()

    main(config_, module_manager_)
