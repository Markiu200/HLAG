import json
from models import InstanceDBEntry, Ref


class InstanceDBRecord:
    def __init__(self, instance_db_entry: InstanceDBEntry, instance_id: int, ref: Ref):
        self.instance_db_entry = instance_db_entry
        self.instance_id = instance_id
        self.ref = ref

    def get_as_json(self):
        checked_data = ""
        if isinstance(self.instance_db_entry.data, str):
            checked_data = self.instance_db_entry.data
        elif isinstance(self.instance_db_entry.data, dict):
            checked_data = json.dumps(self.instance_db_entry.data)

        checked_meta = ""
        if isinstance(self.instance_db_entry.meta, str):
            checked_meta = self.instance_db_entry.meta
        elif isinstance(self.instance_db_entry.meta, dict):
            checked_meta = json.dumps(self.instance_db_entry.meta)

        result = "".join([
            '{"id": ', str(self.instance_id),
            ', "data": ', checked_data,
            ', "meta": ', checked_meta,
            ', "instance": null}'
        ])
        return result
