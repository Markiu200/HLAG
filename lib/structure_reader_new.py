import os
from itertools import chain
# Own imports
from models.config import Config
from lib.base_outline_manager import BaseOutlineManager


class StructureReader:
    def __init__(self, config: Config, outline_manager: BaseOutlineManager):
        self.config = config
        self.outline_manager = outline_manager

    def scan(self):
        self.scan_for_outline()

    def scan_for_outline(self) -> None:
        for path, dirs, files in os.walk(self.config.target_path):
            pass
            # for name in dirs:
            #     if not name.startswith(".") and not name.startswith("_"):
            #         self.outline_manager.register(path, name)
            # for name in files:
            #     if not name.startswith(".") and not name.startswith("_"):
            #         self.outline_manager.register(path, name)