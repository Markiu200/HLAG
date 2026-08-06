from content_manager.structures import InstanceDBRecord


class InstanceDBRecordGroup:
    def __init__(self, module: str):
        self.module = module
        self.instance_list: list[InstanceDBRecord] = []

    def add_record(self, instance_db_record: InstanceDBRecord):
        self.instance_list.append(instance_db_record)

    def yield_as_js_map_entry(self):
        yield f'["{self.module}", [\n'
        for instance in self.instance_list:
            yield f"  {instance.get_as_json()},\n"
        yield ']]'
