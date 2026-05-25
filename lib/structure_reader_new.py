import os
# Own imports
from models.config import Config
from lib.base_outline_manager import BaseOutlineManager


class StructureReader:
    def __init__(self, config: Config, outline_manager: BaseOutlineManager):
        self.config = config
        self.omanager = outline_manager

    def scan(self) -> None:
        for path, dirs, files in os.walk(self.config.target_path):
            for a_dir in dirs:
                if (not a_dir.startswith(".") and not a_dir.startswith("_")) \
                        or a_dir == "_dict":
                    self.omanager.register(path, a_dir)
            for file in files:
                if not file.startswith(".") and not file.startswith("_"):
                    self.omanager.register(path, file)
