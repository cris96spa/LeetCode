class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """Return the preorder traversal of a binary tree's node values.

    Problem Statement:
        Given the root of a binary tree, return the preorder traversal of its
        nodes' values (current node -> left subtree -> right subtree).

    Approach:
        Use an explicit stack to simulate the recursive call stack. Push the
        root first. At each step, pop the top node, record its value, then push
        its right child followed by its left child. Because the stack is LIFO,
        the left child is processed before the right, preserving preorder.

    Complexity:
        Time: O(n), each node is pushed and popped exactly once.
        Space: O(n) for the output list; O(h) auxiliary for the stack, where h
            is the height of the tree.
    """

    def preorderTraversal(self, root: TreeNode | None) -> list[int]:
        if root is None:
            return []

        result = []
        stack = [root]

        while stack:
            node = stack.pop()
            result.append(node.val)

            if node.right is not None:
                stack.append(node.right)

            if node.left is not None:
                stack.append(node.left)

        return result
