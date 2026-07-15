import re
import json
# Own imports
# from base_module.base_module import BaseModule
# from structure_scanner.document_tree.document_node import DocumentNode


class Text:
    def __init__(self, content: str, metadata: dict):
        self.content = content
        self.metadata = metadata

    def print(self):
        lines = []
        last_find = 0
        while True:
            search = re.search(r'JSREF\(.*?\)', self.content[last_find:])
            if not search:
                break
            lines.append(self.content[last_find:search.regs[0][0] - 1])
            lines.append(self.content[search.regs[0][0]:search.regs[0][1]])
            last_find = search.regs[0][1] + 1
        lines.append(self.content[last_find:])
        #
        result = {
            "module": "text",
            "content": lines,
            "metadata": "some_meta"
        }
        return result


if __name__ == "__main__":
    from pathlib import PurePath, Path
    import os
    from test import getpath
    pathp = Path(".")
    path = os.path.abspath(os.getcwd())
    print(getpath())
