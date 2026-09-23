from pathlib import PurePath
# Own imports
from lib.print_logger import PrintLogger
from lib.n_config import Config
from lib.module_management.module_manager import ModuleManager
from lib.assets_manager.assets_manager import AssetsManager
from lib.toolbox import Toolbox
from lib.snippet_provider import yield_snippet, yield_snippet_with_args
from lib.js_manager import JSManager
from lib.css_manager import CSSManager
from lib.structure_scanner import StructureScanner
from lib.content_manager import ContentManager
from lib.linker import Linker
from lib.printer.printer import Printer


def main(config, module_manager):
    # TEMPORARY CONFIG SETUP
    # config.target_path = PurePath(r'D:\hlag_t')
    # config.output_path = PurePath(r'D:\hlag_t_doc')
    # config.assets_path = PurePath(r'D:\hlag_t_doc')
    # config.assets_dir_name = "assets"
    # config.modules_path = PurePath(r'D:\hlag\modules')
    # config.output_name = "hlag_t.html"
    # config.document_title = "General testing target"
    # config.embed_images = True
    # config.base_path_length = len(config.target_path.parts)

    # todo asset manager doesn't create assets folder if not needed
    # todo output directory created if doesn't exist
    # todo documentation on usage of modules

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
    logger = PrintLogger()

    # Start Config
    config_ = Config()
    base_config = config_.base_config
    base_path = PurePath(__file__).parent
    base_config.add_config_item("base_path", base_path)
    base_config.add_config_item("target_path", PurePath(base_path, "inputs"))
    base_config.add_config_item("output_path", PurePath(base_path, "outputs"))
    base_config.add_config_item("assets_path", PurePath(base_path, "outputs"))
    base_config.add_config_item("modules_path", PurePath(base_path, "modules"))
    base_config.add_config_item("assets_dir_name", "assets")
    base_config.add_config_item("output_name", "output.html")
    base_config.add_config_item("output_title", "Pagemaker")
    base_config.add_config_item("logger", logger)
    base_config.add_config_item("logger_level", 20)

    # Initialize Toolbox
    toolbox = Toolbox()

    # Start ModuleManager and check for modules
    module_manager_ = ModuleManager(config_, toolbox)
    module_manager_.initialize()
    print(module_manager_)

    # main(config_, module_manager_)
