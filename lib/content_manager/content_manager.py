import json
from structure_scanner import StructureScanner, DocumentNode
from module_management import ModuleManager
from models import Card, Ref, InstanceDBEntry


class ContentManager:
    printable_elements_list: list[DocumentNode] = []
    used_modules: set[str] = set()
    module_map: dict = dict()
    instance_db_records: dict = dict()  # refs beda jak {"nazwa": [str_refek]}
    saved_refs_ids: dict = dict()
    current_node: DocumentNode

    @classmethod
    def fetch_content_from_scanner(cls):
        for node in StructureScanner.tree:
            if node.metadata.get("module") and not node.has_attribute("escaped"):
                cls.printable_elements_list.append(node)

    @classmethod
    def parse_files(cls):
        for element in cls.printable_elements_list:
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
    def register_instance(cls, instance_entry: InstanceDBEntry) -> str:  # zwraca JSREF
        # saved_refs = {module: {id:int, refs:list}}
        module = instance_entry.module
        #
        if module not in cls.used_modules:  # not cls.saved_refs_ids.get(module):
            cls.saved_refs_ids[module] = -1
            cls.instance_db_records[module] = []
            cls.used_modules.add(module)
            ModuleManager.get_module(module).register_files()
        new_module_id = cls.saved_refs_ids[module] + 1
        cls.saved_refs_ids[module] = new_module_id
        #
        jsref = f"[%JSREF({module},{new_module_id})%]"
        instance_db_record = {
            "id": new_module_id,
            "data": instance_entry.data,
            "meta": instance_entry.meta
        }
        cls.instance_db_records[module].append(instance_db_record)
        #
        ref = Ref(
            module=module,
            ref_id=new_module_id
        )
        cls.current_node.all_refs.append(ref)
        # with this order, last ref will be file's own ref.
        cls.current_node.ref = ref
        #
        print(f"Instance of {module} registered, count {new_module_id}: {ref.module}")
        return jsref

    #
    #   PRINTING RELATED METHODS
    #

    @classmethod
    def generate_module_map(cls) -> str:
        res = "["
        for used_module in cls.used_modules:
            jsmanager = ModuleManager.get_module(used_module).get_info().get("jsmanager")
            if jsmanager:
                res = "".join([res, "{", f' "name": "{used_module}", "manager": {jsmanager} ', "},"])
        res = "".join([res, "];"])
        return res

    @classmethod
    def print_html_container(cls):
        yield '<main id="main"></main>'

    @classmethod
    def print(cls):
        yield "".join(["let registered_modules = ", json.dumps(cls.instance_db_records), ";"])
        yield "\n"
        yield "".join(["let moduleMap = ", cls.generate_module_map()])
