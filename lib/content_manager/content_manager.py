import json
from structure_scanner import StructureScanner, DocumentNode
from module_management import ModuleManager


class ContentManager:
    printable_elements_list: list[DocumentNode] = []
    used_modules: set[str] = set()
    module_map: dict = dict()
    saved_refs: dict = dict()  # refs beda jak {"nazwa": [str_refek]}
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
            jsref = cls.get_jsref_from_file(element)
            # element.references.append(jsref)

    @classmethod
    def get_jsref_from_file(cls, node: DocumentNode) -> str:  # zwraca JSREF
        # Get current module from metadata
        module = ModuleManager.get_module(node.metadata.get("module"))
        # Read the metadata using current Module meta-fetcher
        found_meta = module.read_metadata_from_file(node)
        # Update metadata
        node.add_metadata(found_meta)
        # See what module it is after all and register that module as used
        module = ModuleManager.get_module(node.metadata.get("module"))
        # Invoke that Module parse method and save it's jscard
        # # if parser encounter reference, it asks this class to get reference (get_reference_from_data)
        jscard = module.parse_from_file(node)
        # Having file finally parsed, generate and return jsref
        jsref = cls.register_instance(jscard)
        return jsref

    @classmethod
    def get_jsref_from_data(cls, data: dict) -> str:
        module = ModuleManager.get_module(data.get("module"))
        if not module:
            raise RuntimeError(f"Module {data.get('module')} has been referenced but no such module is found.")
        found_meta = module.read_metadata_from_string(data.get("content"))
        jscard = module.parse_from_string(data.get("content"), found_meta)
        jsref = cls.register_instance(jscard)
        return jsref

    @classmethod
    def register_instance(cls, data: dict) -> str:  # zwraca JSREF
        # saved_refs = {module: {id:int, refs:list}}
        module = data.get("module")
        #
        if module not in cls.used_modules:  # not cls.saved_refs_ids.get(module):
            cls.saved_refs_ids[module] = -1
            cls.saved_refs[module] = []
            cls.used_modules.add(module)
            ModuleManager.get_module(module).register_files()
        new_module_id = cls.saved_refs_ids[module] + 1
        cls.saved_refs_ids[module] = new_module_id
        #
        jsref = f"[%JSREF({module},{new_module_id})%]"
        refdata = {
            "id": new_module_id,
            "data": data["data"],
            "meta": data["meta"]
        }
        cls.saved_refs[module].append(refdata)
        #
        ref = {
            "module": module,
            "id": new_module_id,
        }
        cls.current_node.all_refs.append(ref)
        # with this order, last ref will be file's own ref.
        cls.current_node.ref = ref
        #
        print(f"Instance of {module} registered, count {new_module_id}: {refdata}")
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
        yield "".join(["let registered_modules = ", json.dumps(cls.saved_refs), ";"])
        yield "\n"
        yield "".join(["let moduleMap = ", cls.generate_module_map()])
