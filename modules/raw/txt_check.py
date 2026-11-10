# Own imports
from lib.base_check import BaseCheck


class TXTCheck(BaseCheck):
    # def check(self, node: DocumentNode):
    def check(self, node):
        meta = dict()
        if node.path.suffix == ".txt":
            meta = {"module": "raw"}
            node.add_metadata(meta)
        return meta
