from pathlib import Path
from node import Node


class File(Node):
    def __init__(self, path: Path, parent: Node):
        super().__init__(path, parent)
