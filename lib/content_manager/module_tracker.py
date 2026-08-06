from content_manager.structures import InstanceDBRecord, InstanceDBRecordGroup, ControllerMapRecord
from models import InstanceDBEntry, Ref
from module_management import ModuleManager


class TrackedModule:
    def __init__(self, controller: str | None, module: str):
        self.module = module
        self.controller = controller
        self.next_id = 0
        self.instance_db_record_group: InstanceDBRecordGroup = InstanceDBRecordGroup(self.module)


class ModuleTracker:
    tracked_modules: dict[str, TrackedModule] = dict()

    @classmethod
    def add_record(cls, instance_entry: InstanceDBEntry) -> (Ref, object):
        module = instance_entry.module
        tracked_module = cls.tracked_modules.get(module)
        if tracked_module:
            instance_db_record = InstanceDBRecord(
                instance_db_entry=instance_entry,
                instance_id=tracked_module.next_id
            )
            tracked_module.instance_db_record_group.add_record(instance_db_record)
            tracked_module.next_id += 1
            return (
                Ref(
                    module=module,
                    ref_id=instance_db_record.instance_id
                ),
                None
            )
        else:
            controller = ModuleManager.get_module(module).get_info().get("controller")
            #
            cls.tracked_modules[module] = TrackedModule(
                module=module,
                controller=controller
            )
            returned = cls.add_record(instance_entry)
            return (
                returned[0],
                ModuleManager.get_module(module).register_files
            )

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
