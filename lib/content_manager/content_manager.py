import json
from structure_scanner import StructureScanner, DocumentNode
from module_manager import ModuleManager


class ContentManager:
    printable_elements_list: list[DocumentNode] = []
    used_modules: set[str] = set()
    module_map: dict = dict()
    saved_refs: dict = dict()  # refs beda jak {"nazwa": [str_refek]}
    saved_refs_ids: dict = dict()

    @classmethod
    def fetch_content_from_scanner(cls):
        for node in StructureScanner.tree:
            if node.metadata.get("module") and not node.has_attribute("escaped"):
                cls.printable_elements_list.append(node)

    @classmethod
    def parse_files(cls):
        for element in cls.printable_elements_list:
            jsref = cls.get_reference_from_file(element)
            element.references.append(jsref)

    @classmethod
    def get_reference_from_file(cls, node: DocumentNode) -> str:  # zwraca JSREF
        # todo get current module from metadata
        module = ModuleManager.get_module(node.metadata.get("module"))
        # todo then read the metadata using current Module meta-fetcher
        found_meta = module.read_metadata_from_file(node)
        # todo then update metadata
        node.add_metadata(found_meta)
        # todo then see what module it is after all
        # todo then register that module as used
        module = ModuleManager.get_module(node.metadata.get("module"))
        # todo then append metadata read to the metadata
        # assuming for now that it's been done via meta update above
        # todo then invoke current Module parse along with DocumentNode
        # todo then save the returned object (to be JSREFed at print)
        # # todo if parser encounter reference, it asks this method for reference (passes the object)
        jsref_dict = module.parse_from_file(node)
        jsref = cls.register_instance(jsref_dict)
        return jsref

    @classmethod
    def get_reference_from_data(cls, data: dict) -> str:
        module = ModuleManager.get_module(data.get("module"))
        if not module:
            raise RuntimeError(f"Module {data.get('module')} has been referenced but no such module is found.")
        found_meta = module.read_metadata_from_string(data.get("content"))
        jsref_dict = module.parse_from_string(data.get("content"), found_meta)
        jsref = cls.register_instance(jsref_dict)
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
        ref = {
            "id": new_module_id,
            "data": data["data"],
            "meta": data["meta"]
        }
        cls.saved_refs[module].append(ref)
        #
        print(f"Instance of {module} registered, count {new_module_id}: {ref}")
        return jsref

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
