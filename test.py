from itertools import chain
from outline_node import OutlineNode

my_tree = Tree("root")

my_tree.add_child_to_node(my_tree.get_root(), TreeNode("1a"))
my_tree.add_child_to_node(my_tree.get_root(), TreeNode("1b"))
my_tree.add_child_to_node(my_tree.get_node("1b"), TreeNode("2a"))
my_tree.add_child_to_node(my_tree.get_node("1b"), TreeNode("2b"))
my_tree.add_child_to_node(my_tree.get_node("2b"), TreeNode("3a"))
my_tree.add_child_to_node(my_tree.get_node("2b"), TreeNode("3b"))
my_tree.add_child_to_node(my_tree.get_node("1b"), TreeNode("2c"))
my_tree.add_child_to_node(my_tree.get_root(), TreeNode("1c"))

# root = my_tree.get_root()
#
# root.add_child(TreeNode("1a"))
#
# second = TreeNode("1b")
# root.add_child(second)
#
# second.add_child(TreeNode("2a"))
#
# third = TreeNode("2b")
# second.add_child(third)
#
# second.add_child(TreeNode("2c"))
#
# third.add_child(TreeNode("3a"))
# third.add_child(TreeNode("3b"))
#
# root.add_child(TreeNode("1c"))

for node in my_tree.walk():
    print(node.data)
