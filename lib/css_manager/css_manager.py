from pathlib import PurePath


class CSSManager:
    registered_css_files: set[PurePath] = set()

    @classmethod
    def register(cls, path):
        CSSManager.registered_css_files.add(path)

    @classmethod
    def print(cls):
        yield f"<style>\n"
        for file in CSSManager.registered_css_files:
            with open(file) as f:
                for css_code in f:
                    yield css_code
        yield "</style>"
