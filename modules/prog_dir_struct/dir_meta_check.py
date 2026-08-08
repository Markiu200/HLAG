import os
# Own imports
from module_facade import BaseCheck, DocumentNode, ModuleFacade, Card


class DirMetaCheck(BaseCheck):
    def check(self, dir_node: DocumentNode):
        result = dict()
        if len(dir_node.children) > 0:
            for child in dir_node.children:
                if os.path.isfile(child.path):
                    if child.path.name == "_meta.txt" or child.path.name == "_metafile.txt":
                        card = Card(
                            node=child,
                            file=True,
                            meta=dict(),
                            content=None
                        )
                        got_meta = ModuleFacade.get_module("raw").get_metadata_from_file(card)
                        dir_node.add_metadata(got_meta)
        return result
