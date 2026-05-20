class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """Given the root of a BST and a key, delete the node whose value equals key.

    Return the root of the modified BST.
    Idea:
        Use the BST property to recursively search for the target node.

        If key < root.val:
            delete from the left subtree.

        If key > root.val:
            delete from the right subtree.

        If key == root.val:
            we found the node to delete.

            There are three cases:

            1. root has no left child:
                Replace root with root.right.

            2. root has no right child:
                Replace root with root.left.

            3. root has two children:
                Find the inorder successor, which is the smallest node in
                root.right. Copy the successor's value into root, then delete
                the duplicate successor from root.right.

    Complexity:
        Let h be the height of the tree.

        Time: O(h)
            We follow one BST search path. In the two-child case, we also walk
            down to the leftmost node of the right subtree, which is still O(h).

        Space: O(h)
            Due to the recursion stack.
    """

    def deleteNode(self, root: TreeNode | None, key: int) -> TreeNode | None:
        if not root:
            return None

        if key < root.val:
            root.left = self.deleteNode(root.left, key)

        elif key > root.val:
            root.right = self.deleteNode(root.right, key)

        else:
            # Case 1: no left child
            if not root.left:
                return root.right

            # Case 2: no right child
            if not root.right:
                return root.left

            # Case 3: two children
            successor = root.right
            while successor.left:
                successor = successor.left

            root.val = successor.val
            root.right = self.deleteNode(root.right, successor.val)

        return root
