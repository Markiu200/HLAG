from tree_node import TreeNode


class Tree:
    def __init__(self, root_data):
        self.root = TreeNode(root_data)

    def walk(self):
        yield from self._walk(self.root)

    def _walk(self, node):
        yield node
        for child in node.children:
            yield from self._walk(child)

    def add_child_to_node(self, parent_node: TreeNode, child_node: TreeNode):
        parent_node.add_child(child_node)

    def get_root(self):
        return self.root

    def get_size(self):
        return self._count_nodes(self.root)

    def _count_nodes(self, node: TreeNode):
        count = 1
        for child in node.children:
            count += self._count_nodes(child)
        return count

    def get_height(self):
        return self._get_height(self.root)

    def _get_height(self, node: TreeNode):
        if node.is_leaf():
            return 0

        max_child_height = 0
        for child in node.children:
            child_height = self._get_height(child)
            max_child_height = max(max_child_height, child_height)

        return max_child_height + 1

    def get_node(self, data):
        return self._get_node(self.root, data)

    def _get_node(self, node:TreeNode, data):
        if node.data == data:
            return node

        for child in node.children:
            results = self._get_node(child, data)
            if results:
                return results

        return None
