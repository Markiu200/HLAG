# Own imports
from module_facade import BaseCheck, DocumentNode, ModuleFacade, Card


class NavigationMetaCheck(BaseCheck):
    def check(self, node: DocumentNode):
        result = dict()
        if node.path == ModuleFacade.get_structure_scanner().root_directory:
            if node.metadata.get("navigation") == "pydocnavigation":
                ModuleFacade.get_content_manager().get_ref(Card(
                    node=node,
                    file=False,
                    meta={"module": "py_doc_navigation"},
                    content=None
                ))
        return result
