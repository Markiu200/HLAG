# Own imports
from module_facade import BaseCheck, DocumentNode


class TXTCheck(BaseCheck):
    def check(self, node: DocumentNode):
        meta = dict()
        if node.path.suffix == ".txt":
            meta = {"module": "text"}
            node.add_metadata(meta)
        return meta
