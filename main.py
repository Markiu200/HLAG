from pathlib import PurePath
from os import path as os_path
import logging
import re
import json
# Own imports
from init_config import init_config, init_logger
from lib.n_config import Config
from lib.module_manager import ModuleManager
from lib.toolbox import Toolbox
from lib.document_node import DocumentNode
from lib.structure_scanner import StructureScanner
from lib.assets_manager import AssetsManager
from lib.code_block import CodeBlock
from lib.content_manager import ContentManager
from assets.html_snippets import html_snippets
# from lib.snippet_provider import yield_snippet, yield_snippet_with_args
# from lib.snippets import ContentManager
# from lib.linker import Linker
# from lib.printer.printer import Printer


# todo asset manager doesn't create assets folder if not needed
# todo output directory created if doesn't exist
# todo documentation on usage of modules
# todo add config for "Home" in outline
# todo css_manager instantiated early to be able to choose styles
# todo db_manager gets all dictionaries from structure_scanner
# todo check if output folder exists

def main(config: Config, module_manager: ModuleManager):
    config_ns = config.get_base_config()
    toolbox = module_manager.toolbox
    assets_dir = PurePath(PurePath(__file__).parent, "assets")

    # Pre-checks
    ## Check if output directory in config:output_path exists (required in printing step)
    if not os_path.isdir(str(config_ns.get("output_path"))):
        raise NotADirectoryError(f"Output directory {str(config_ns.get('output_path'))} doesn't exist.")

    # Set up logger
    logger = None
    if config_ns.get("logger_name"):
        logger = logging.getLogger(config.get_base_config().get("logger_name"))

    # Set up root node
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
            logger.critical(f"Source path {config_ns.get('target_path')} is not an directory")
        raise e

    # Structure scanner part
    try:
        if root_node:
            structure_scanner = StructureScanner(root_node)
            structure_scanner.scan()
            toolbox.structure_scanner = structure_scanner
    except NotADirectoryError as e:
        if logger:
            logger.critical(f"Source path {config_ns.get('target_path')} is not an directory")
        raise e

    # Assets manager part
    try:
        if not os_path.isdir(config_ns.get('output_path')):
            raise NotADirectoryError(f"Output path {config_ns.get('output_path')} is not an directory")
        pattern = re.compile('[^a-zA-Z0-9 ]')
        if pattern.search(config_ns.get('assets_dir_name')):
            raise ValueError(f"Assets directory name contains illegal characters, it should contain only alphanumeric characters.")
        assets_manager = AssetsManager(
            assets_dir_name=config_ns.get('assets_dir_name'),
            input_dir_path=config_ns.get('target_path'),
            output_dir_path=config_ns.get('output_path')
        )
        toolbox.assets_manager = assets_manager
    except Exception as e:
        if logger:
            logger.critical(e)
        raise e

    #
    # Javascript manager part
    #
    js_manager = CodeBlock("<script>", "</script>")
    toolbox.js_manager = js_manager

    #
    # CSS manager part
    #
    css_manager = CodeBlock("<style>", "</style>", logger_name=config_ns.get("logger_name"))
    toolbox.css_manager = css_manager
    ## Register default CSS
    css_manager.register(PurePath(assets_dir, "css", "default.css"), is_file=True, delayed=False)

    #
    # ContentManager part
    #
    content_manager = ContentManager(module_manager.get_all_registered_modules())
    content_manager.run(root_node)

    #
    # Other parts here
    #

    #
    # Printing part
    #
    # Steps:
    # 1. Output directory must already exist - check that maybe before all the algoriths above.
    #    a. Assets directory may not exist, it may not be needed - AssetsManager will create one if needed
    # 2. Open file in config:output_path with name of config:output_name.
    # 3. Write in all the static code and code received from all other classes.
    #    a. By this time, JSManager and CSSManager should have all the code registered in them.
    # 4. Done.
    #
    file_name = str(PurePath(config_ns.get("output_path"), config_ns.get("output_name")))
    with open(file_name, "wt") as f:
        beginning_code = html_snippets.get("beginning")
        beginning_code = beginning_code.replace("!PLACEHOLDER:TITLE!", config_ns.get("output_title"))
        f.write(beginning_code)
        f.write(css_manager.print())
        f.write(html_snippets.get("middle"))
        f.write(html_snippets.get("nav"))
        f.write(html_snippets.get("main"))
        f.write(js_manager.print())
        f.write(html_snippets.get("ending"))

    return 0


    # Printer is instantiated
    printer = Printer()
    printer.set_output_file_path(PurePath(
        config.get_base_config().get("output_path"),
        config.get_base_config().get("output_name"))
    )

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
    JSManager.register_file(PurePath(this_file_dir, r"snippets\ref_resolver.js"))
    # Modules dependencies
    JSManager.register_file(PurePath(this_file_dir, r"snippets/js_module_instance.js"))
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
    toolbox_ = Toolbox()

    # Start ModuleManager and check for modules
    module_manager_ = ModuleManager(config_, toolbox_)
    module_manager_.initialize()

    main(config_, module_manager_)
