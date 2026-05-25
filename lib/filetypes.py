from abc import ABC, abstractmethod
from pathlib import PurePath
import logging
# Own imports
from base_generator import BaseGenerator
from dummy_generator import DummyGenerator

logger = logging.getLogger(__name__)


class Node(ABC):
    def __init__(self, path: PurePath, rel_path: PurePath, parent):
        self.path = path
        self.rel_path = rel_path
        self.parent = parent

    @abstractmethod
    def generate(self) -> str:
        pass


class RootNode(Node):
    def __init__(self):
        super().__init__(PurePath("."), PurePath("."), None)

    def generate(self) -> str:
        return DummyGenerator().generate()


class Directory(Node):
    def __init__(self, path: PurePath, rel_path: PurePath, parent: Node):
        super().__init__(path, rel_path, parent)
        self.children = []
        self.generator = None

    def generate(self) -> str:
        if self.generator in None:
            self.generator = DummyGenerator()
            logger.warning(f"Dummy generator set when calling generate() for {self.path}")
        return self.generator.generate()

    def add_child(self, child: Node):
        """Append new child to this directory node.

        Positional arguments:
              child: Node   - child node to append
        """
        self.children.append(child)

    def set_generator(self, generator: BaseGenerator):
        self.generator = generator


class File(Node):
    def __init__(self, path: PurePath, rel_path: PurePath, parent: Node):
        super().__init__(path, rel_path, parent)
        self.generator = None

    def generate(self) -> str:
        if self.generator in None:
            self.generator = DummyGenerator()
            logger.warning(f"Dummy generator set when calling generate() for {self.path}")
        return self.generator.generate()

    def set_generator(self, generator: BaseGenerator):
        self.generator = generator
