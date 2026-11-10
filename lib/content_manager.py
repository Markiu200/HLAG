from pathlib import PurePath
# Own imports
if __name__ == '__main__':
    from sys import path as sys_path
    sys_path.append(str(PurePath(__file__).parent.parent))
from lib.document_node import DocumentNode
from lib.models import Ref
# from lib.structure_scanner import StructureScanner, DocumentNode
# from lib.models import Card, InstanceDBEntry, Ref
# from module_manager import ModuleManager
# from lib.module_tracker import ModuleTracker


class ContentManager:
    # from lib.module_manager import Module

    def __init__(self, pm_modules: dict):
        self.nodes: list[DocumentNode] = []
        self.current_node: DocumentNode | None = None  # DocumentNode that is currently being parsed
        self.encountered_modules = set()
        self.tracked_modules_count = dict()
        self.records = []
        self.pm_modules: dict[str, Module] = pm_modules  # dict of all modules found by module manager

    def run(self, root: DocumentNode):
        for node in root:
            if node.metadata.get("module") and not node.has_attribute("escaped"):
                self.nodes.append(node)
        self._parse(self.nodes)

    def _parse(self, nodes: list[DocumentNode]):
        for node in nodes:
            self.current_node = node

            # Step 1 - check if we're dealing with a file
            if node.is_file:
                # Step 1.1 - read metadata from file using module that understands the file
                module = self.pm_modules.get(node.metadata.get("module"))
                got_meta = module.module_instance.get_metadata(node.path, is_file=True)
                # Step 1.2 - Update card with that metadata
                for key, value in got_meta.items():
                    node.metadata[key] = value

            # Step 2 - get module from metadata
            module = self.pm_modules.get(node.metadata.get("module"))
            if not module:
                raise RuntimeError(
                    f"Module \"{node.metadata.get('module')}\" was requested, but such module was never registered.")
            self.encountered_modules.add(module)

            # Step 3 - parse file by pm module
            pm_module_result = module.module_instance.parse(node.path, node.metadata, is_file=True)
            print(pm_module_result)

            # Step 4 - register that instance and fetch Ref record
            instance_no = self.register_record(module)
            ref = Ref(module=module.codename, ref_id=instance_no)
            node.ref = ref
            # Record: {pm_module, id, data, meta}; "Instance" added in separate method.
            self.records.append(
                {
                    "module": module.codename,
                    "id": instance_no,
                    "data": pm_module_result,
                    "meta": self.current_node.metadata
                }
            )

    def nest_ref(self, module_: str, content, metadata: dict) -> Ref:  # Meant to be called by pm_modules themselves
        # Step 1 - get module
        module = self.pm_modules.get(module_)
        if not module:
            raise RuntimeError(
                f"Module \"{module}\" was requested, but such module was never registered.")
        self.encountered_modules.add(module)

        # Step 2 - parse file by pm module
        pm_module_result = module.module_instance.parse(content, metadata, is_file=False)
        print(pm_module_result)

        # Step 3 - register that instance and fetch Ref record
        instance_no = self.register_record(module_)
        ref = Ref(module=module_, ref_id=instance_no)
        self.current_node.nested_refs.append(ref)
        # Record: {pm_module, id, data, meta}; "Instance" added in separate method.
        self.records.append(
            {
                "module": module.codename,
                "id": instance_no,
                "data": pm_module_result,
                "meta": self.current_node.metadata
            }
        )
        #
        return ref

    def register_record(self, module) -> int:
        if module not in self.tracked_modules_count:
            self.tracked_modules_count[module] = -1
        self.tracked_modules_count[module] += 1
        return self.tracked_modules_count[module]

    def get_records(self) -> list:
        return self.records

    #
    #
    #
    #
    # nodes: list[DocumentNode] = []
    # files_to_register = []
    # current_node: DocumentNode
    #
    # @classmethod
    # def fetch_content_from_scanner(cls):
    #     for node in StructureScanner.tree:
    #         if node.metadata.get("module") and not node.has_attribute("escaped"):
    #             cls.nodes.append(node)
    #
    # @classmethod
    # def parse_files(cls):
    #     for node in cls.nodes:
    #         cls.current_node = node
    #         node_card = Card(
    #             node=node,
    #             file=True,
    #             meta=node.metadata,
    #             content=None
    #         )
    #         node.ref = cls.get_ref(node_card)
    #
    # @classmethod
    # def get_ref(cls, card: Card) -> Ref:
    #     # Step 1 - check if we're dealing with a file
    #     if card.file:
    #         # Step 1.1 - read metadata from file using module that understands the file
    #         module = ModuleManager.get_module(card.meta.get("module"))
    #         got_meta = module.get_metadata(card)
    #         # Step 1.2 - Update card with that metadata
    #         for key, value in got_meta.items():
    #             card.meta[key] = value
    #
    #     # Step 2 - get module from metadata
    #     module = ModuleManager.get_module(card.meta.get("module"))
    #     if not module:
    #         raise RuntimeError(f"Module \"{card.meta.get('module')}\" was requested, but such module was never registered.")
    #
    #     # Step 3 - order instance record from the module
    #     instance_record = module.parse(card)
    #
    #     # Step 4 - register that instance and fetch Ref record
    #     ref = cls.register_instance(instance_record, card)
    #     return ref
    #
    # @classmethod
    # def register_instance(cls, instance_record: InstanceDBEntry, card: Card) -> Ref:
    #     report = ModuleTracker.add_record(instance_record)
    #     ref = report.ref
    #     register_method = report.module_file_register_method
    #     if register_method:
    #         cls.files_to_register.append(register_method)
    #         #
    #     card.node.all_refs.append(ref)
    #     #
    #     print(f"Instance of {ref.module} registered with ID: {ref.ref_id}")
    #     return ref
    #
    # @classmethod
    # def get_instance_records(cls):
    #     groups = ModuleTracker.get_instance_db_record_groups()
    #     unpacked = []
    #     for group in groups:
    #         unpacked.extend([instance for instance in group.instance_list])
    #     return unpacked

    #
    #   PRINTING RELATED METHODS
    #

    # @classmethod
    # def print_html(cls):
    #     yield '    <main id="main"></main>\n'
    #
    # @classmethod
    # def queue_module_printing(cls):
    #     for register in cls.files_to_register:
    #         register()
    #
    # @classmethod
    # def print_instance_db(cls, beginning: str):
    #     indented_beginning = "".join(["  ", beginning])
    #     yield f"{beginning}static instanceDB = new Map([\n"
    #     #
    #     instance_db_record_groups = ModuleTracker.get_instance_db_record_groups()
    #     for i, instance_db_record_group in enumerate(instance_db_record_groups):
    #         if i < len(instance_db_record_groups) - 1:
    #             for line in instance_db_record_group.yield_as_js_map_entry():
    #                 yield f"{indented_beginning}  {line}"
    #             yield ",\n"
    #         else:
    #             for line in instance_db_record_group.yield_as_js_map_entry():
    #                 yield f"{indented_beginning}  {line}"
    #             yield "\n"
    #     yield f"{beginning}]);"
    #
    # @classmethod
    # def print_controller_map(cls, beginning: str):
    #     indented_beginning = "".join(["  ", beginning])
    #     yield f"{beginning}static controllerMap = new Map([\n"
    #     #
    #     controller_map_records = ModuleTracker.get_controller_map_records()
    #     for i, controller_record in enumerate(controller_map_records):
    #         if i < len(controller_map_records) - 1:
    #             yield f"{indented_beginning}{controller_record.get_as_js_controller_map_record()},\n"
    #         else:
    #             yield f"{indented_beginning}{controller_record.get_as_js_controller_map_record()}\n"
    #     yield f"{beginning}]);"
    #
    # @classmethod
    # def print_js(cls):
    #     with open(PurePath(PurePath(__file__).parent, r"snippets/js_content_manager.js")) as f:
    #         lines = f.readlines()
    #         for line in lines:
    #             if "//PLACEHOLDER_FOR_INSTANCEDB" in line:
    #                 parts = line.split("//PLACEHOLDER_FOR_INSTANCEDB")
    #                 yield from cls.print_instance_db(parts[0])
    #             elif "//PLACEHOLDER_FOR_CONTROLLERMAP" in line:
    #                 parts = line.split("//PLACEHOLDER_FOR_CONTROLLERMAP")
    #                 yield from cls.print_controller_map(parts[0])
    #             else:
    #                 yield line


