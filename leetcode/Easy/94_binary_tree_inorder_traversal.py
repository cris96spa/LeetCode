# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """Return the inorder traversal of a binary tree's node values.

    Problem Statement:
        Given the root of a binary tree, return the inorder traversal of its
        nodes' values (left subtree -> current node -> right subtree).

    Approach:
        Simulate the recursive call stack with an explicit stack. Keep moving
        to the leftmost node, pushing every visited node onto the stack. Once
        there is no left child, pop and process the node, then move to its right
        subtree and repeat.

    Complexity:
        Time: O(n), where n is the number of nodes. Each node is pushed and
            popped at most once.
        Space: O(n) for the output list; O(h) auxiliary for the stack, where h
            is the height of the tree.
    """

    def inorderTraversal(self, root: TreeNode | None) -> list[int]:
        result = []
        stack = []
        current = root

        while current or stack:
            while current:
                stack.append(current)
                current = current.left

            current = stack.pop()
            result.append(current.val)
            current = current.right

        return result
