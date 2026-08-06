from pathlib import PurePath


class JSManager:
    registered_prints = []

    @classmethod
    def append_print(cls, resource_type: str, resource):
        cls.registered_prints.append({
            "resource_type": resource_type,
            "resource": resource
        })

    @classmethod
    def register_file(cls, path: PurePath):
        cls.append_print("file", path)

    @classmethod
    def register_print(cls, callback):
        cls.append_print("callback", callback)

    @classmethod
    def print(cls):
        yield f"<script>\n"
        for element in cls.registered_prints:
            if element["resource_type"] == "file":
                with open(element["resource"]) as f:
                    for js_code in f:
                        yield js_code
            if element["resource_type"] == "callback":
                yield from element["resource"]
        yield "</script>\n"
