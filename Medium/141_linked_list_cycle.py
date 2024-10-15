from typing import Optional


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    """
    Problem:
    Given the head of a linked list, determine if the linked list contains a cycle.

    A cycle occurs if a node in the linked list can be reached again by continuously following the `next` pointer.
    Internally, the position `pos` is used to denote the index of the node that the tail's next pointer connects to.
    However, the position is not provided as an input parameter to the function.

    Return `True` if there is a cycle in the linked list, otherwise return `False`.
    Can you solve the problem using constant O(1) memory?

    Solution:
    The problem can be solved using Floyd’s Cycle Detection Algorithm, also known as the Tortoise and Hare algorithm.
    The idea is to maintain two pointers, one moving at twice the speed of the other. If the linked list has a cycle,
    these two pointers will eventually meet, indicating the presence of a cycle. If no cycle exists,
    the faster pointer will reach the end of the list.

    Approach:
    1. Initialize two pointers, `next_node` and `double_next_node`, both starting at the head of the linked list.
    2. Traverse the list with `next_node` moving one step at a time and `double_next_node` moving two steps at a time.
    3. If at any point the two pointers meet, return `True`, indicating that a cycle is detected.
    4. If `double_next_node` reaches the end of the list, return `False`, indicating no cycle.

    Time Complexity: O(n), where n is the number of nodes in the linked list.
    Space Complexity: O(1), as only two pointers are used.
    """

    def hasCycle(self, head: Optional[ListNode]) -> bool:
        next_node = double_next_node = head

        while double_next_node and double_next_node.next:
            next_node = next_node.next
            double_next_node = double_next_node.next.next

            if next_node == double_next_node:
                return True
        return False
