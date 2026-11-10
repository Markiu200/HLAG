# Own imports
if __name__ == '__main__':
    from sys import path as sys_path
    from pathlib import PurePath
    sys_path.append(str(PurePath(__file__).parent.parent))
from lib.base_check import BaseCheck


class DummyCheck(BaseCheck):
    def __init__(self):
        self.codename = "mod"

    def set_codename(self, codename: str):
        self.codename = codename

    def check(self, node):
        meta = dict()
        if node.path.suffix == f".{self.codename}":
            meta = {"module": self.codename}
            node.add_metadata(meta)
        return meta
