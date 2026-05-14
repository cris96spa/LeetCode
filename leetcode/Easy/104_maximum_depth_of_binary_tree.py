from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """Return the maximum depth of a binary tree.

    Problem Statement:
        Given the root of a binary tree, return its maximum depth. The maximum
        depth is the number of nodes along the longest path from the root node
        down to the farthest leaf node.

    Approach:
        Use recursive DFS. For each node, compute the maximum depth of the left
        and right subtrees, then return 1 plus the greater of the two. The base
        case returns 0 for a None node.

    Complexity:
        Time: O(n), where n is the number of nodes, as each node is visited once.
        Space: O(h), where h is the height of the tree, due to the call stack.
    """

    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        return max(self.maxDepth(root.left), self.maxDepth(root.right)) + 1
