# Own imports
from models.config import config
from outline_node import OutlineNode
from base_outline_manager import BaseOutlineManager


class OutlineManager(BaseOutlineManager):
    def __init__(self):
        # create root
        self.root = OutlineNode(
            full_path=config.target_path
        )

    def register(self, full_path):
        if full_path == config.target_path:
            parent = self.root
        else:
            parent = self.root.get_node_by_full_path(OutlineNode.get_potential_parent(full_path))
        if parent is not None:
            new_node = OutlineNode(
                full_path=full_path
            )
            parent.add_child(new_node)
