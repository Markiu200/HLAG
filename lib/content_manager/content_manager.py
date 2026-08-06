from pathlib import PurePath
from structure_scanner import StructureScanner, DocumentNode
from module_management import ModuleManager
from models import Card, InstanceDBEntry
from .module_tracker import ModuleTracker


class ContentManager:
    nodes: list[DocumentNode] = []
    files_to_register = []
    current_node: DocumentNode

    @classmethod
    def fetch_content_from_scanner(cls):
        for node in StructureScanner.tree:
            if node.metadata.get("module") and not node.has_attribute("escaped"):
                cls.nodes.append(node)

    @classmethod
    def parse_files(cls):
        for element in cls.nodes:
            cls.current_node = element
            cls.get_jsref_from_file(element)

    @classmethod
    def get_jsref_from_file(cls, node: DocumentNode) -> str:
        # Get current module from metadata, then using it read metadata in file
        module = ModuleManager.get_module(node.metadata.get("module"))
        found_meta = module.get_metadata_from_file(node)
        # Update metadata and then fetch module again to see if it changed
        node.add_metadata(found_meta)
        module = ModuleManager.get_module(node.metadata.get("module"))
        # Get jscard from using module's method
        instance_entry = module.parse_file(node)
        # Having file finally parsed, generate, register and return jsref
        jsref = cls.register_instance(instance_entry)
        return jsref

    @classmethod
    def get_jsref_from_card(cls, card: Card) -> str:
        module = ModuleManager.get_module(card.module)
        instance_entry = module.parse_data(card.data)
        jsref = cls.register_instance(instance_entry)
        return jsref

    @classmethod
    def register_instance(cls, instance_entry: InstanceDBEntry) -> str:
        res = ModuleTracker.add_record(instance_entry)
        ref = res[0]
        register = res[1]
        if register:
            cls.files_to_register.append(register)
        #
        jsref = f"[%JSREF({ref.module},{ref.ref_id})%]"
        #
        cls.current_node.all_refs.append(ref)
        cls.current_node.ref = ref  # with this order, last ref will be file's own ref.
        #
        print(f"Instance of {ref.module} registered with ID: {ref.ref_id}")
        return jsref

    #
    #   PRINTING RELATED METHODS
    #

    @classmethod
    def print_html(cls):
        yield '    <main id="main"></main>\n'

    @classmethod
    def queue_module_printing(cls):
        for register in cls.files_to_register:
            register()

    @classmethod
    def print_instance_db(cls, beginning: str):
        indented_beginning = "".join(["  ", beginning])
        yield f"{beginning}static instanceDB = new Map([\n"
        #
        instance_db_record_groups = ModuleTracker.get_instance_db_record_groups()
        for i, instance_db_record_group in enumerate(instance_db_record_groups):
            if i < len(instance_db_record_groups) - 1:
                for line in instance_db_record_group.yield_as_js_map_entry():
                    yield f"{indented_beginning}  {line}"
                yield ",\n"
            else:
                for line in instance_db_record_group.yield_as_js_map_entry():
                    yield f"{indented_beginning}  {line}"
                yield "\n"
        yield f"{beginning}]);"

    @classmethod
    def print_controller_map(cls, beginning: str):
        indented_beginning = "".join(["  ", beginning])
        yield f"{beginning}static controllerMap = new Map([\n"
        #
        controller_map_records = ModuleTracker.get_controller_map_records()
        for i, controller_record in enumerate(controller_map_records):
            if i < len(controller_map_records) - 1:
                yield f"{indented_beginning}{controller_record.get_as_js_controller_map_record()},\n"
            else:
                yield f"{indented_beginning}{controller_record.get_as_js_controller_map_record()}\n"
        yield f"{beginning}]);"

    @classmethod
    def print_js(cls):
        with open(PurePath(PurePath(__file__).parent, r"content_manager.js")) as f:
            lines = f.readlines()
            for line in lines:
                if "//PLACEHOLDER_FOR_INSTANCEDB" in line:
                    parts = line.split("//PLACEHOLDER_FOR_INSTANCEDB")
                    yield from cls.print_instance_db(parts[0])
                elif "//PLACEHOLDER_FOR_CONTROLLERMAP" in line:
                    parts = line.split("//PLACEHOLDER_FOR_CONTROLLERMAP")
                    yield from cls.print_controller_map(parts[0])
                else:
                    yield line
