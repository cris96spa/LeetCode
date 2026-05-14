from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """Return the length of the diameter of a binary tree.

    Problem Statement:
        Given the root of a binary tree, return the length of its diameter. The
        diameter is the length of the longest path between any two nodes,
        measured in number of edges. The path may or may not pass through the
        root.

    Approach:
        Use recursive DFS. For each node, compute the depth of its left and
        right subtrees. The diameter candidate at that node equals left_depth +
        right_depth. A nonlocal variable tracks the global maximum across all
        nodes. Each call returns the node's height (1 + max(left, right)) to
        allow the parent to compute its own candidate.

    Complexity:
        Time: O(n), where n is the number of nodes. Each node is visited once.
        Space: O(h), where h is the height of the tree, due to the call stack.
    """

    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        def dfs(node: Optional[TreeNode]) -> int:
            if not node:
                return 0

            left_depth, right_depth = dfs(node.left), dfs(node.right)
            nonlocal max_diameter
            max_diameter = max(max_diameter, left_depth + right_depth)

            return 1 + max(left_depth, right_depth)

        max_diameter = 0
        dfs(root)
        return max_diameter
