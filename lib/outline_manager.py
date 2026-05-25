from pathlib import PurePath, Path
import logging
# Own imports
from models.config import Config
from filetypes import Node, File, Directory, RootNode
from outline_node import OutlineNode
from outline_element import OutlineElement
from base_outline_manager import BaseOutlineManager

logger = logging.getLogger(__name__)


class OutlineManager(BaseOutlineManager):
    def __init__(self, config: Config):
        self.config = config
        self.node_count = 0
        self.registered_nodes = {}
        self.abs_dir_prefix_length = len(config.target_path.parts)
        # Create root
        self.root = OutlineNode(

        )

    def register(self, path, filename):
        print("Registered:", PurePath(path, filename))

        path = PurePath(path, filename)
        if path not in self.registered_nodes:
            if Path(path).is_dir():
                self.register_directory(path)

            if Path(path).is_file():
                self.register_file(path)

    def register_directory(self, path):
        pass
        # todo check if parent directory is added to outline already

        # todo if not, create it

        # todo finally, create new node and append to parent's children
        # new_dir = Directory(
        #     rel_path=path
        # )

    def register_file(self, path):
        self.root.add_child(path)
        self.internal_register_node(
            File(
                path=path,
                rel_path=PurePath(*path.parts[self.prefix_length:]),
                parent=self.root
            )
        )

    def internal_register_node(self, node: Node):
        self.registered_nodes[node.path] = {
            "rel_path": node.rel_path,
            "is_dir": isinstance(node, Directory),
            "node": node
        }
