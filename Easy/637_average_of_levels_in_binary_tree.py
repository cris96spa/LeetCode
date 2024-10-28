from typing import List, Optional
from statistics import mean


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """
    Problem:
    Given the root of a binary tree, return the average value of the nodes on each level in the form of an array.
    Answers within 10^-5 of the actual answer will be accepted.

    Example:
    - Example 1:
        Input: root = [3,9,20,null,null,15,7]
        Output: [3.00000,14.50000,11.00000]
        Explanation: The average value of nodes on level 0 is 3, on level 1 is 14.5, and on level 2 is 11.
        Hence return [3, 14.5, 11].

    Solution:
    This algorithm uses a level-order traversal (breadth-first search) to compute the average values of nodes on each
    level of the tree:
    1. Initialize a queue with the root node and a list to store averages.
    2. For each level, iterate through the nodes in the queue, collecting their values and adding their children to
       the queue for the next level.
    3. After processing all nodes at a level, compute the average of that level and store it in the results list.
    4. Continue until all levels are processed.

    Complexity:
    - Time Complexity: O(N), where N is the number of nodes in the tree, since each node is visited once.
    - Space Complexity: O(M), where M is the maximum width of the tree (i.e., the maximum number of nodes at any level),
      due to the queue storing nodes level-by-level.

    Returns:
    A list of floats representing the average value of nodes at each level.
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
