class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """Problem:.

        Given the root of a Binary Search Tree and an integer val, insert val into
        the BST while preserving the BST property. Return the root of the BST after
        insertion.

    Approach:
        Traverse the tree iteratively starting from the root.

        At each node:
            - If val is smaller than the current node's value, move to the left child.
            - Otherwise, move to the right child.

        When the desired child pointer is empty, insert the new node there.

        If the tree is empty, the new node becomes the root.

    Correctness:
        Since we always move left when val is smaller and right otherwise, we follow
        the exact path where val must be placed according to the BST property.
        The first empty position on this path is a valid insertion point.

    Complexity:
        Time:
            O(h), where h is the height of the tree.
            In the worst case, the tree is skewed, so h = n and time is O(n).
            If the tree is balanced, h = log n and time is O(log n).

        Space:
            O(1), because the solution is iterative and uses only a few variables.
    """

    def insertIntoBST(self, root: TreeNode | None, val: int) -> TreeNode | None:
        new_node = TreeNode(val)

        if root is None:
            return new_node

        curr = root

        while curr:
            if val < curr.val:
                if curr.left is None:
                    curr.left = new_node
                    break
                curr = curr.left
            else:
                if curr.right is None:
                    curr.right = new_node
                    break
                curr = curr.right

        return root
