import os
from pathlib import PurePath
# Own imports
from config import config
from base_outline_manager import BaseOutlineManager


class StructureReader:
    def __init__(self, outline_manager: BaseOutlineManager = None):
        self.outline_manager = None

    def set_outline_manager(self, outline_manager: BaseOutlineManager):
        self.outline_manager = outline_manager

    def scan(self):
        self._scan(config.target_path)

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
