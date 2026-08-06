import json
from models import InstanceDBEntry


class InstanceDBRecord:
    def __init__(self, instance_db_entry: InstanceDBEntry, instance_id: int):
        self.instance_db_entry = instance_db_entry
        self.instance_id = instance_id

    def get_as_json(self):
        result = json.dumps({
            "id": self.instance_id,
            "data": self.instance_db_entry.data,
            "meta": self.instance_db_entry.meta,
            "instance": "null"
        })
        result = result.replace('"null"', "null")
        return result
