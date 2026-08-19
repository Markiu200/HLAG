from pathlib import PurePath
from structure_scanner import StructureScanner, DocumentNode
from module_management import ModuleManager
from models import Card, InstanceDBEntry, Ref
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
        for node in cls.nodes:
            cls.current_node = node
            node_card = Card(
                node=node,
                file=True,
                meta=node.metadata,
                content=None
            )
            node.ref = cls.get_ref(node_card)

    @classmethod
    def get_ref(cls, card: Card) -> Ref:
        # Step 1 - check if we're dealing with a file
        if card.file:
            # Step 1.1 - read metadata from file using module that understands the file
            module = ModuleManager.get_module(card.meta.get("module"))
            got_meta = module.get_metadata(card)
            # Step 1.2 - Update card with that metadata
            for key, value in got_meta.items():
                card.meta[key] = value

        # Step 2 - get module from metadata
        module = ModuleManager.get_module(card.meta.get("module"))
        if not module:
            raise RuntimeError(f"Module \"{card.meta.get('module')}\" was requested, but such module was never registered.")

        # Step 3 - order instance record from the module
        instance_record = module.parse(card)

        # Step 4 - register that instance and fetch Ref record
        ref = cls.register_instance(instance_record, card)
        return ref

    @classmethod
    def register_instance(cls, instance_record: InstanceDBEntry, card: Card) -> Ref:
        report = ModuleTracker.add_record(instance_record)
        ref = report.ref
        register_method = report.module_file_register_method
        if register_method:
            cls.files_to_register.append(register_method)
            #
        card.node.all_refs.append(ref)
        #
        print(f"Instance of {ref.module} registered with ID: {ref.ref_id}")
        return ref

    @classmethod
    def get_instance_records(cls):
        groups = ModuleTracker.get_instance_db_record_groups()
        unpacked = []
        for group in groups:
            unpacked.extend([instance for instance in group.instance_list])
        return unpacked

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
