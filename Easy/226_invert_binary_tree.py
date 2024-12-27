from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """
    Problem Statement:
    ------------------
    Given the root of a binary tree, invert the tree, and return its root.

    Inversion means swapping the left and right subtrees of every node in the tree.

    Example:
    --------
    Input:
        root = [4, 2, 7, 1, 3, 6, 9]

                4
              /   \
             2     7
            / \   / \
           1   3 6   9

    Output:
        root = [4, 7, 2, 9, 6, 3, 1]

                4
              /   \
             7     2
            / \   / \
           9   6 3   1

    Constraints:
    ------------
    - The number of nodes in the tree is in the range [0, 100].
    - -100 <= Node.val <= 100

    Solution:
    ---------
    The solution uses recursion to traverse the binary tree and invert it by swapping the left and
    right child nodes at each step. This approach works because we handle each node independently
    and recursively invert its subtrees.

    Steps:
    1. Base Case: If the root is None, return None.
    2. Swap the left and right children of the current node.
    3. Recursively invert the left subtree.
    4. Recursively invert the right subtree.
    5. Return the root node once the tree is fully inverted.

    Time Complexity: O(n), where n is the number of nodes in the tree, as we visit each node once.
    Space Complexity: O(h), where h is the height of the tree, representing the recursion stack.
    """

    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if root is None:
            return None

        # Swap the left and right children
        root.left, root.right = root.right, root.left

        # Recursively invert the left and right subtrees
        self.invertTree(root.left)
        self.invertTree(root.right)

        return root
