from pathlib import PurePath
# Own imports
from indent_tracker import IndentTracker


class JSManager:
    registered_js_files: set[PurePath] = set()
    registered_prints = []

    @classmethod
    def register_file(cls, path):
        JSManager.registered_js_files.add(path)

    @classmethod
    def register_other_print(cls, callback):
        cls.registered_prints.append(callback)

    @classmethod
    def print(cls):
        yield f"<script>\n"
        for file in JSManager.registered_js_files:
            with open(file) as f:
                for js_code in f:
                    yield js_code
        for other in cls.registered_prints:
            yield from other
        yield "</script>"
