from pathlib import Path
from file import File
from node import Node


class MetaFile(File):
    def __init__(self, path: Path, parent: Node):
        super().__init__(path, parent)

    def get_title(self) -> str:
        """Reads first line and takes it as section title."""
        with open(self.path) as f:
            line = f.readline()
        return line
