# Own imports
if __name__ == '__main__':
    from sys import path as sys_path
    from pathlib import PurePath
    sys_path.append(str(PurePath(__file__).parent.parent))
from lib.instance_db_record import InstanceDBRecord
from lib.instance_db_record_group import InstanceDBRecordGroup
from lib.controller_map_record import ControllerMapRecord
from lib.models import InstanceDBEntry, Ref
from lib.module_manager import ModuleManager


class TrackedModule:
    def __init__(self, controller: str | None, module: str):
        self.module = module
        self.controller = controller
        self.next_id = 0
        self.instance_db_record_group: InstanceDBRecordGroup = InstanceDBRecordGroup(self.module)


class RecordReport:
    def __init__(self, ref: Ref | None = None, module_file_register_method=None):
        self.ref = ref
        self.module_file_register_method = module_file_register_method


class ModuleTracker:
    tracked_modules: dict[str, TrackedModule] = dict()
    module_manager: ModuleManager = None

    def __init__(self, module_manager: ModuleManager):
        self.module_manager = module_manager
        ModuleTracker.module_manager = self.module_manager

    @classmethod
    def add_record(cls, instance_entry: InstanceDBEntry) -> RecordReport:
        module = instance_entry.module
        tracked_module = cls.tracked_modules.get(module)
        if tracked_module:
            next_id = tracked_module.next_id
            ref = Ref(
                module=module,
                ref_id=next_id
            )
            instance_db_record = InstanceDBRecord(
                instance_db_entry=instance_entry,
                instance_id=tracked_module.next_id,
                ref=ref
            )
            tracked_module.instance_db_record_group.add_record(instance_db_record)
            tracked_module.next_id += 1
            return RecordReport(
                ref=ref
            )
        else:
            controller = cls.module_manager.get_registered_module(module).module_info.get("controller")
            #
            cls.tracked_modules[module] = TrackedModule(
                module=module,
                controller=controller
            )
            returned = cls.add_record(instance_entry)
            returned.module_file_register_method = cls.module_manager.get_registered_module(module).register_files
            return returned

    @classmethod
    def get_instance_db_record_groups(cls) -> list[InstanceDBRecordGroup]:
        results = []
        for module in cls.tracked_modules:
            results.append(cls.tracked_modules[module].instance_db_record_group)
        return results

    @classmethod
    def get_controller_map_records(cls) -> list[ControllerMapRecord]:
        results = []
        for module in cls.tracked_modules:
            controller = cls.tracked_modules[module].controller
            if controller:
                results.append(ControllerMapRecord(
                    module=module,
                    controller=controller
                ))
        return results
