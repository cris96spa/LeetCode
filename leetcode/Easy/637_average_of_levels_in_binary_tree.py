from statistics import mean
from typing import List, Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """Return the average value of nodes on each level of a binary tree.

    Problem Statement:
        Given the root of a binary tree, return the average value of the nodes
        on each level as a list of floats. Answers within 10^-5 of the actual
        answer are accepted.

    Approach:
        Use level-order traversal (BFS) with a single flat list as the queue.
        Track the start index of the current level. For each level, iterate from
        start to the current queue end, enqueue each node's children, collect
        values, then compute and store the average before advancing the index.

    Complexity:
        Time: O(n), where n is the number of nodes. Each node is visited once.
        Space: O(m), where m is the maximum width of the tree, for the queue.
    """

    def averageOfLevels(self, root: Optional[TreeNode]) -> List[float]:
        if not root:
            return []

        queue = [root]
        output = []

        start = 0
        while start < len(queue):
            level = []
            end = len(queue)
            for node in queue[start:end]:
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
                level.append(node.val)
            output.append(mean(level))
            start = end

        return output
