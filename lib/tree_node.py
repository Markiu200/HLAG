class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []
        self.parent = None

    def add_child(self, child_node: 'TreeNode'):
        """Adds the child to the children list of the node"""
        if not isinstance(child_node, TreeNode):
            raise TypeError(f"Child node is of type {type(child_node)} whereas it should be {type(self)}")

        child_node.parent = self
        self.children.append(child_node)

    def is_leaf(self) -> bool:
        """Returns true if node has no children"""
        return len(self.children) == 0

    def is_root(self) -> bool:
        """Returns true if the node is a root of a tree (has no parent)"""
        return self.parent is None

    def get_depth(self) -> int:
        """Returns depth of the node in a tree"""
        if self.is_root():
            return 0
        return self.parent.get_depth() + 1
