# Own imports
from module_facade import BaseCheck, DocumentNode


class DirectoryCheck(BaseCheck):
    def check(self, node: DocumentNode):
        node.add_attribute("directory")
        return "directory"
