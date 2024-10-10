from collections import deque
from typing import List, Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    """
    Problem:
    Given the root of a binary tree, return the level order traversal of its nodes' values 
    (i.e., from left to right, level by level).

    Example 1:
        Input: root = [3, 9, 20, null, null, 15, 7]
        Output: [[3], [9, 20], [15, 7]]

    Example 2:
        Input: root = [1]
        Output: [[1]]

    Example 3:
        Input: root = []
        Output: []

    Constraints:
    - The number of nodes in the tree is in the range [0, 2000].
    - Node values are between -1000 and 1000.
    
    Solution Approach:
    This solution uses Breadth-First Search (BFS) to traverse the binary tree level by level.
    BFS is ideal for this problem since it explores nodes at the current level before moving
    to the next level.

    Approach:
    1. We initialize a queue that will help us traverse the tree level by level, starting with 
       the root node.
    2. For each level, we process all nodes currently in the queue, collecting their values in 
       a list. We also enqueue the children of these nodes (if they exist) for processing in 
       the next level.
    3. Once all nodes at the current level are processed, we append the list of values to the 
       result list.
    4. This process continues until there are no more nodes to process, meaning the entire tree 
       has been traversed.
    5. The result is a list of lists, where each inner list represents the values of nodes at a 
       particular level of the binary tree.

    Time Complexity: O(n), where n is the number of nodes in the binary tree. Each node is processed once.
    Space Complexity: O(n), where n is the number of nodes. In the worst case, the queue contains 
                      n/2 nodes, and we also store the result of each node's value.
    """

    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        # If the tree is empty, return an empty list
        if root is None:
            return []

        output = []
        queue = deque([root])

        # Perform BFS
        while queue:
            current_level_values = []
            level_size = len(queue)

            # Process all nodes at the current level
            for _ in range(level_size):
                node = queue.popleft()
                current_level_values.append(node.val)

                # Add children to the queue
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            
            # Append the values of the current level to the output
            output.append(current_level_values)

        return output
