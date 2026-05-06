# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def inorderTraversal(self, root: TreeNode | None) -> list[int]:
        """
        LeetCode 94 - Binary Tree Inorder Traversal

        Given the root of a binary tree, return the inorder traversal of
        its nodes' values.

        Inorder traversal visits nodes in this order:

            left subtree -> current node -> right subtree

        Recursive intuition:
        Starting from the root, first recursively traverse the left subtree,
        then process the current node, and finally recursively traverse the
        right subtree.

        Iterative approach:
        We simulate the recursive call stack manually using a stack.

        The idea is:
        1. Keep moving to the leftmost node, pushing every visited node
           onto the stack.
        2. Once there is no more left child, pop from the stack and process
           that node.
        3. Then move to its right subtree and repeat the same process.

        Complexity:
            Time: O(n), where n is the number of nodes, because each node is
                pushed and popped at most once.
            Space: O(n) including the output list.
                O(h) auxiliary space for the stack, where h is the height of the tree.
                In the worst case h = n for a skewed tree.
        """
        result = []
        stack = []
        current = root

        while current or stack:
            while current:
                stack.append(current)
                current = current.left

            current = stack.pop()
            result.append(current.val)

            # Move to the right subtree
            current = current.right

        return result
