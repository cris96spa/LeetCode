from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """Invert a binary tree by swapping left and right subtrees at every node.

    Problem Statement:
        Given the root of a binary tree, invert the tree and return its root.
        Inversion means swapping the left and right child of every node in the
        tree.

    Approach:
        Use recursive DFS. For each node, swap its left and right children, then
        recursively invert both subtrees. The base case returns None for an
        empty node.

    Complexity:
        Time: O(n), where n is the number of nodes, as each node is visited once.
        Space: O(h), where h is the height of the tree, due to the call stack.
    """

    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if root is None:
            return None

        root.left, root.right = root.right, root.left
        self.invertTree(root.left)
        self.invertTree(root.right)

        return root
