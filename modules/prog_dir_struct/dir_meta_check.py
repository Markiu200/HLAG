import os
# Own imports
from module_facade import BaseCheck, DocumentNode, ModuleFacade


class DirMetaCheck(BaseCheck):
    def check(self, dir_node: DocumentNode):
        result = dict()
        if len(dir_node.children) > 0:
            for child in dir_node.children:
                if os.path.isfile(child.path):
                    if child.path.name == "_meta.txt" or child.path.name == "_metafile.txt":
                        got_meta = ModuleFacade.get_module("text").read_metadata_from_file(child)
                        dir_node.add_metadata(got_meta)
        return result
