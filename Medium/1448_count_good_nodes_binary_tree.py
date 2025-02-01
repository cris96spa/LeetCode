# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def goodNodes(self, root: TreeNode) -> int:
        """
        Given a binary tree root, a node X in the tree is named a "good node" if,
        in the path from the root to X, there are no nodes with a value greater than X.

        This function returns the count of good nodes in the binary tree.

        Approach:
        - Perform a Depth-First Search (DFS) traversal of the tree.
        - Maintain the maximum value encountered so far (`_max`) on the current path.
        - If the current node's value is greater than or equal to `_max`, it is counted as a good node.
        - Recursively check left and right children, updating `_max` as necessary.

        Time Complexity:
        - O(N), where N is the number of nodes in the tree, since each node is visited once.

        Space Complexity:
        - O(H), where H is the height of the tree. In the worst case (skewed tree), H can be O(N),
          while in a balanced tree, it is O(log N).


        :param root: TreeNode - The root of the binary tree.
        :return: int - Number of good nodes in the tree.
        """

        def dfs(node: TreeNode, _max: float) -> int:
            if not node:
                return 0

            # Determine if the current node is "good"
            curr_valid = 1 if node.val >= _max else 0

            # Update the max value for the path
            new_max = max(_max, node.val)

            # Recur for left and right children
            left_valid = dfs(node.left, new_max)
            right_valid = dfs(node.right, new_max)

            return curr_valid + left_valid + right_valid

        return dfs(root, root.val)
