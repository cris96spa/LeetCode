from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """Find the kth smallest value in a binary search tree.

    Problem Statement:
        Given the root of a BST and an integer k, return the kth smallest value
        (1-indexed) of all node values in the tree.

    Approach:
        Perform an inorder traversal (left, current, right) which visits BST nodes
        in ascending order. Collect results until we have k elements, then return
        the kth element.

    Complexity:
        Time: O(n) in the worst case where n is the number of nodes.
        Space: O(n) for the recursion stack and result list.
    """

    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        self.result = []

        def inorder(node):
            if node is None:
                return
            inorder(node.left)
            self.result.append(node.val)
            if len(self.result) >= k:
                return
            else:
                inorder(node.right)

        inorder(root)
        return self.result[k - 1]
