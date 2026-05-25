from pathlib import Path


class Node:
    def __init__(self, path: Path, parent=None):
        self.path = path
        self.parent = parent
