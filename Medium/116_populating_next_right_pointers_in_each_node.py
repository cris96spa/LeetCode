from collections import deque
from typing import Optional


# Definition for a Node.
class Node:
    def __init__(
        self,
        val: int = 0,
        left: "Node" = None,
        right: "Node" = None,
        next: "Node" = None,
    ):
        self.val = val
        self.left = left
        self.right = right
        self.next = next


class Solution:
    """
    You are given a perfect binary tree where all leaves are on the same level, and every parent has two children.

    Populate each next pointer to point to its next right node. If there is no next right node, the next pointer
    should be set to NULL. Initially, all next pointers are set to NULL.

    Example:
    Input: root = [1,2,3,4,5,6,7]
    Output: [1,#,2,3,#,4,5,6,7,#]
    Explanation: Given the above perfect binary tree (Figure A), your function should populate each next pointer
    to point to its next right node, just like in Figure B. The serialized output is in level order as connected
    by the next pointers, where '#' signifies the end of each level.

    Approach:
    1. Perform a level-order traversal (BFS) using a queue.
    2. At each level, traverse all nodes and link each node's `next` pointer to the next node in the queue,
       except for the last node at that level.
    3. For each node, enqueue its left and right children if they exist.
    4. Return the modified tree.

    Time Complexity: O(N), where N is the number of nodes in the tree. Each node is visited once.
    Space Complexity: O(N), due to the space required for the queue.

    """

    def connect(self, root: "Optional[Node]") -> "Optional[Node]":
        # Empty check
        if not root:
            return root

        queue = deque([root])

        # Iterate until there are elements to be visited
        while queue:
            size = len(queue)

            for i in range(size):
                # Get the next node to be assigned
                curr = queue.popleft()

                if i < size - 1:
                    curr.next = queue[0]

                # Add the new nodes to the queue
                if curr.left:
                    queue.append(curr.left)
                if curr.right:
                    queue.append(curr.right)

        return root
