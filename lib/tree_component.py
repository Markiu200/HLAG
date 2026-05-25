from abc import ABC
# Own imports
from tree_node import TreeNode
from tree import Tree


class TreeComponent:
    ### implementable by both Tree and TreeNode:
    def walk(self):
        raise NotImplementedError(f"Component of type {type(self)} does not implement that operation")

    def get_size(self):
        raise NotImplementedError(f"Component of type {type(self)} does not implement that operation")

    # _count nodes would be same across both types
    def _count_nodes(self, node: 'TreeComponent'):
        count = 1
        for child in node.children:
            count += self._count_nodes(child)
        return count

    def get_height(self):
        raise NotImplementedError(f"Component of type {type(self)} does not implement that operation")

    # _get_height nodes would be same across both types
    def _get_height(self, node: 'TreeComponent'):
        if node.is_leaf():
            return 0

        max_child_height = 0
        for child in node.children:
            child_height = self._get_height(child)
            max_child_height = max(max_child_height, child_height)

        return max_child_height + 1

    ### implementable only by Tree
    def add_child_to_node(self, parent_node: TreeNode, child_node: TreeNode):
        raise NotImplementedError(f"Component of type {type(self)} does not implement that operation")

    def get_root(self):
        raise NotImplementedError(f"Component of type {type(self)} does not implement that operation")