__all__ = [ContentManager]

if __name__ == '__main__':
    # Initialize dummy modules
    from lib.dummy_pm_module import DummyPMModue
    pm_module_a = DummyPMModue("moda")
    pm_module_b = DummyPMModue("modb")

    # Initialize dummy module dictionary
    from lib.module_manager import Module
    module_a = Module(
        module_class=type(Module),
        module_instance=pm_module_a,
        codename="moda",
        module_info={
            "codename": "moda",
            "priority": 1,
            "controller": "ModAController"
        }
    )
    module_b = Module(
        module_class=type(Module),
        module_instance=pm_module_b,
        codename="modb",
        module_info={
            "codename": "modb",
            "priority": 1,
            "controller": "ModBController"
        }
    )
    modules_dict = {
        "moda": module_a,
        "modb": module_b
    }

    # Initialize dummy nodes
    DocumentNode.root_path = PurePath(__file__).parent
    node_a = DocumentNode(PurePath(__file__), is_file=True)
    node_a.metadata["module"] = "moda"
    node_b = DocumentNode(PurePath(__file__), is_file=False)
    node_b.metadata["module"] = "modb"

    # Initialize ContentManager
    content_manager = ContentManager(modules_dict)

    # Test parsing
    content_manager._parse([node_a, node_a])
    content_manager.nest_ref("modb", "content", node_b.metadata)
    content_manager.nest_ref("modb", "content", node_b.metadata)
    content_manager.nest_ref("modb", "content", node_b.metadata)

    # Internally saved records
    print(content_manager.records)
