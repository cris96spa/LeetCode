class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """Determine if a binary tree is height-balanced.

    Problem:
        Given a binary tree, determine whether it is height-balanced.

        A binary tree is balanced if, for every node, the heights of its
        left and right subtrees differ by at most 1.

    Strategy:
        Use postorder DFS.

        For each node, we first compute the heights of the left and right
        subtrees. If either subtree is already unbalanced, propagate -1 upward.

        The DFS returns:
            - height of the subtree if it is balanced
            - -1 if the subtree is unbalanced

        This allows us to compute height and check balance in one traversal.

    Complexity:
        Time: O(n), where n is the number of nodes.
        Space: O(h), where h is the height of the tree, due to recursion stack.
    """

    def isBalanced(self, root: TreeNode | None) -> bool:

        def dfs(node: TreeNode | None) -> int:
            if not node:
                return 0

            left_height = dfs(node.left)
            if left_height == -1:
                return -1

            right_height = dfs(node.right)
            if right_height == -1:
                return -1

            if abs(left_height - right_height) > 1:
                return -1

            return 1 + max(left_height, right_height)

        return dfs(root) != -1
