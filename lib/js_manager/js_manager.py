from pathlib import PurePath
# Own imports
from indent_tracker import IndentTracker


class JSManager:
    registered_js_files: set[PurePath] = set()

    @classmethod
    def register(cls, path):
        JSManager.registered_js_files.add(path)

    @classmethod
    def print(cls):
        yield f"<script>\n"
        for file in JSManager.registered_js_files:
            with open(file) as f:
                for js_code in f:
                    yield js_code
        yield "</script>"
