"""
Given the root of a binary tree, return its maximum depth.
A binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.

Example 1:

Input: root = [3,9,20,null,null,15,7]
Output: 3
Example 2:

Input: root = [1,null,2]
Output: 2
 
Constraints:
The number of nodes in the tree is in the range [0, 104].
-100 <= Node.val <= 100
"""

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0

        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right)) 

"""
This function calculates the maximum depth of a binary tree. The maximum depth is defined as the number of nodes along the longest path from the root node down to the farthest leaf node.

The approach used in this solution is a recursive depth-first traversal of the binary tree. Here's a step-by-step explanation:

1. **Base Case**:
   - The base case for the recursion is when the `root` is `None`. If the tree is empty (i.e., the node is `None`), the depth is 0, so the function returns 0.

2. **Recursive Case**:
   - If the current node is not `None`, the function recursively calculates the maximum depth of the left and right subtrees by calling `self.maxDepth(root.left)` and `self.maxDepth(root.right)`, respectively.
   - The function then returns 1 plus the maximum of these two depths. The `1` accounts for the current node's depth, and `max(self.maxDepth(root.left), self.maxDepth(root.right))` ensures that we are considering the longest path from the current node to a leaf node.

3. **Combining Results**:
   - By recursively applying this logic from the root down to each leaf, the function effectively calculates the depth of the deepest path in the binary tree.

This algorithm has a time complexity of O(n), where n is the number of nodes in the tree, since each node is visited once during the traversal.
"""
