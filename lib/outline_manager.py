from pathlib import PurePath
from os import sep as system_separator
import logging
# Own imports
from models.config import Config
from outline_node import OutlineNode
from base_outline_manager import BaseOutlineManager

logger = logging.getLogger(__name__)


class OutlineManager(BaseOutlineManager):
    def __init__(self, config: Config):
        self.config = config
        self.node_count = 0
        self.registered_nodes = []
        self.abs_dir_prefix_length = len(config.target_path.parts)
        # Create root
        self.root = OutlineNode(
            rel_path=PurePath(system_separator),
            abs_path=self.config.target_path,
            filename="root"
        )

    def register(self, path, filename):
        rel_path = PurePath(*PurePath(path).parts[self.abs_dir_prefix_length:])
        if rel_path not in self.registered_nodes:
            new_node = OutlineNode(
                rel_path=rel_path,
                abs_path=PurePath(path, filename),
                filename=filename
            )
            print(new_node.rel_path, new_node.abs_path, new_node.filename, new_node.dom_id)

            self.registered_nodes.append(rel_path)

        # print("Registered:", PurePath(path, filename))
        #
        # path = PurePath(path, filename)
        # if path not in self.registered_nodes:
        #     if Path(path).is_dir():
        #         self.register_directory(path)
        #
        #     if Path(path).is_file():
        #         self.register_file(path)

        # File(
        #             path=path,
        #             rel_path=PurePath(*path.parts[self.prefix_length:]),
        #             parent=self.root
        #         )
