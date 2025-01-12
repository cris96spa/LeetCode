# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def hasCycle(self, head: ListNode | None) -> bool:
        """
        Determines if a linked list has a cycle using Floyd's Tortoise and Hare Algorithm.

        Args:
        head (Optional[ListNode]): The head of the linked list.

        Returns:
        bool: True if the list has a cycle, False otherwise.

        Time Complexity: O(n), where n is the number of nodes in the linked list.
        Space Complexity: O(1), constant space usage.
        """
        # Edge case: A list with 0 or 1 node cannot have a cycle
        if not head or not head.next:
            return False

        # Initialize two pointers, slow (1 step) and fast (2 steps)
        slow, fast = head, head

        # Traverse the list
        while fast and fast.next:
            slow = slow.next  # Move slow pointer by 1 step
            fast = fast.next.next  # Move fast pointer by 2 steps

            # If the two pointers meet, a cycle exists
            if slow == fast:
                return True

        # If we exit the loop, no cycle is present
        return False
