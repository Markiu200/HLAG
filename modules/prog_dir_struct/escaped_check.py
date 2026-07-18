# Own imports
from module_facade import BaseCheck, DocumentNode


class EscapedCheck(BaseCheck):
    def check(self, node: DocumentNode):
        if node.path.name.startswith("_"):
            node.add_attribute("escaped")
        if node.parent and node.parent.has_attribute("escaped"):
            node.add_attribute("escaped")
        return "escaped"
