from pathlib import Path
from node import Node


class Directory(Node):
    def __init__(self, path: Path, parent: Node | None, children=None):
        super().__init__(path, parent)
        if children is None:
            children = []
        self.children = children

    def check_for_children_directories(self) -> bool:
        for node in self.children:
            if isinstance(node, type(self)):
                return True
        return False
