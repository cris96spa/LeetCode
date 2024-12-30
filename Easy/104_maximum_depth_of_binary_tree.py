from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        """
        Problem Statement:
        ------------------
        Given the root of a binary tree, return its maximum depth.

        The maximum depth is the number of nodes along the longest path from the root node
        down to the farthest leaf node.

        Parameters:
        -----------
        root : Optional[TreeNode]
            The root of the binary tree.

        Returns:
        --------
        int
            The maximum depth of the binary tree.

        Approach:
        ---------
        1. Use a recursive depth-first traversal of the binary tree to calculate the depth.
        2. For each node, compute the maximum depth of its left and right subtrees.
        3. Add 1 to the greater of the two depths to include the current node.
        4. Base Case: If the node is None (empty), return 0.

        Complexity:
        -----------
        - Time Complexity: O(n), where n is the number of nodes in the tree, as each node is visited once.
        - Space Complexity: O(h), where h is the height of the tree, due to the recursive call stack.

        Examples:
        ---------
        Example 1:
        Input: root = [3,9,20,null,null,15,7]
        Output: 3

        Example 2:
        Input: root = [1,null,2]
        Output: 2

        Example 3:
        Input: root = []
        Output: 0

        """
        if not root:
            return 0
        return max(self.maxDepth(root.left), self.maxDepth(root.right)) + 1
