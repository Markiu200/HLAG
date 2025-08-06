from pathlib import Path
from node import Node


class Directory(Node):
    def __init__(self, path: Path, parent: Node | None, children=None):
        super().__init__(path, parent)
        if children is None:
            children = []
        self.children = children
