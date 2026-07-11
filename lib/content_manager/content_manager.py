import json


class ContentManager:
    count = 0

    @classmethod
    def register_instance(cls, data) -> str:
        table_data = [data["module"], cls.count, data["content"], data["metadata"]]
        ref_data = [data["module"], cls.count, data["metadata"]]
        cls.count += 1
        json_table_data = json.dumps(table_data)
        json_ref_data = json.dumps(ref_data)
        print(f"Instance registered, count {cls.count}: {json_table_data}")
        return f"[%JSREF({json_ref_data})%]"
