class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    """
    Problem:
        Given the root of a binary tree, return the preorder traversal
        of its nodes' values.

        In preorder traversal, each node is processed before its children:

            current node -> left subtree -> right subtree

    Approach:
        A recursive preorder traversal is straightforward:
            1. Visit the current node.
            2. Recursively traverse the left subtree.
            3. Recursively traverse the right subtree.

        To avoid recursion, we can simulate the call stack manually.

        We use a stack initialized with the root node. At each step:
            1. Pop the top node.
            2. Add its value to the result.
            3. Push its right child, if it exists.
            4. Push its left child, if it exists.

        The right child is pushed before the left child because the stack
        is Last-In-First-Out. This ensures that the left child is processed
        before the right child.

    Correctness:
        The algorithm always processes a node immediately when it is popped.
        Since we push the right child first and the left child second, the left
        child is popped and processed before the right child. Therefore, every
        node is visited in preorder order:

            node -> left -> right

    Complexity:
        Let n be the number of nodes in the tree.

        Time:
            O(n), because each node is pushed and popped at most once.

        Space:
            O(n) in the worst case for the result array.
            O(h) auxiliary space for the stack in a balanced tree, where h is
            the height of the tree.
            O(n) auxiliary space in the worst case for a skewed tree.
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