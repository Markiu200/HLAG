# Own imports
from lib.module_facade import BaseCheck, DocumentNode


class NavSeparatorCheck(BaseCheck):
    def check(self, node: DocumentNode):
        if node.metadata.get("nav-separator"):
            node.add_attribute("escaped")
        return "nav-separator"
