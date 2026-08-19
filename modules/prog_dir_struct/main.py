from importlib import import_module
#
from module_facade import ModuleFacade, Card, InstanceDBEntry
from module_management import IModule


def get_module_main_class():
    return ProgDirStruct


class ProgDirStruct(IModule):
    escaped_check = import_module(f"prog_dir_struct.escaped_check")
    dir_meta_check = import_module(f"prog_dir_struct.dir_meta_check")
    directory_check = import_module(f"prog_dir_struct.directory_check")

    @classmethod
    def get_info(cls) -> dict:
        return {
            "name": "prog_dir_struct",
            "priority": 10,
            "dependencies": []
        }

    @classmethod
    def register_checks(cls):
        ModuleFacade.register_initial_dir_check(cls.escaped_check.EscapedCheck())
        ModuleFacade.register_initial_dir_check(cls.directory_check.DirectoryCheck())
        ModuleFacade.register_check(cls.escaped_check.EscapedCheck())
        ModuleFacade.register_final_dir_check(cls.dir_meta_check.DirMetaCheck())

    @classmethod
    def register_files(cls):
        pass

    @classmethod
    def get_metadata_from_file(cls, card: Card) -> dict:
        return dict()

    @classmethod
    def get_metadata_from_data(cls, card: Card) -> dict:
        return dict()

    @classmethod
    def parse_file(cls, card: Card) -> InstanceDBEntry:
        return InstanceDBEntry("", None, None)

    @classmethod
    def parse_data(cls, card: Card) -> InstanceDBEntry:
        return InstanceDBEntry("", None, None)
