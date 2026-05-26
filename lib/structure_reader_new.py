import os
from pathlib import PurePath
# Own imports
from models.config import Config
from base_outline_manager import BaseOutlineManager


class StructureReader:
    prefix = 0

    @classmethod
    def set_prefix(cls, length):
        cls.prefix = length

    # def __init__(self, config: Config, outline_manager: BaseOutlineManager):
    #     self.config = config
    #     self.outline_manager = outline_manager

    def __init__(self):
        self.config = None
        self.outline_manager = None

    def set_config(self, config: Config):
        self.config = config

    def set_outline_manager(self, outline_manager: BaseOutlineManager):
        self.outline_manager = outline_manager

    def scan(self):
        self._scan(self.config.target_path)

    def _scan(self, full_path):
        for path, dirs, files in os.walk(full_path):
            for a_dir in dirs:
                current_full_path = PurePath(path, a_dir)
                self._for_outline(current_full_path)
            for a_file in files:
                current_full_path = PurePath(path, a_file)
                self._for_outline(current_full_path)

    def _for_outline(self, full_path: PurePath) -> None:
        if not full_path.name.startswith(("_", ".")):
            self.outline_manager.register(full_path)


if 'structure_reader' not in locals():
    structure_reader = StructureReader()
