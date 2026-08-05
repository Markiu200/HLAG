# Own imports
from module_facade import ModuleFacade, DocumentNode, Data, InstanceDBEntry
from module_management import IModule
from escaped_check import EscapedCheck
from dir_meta_check import DirMetaCheck


def get_module():
    return ProgDirStruct


class ProgDirStruct(IModule):
    @classmethod
    def get_info(cls) -> dict:
        return {
            "name": "prog_dir_struct",
            "priority": 1,
            "dependencies": []
        }

    @classmethod
    def register_checks(cls):
        ModuleFacade.register_initial_dir_check(EscapedCheck())
        ModuleFacade.register_check(EscapedCheck())
        ModuleFacade.register_final_dir_check(DirMetaCheck())

    @classmethod
    def register_files(cls):
        pass

    @classmethod
    def get_metadata_from_file(cls, node: DocumentNode) -> dict:
        return dict()

    @classmethod
    def get_metadata_from_data(cls, data: Data) -> dict:
        return dict()

    @classmethod
    def parse_file(cls, node: DocumentNode) -> InstanceDBEntry:
        return InstanceDBEntry("", None, None)

    @classmethod
    def parse_data(cls, data: Data) -> InstanceDBEntry:
        return InstanceDBEntry("", None, None)
