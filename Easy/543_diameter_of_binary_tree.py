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
    Given the root of a binary tree, return the length of the diameter of the tree.
    
    The diameter of a binary tree is defined as the longest path between any two nodes
    in the tree, where the path length is measured by the number of edges.

    Approach:
    - We use a recursive Depth-First Search (DFS) approach to calculate the maximum depth
      of the left and right subtrees for each node.
    - The diameter at each node is determined as `left_depth + right_depth`.
    - We maintain a global (or nonlocal) variable `max_diameter` to track the maximum diameter
      encountered during the traversal.

    Algorithm:
    1. Define a helper function `dfs(node)` that:
       - Recursively computes the maximum depth of left and right subtrees.
       - Updates `max_diameter` with the sum of left and right subtree depths.
       - Returns the height of the current node (1 + max(left_depth, right_depth)).
    2. Initialize `max_diameter` as 0 and start the DFS from the root.
    3. Return `max_diameter` as the final result.

    Complexity Analysis:
    - **Time Complexity:** O(N), where N is the number of nodes in the tree. Each node is visited once.
    - **Space Complexity:** O(H), where H is the height of the tree. This is due to recursive calls.
      - In a balanced tree, H = log(N) → O(log N) space.
      - In a skewed tree, H = N → O(N) space.

    Edge Cases Considered:
    - An empty tree (return 0).
    - A tree with a single node (diameter = 0).
    - A perfectly balanced tree.
    - A skewed tree (linked-list-like structure).

    Example:
    ```
         1
        / \
       2   3
      / \
     4   5
    ```
    - The longest path is [4 → 2 → 5] or [4 → 2 → 1 → 3], with a diameter of 3.
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
