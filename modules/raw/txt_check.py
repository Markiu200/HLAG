# Own imports
from lib.base_check import BaseCheck


class TXTCheck(BaseCheck):
    def __init__(self):
        super().__init__()
        self.priority = 5

    def check(self, node):
        meta = dict()
        if node.path.suffix == ".txt":
            meta = {"module": "raw"}
            node.add_metadata(meta)
        return meta
