class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """
    Given the root of a binary tree, return the lowest common ancestor
    of its deepest leaves.

    Approach:
    Use postorder DFS.

    For every node, return:
        1. The height of the deepest leaf in this node's subtree.
        2. The LCA of all deepest leaves in this node's subtree.

    Recurrence:
        - If the left subtree is deeper, the answer comes from the left subtree.
        - If the right subtree is deeper, the answer comes from the right subtree.
        - If both subtrees have the same depth, the current node is the LCA.

    Time Complexity:
        O(n), where n is the number of nodes.

    Space Complexity:
        O(h), where h is the height of the tree due to recursion stack.
        Worst case: O(n) for a skewed tree.
        Best case: O(log n) for a balanced tree.
    """

    def lcaDeepestLeaves(self, root: TreeNode | None) -> TreeNode | None:
        def dfs(node: TreeNode | None) -> tuple[int, TreeNode | None]:
            if not node:
                return 0, None

            left_depth, left_lca = dfs(node.left)
            right_depth, right_lca = dfs(node.right)

            if left_depth > right_depth:
                return left_depth + 1, left_lca

            if right_depth > left_depth:
                return right_depth + 1, right_lca

            return left_depth + 1, node

        return dfs(root)[1]
