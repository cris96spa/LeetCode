from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        """
        Given the head of a singly linked list, remove the nth node from the end of the list and return its head.

        Problem Constraints:
        - The number of nodes in the list is sz.
        - 1 <= sz <= 30
        - 0 <= Node.val <= 100
        - 1 <= n <= sz

        Approach 1 (Two-Pass Naive Approach):
        1. Count the total number of nodes in the linked list.
        2. Compute the target node position from the start: `target = total_nodes - n`.
        3. Traverse again to remove the target node.
        - Time Complexity: O(sz) + O(sz) = O(sz)
        - Space Complexity: O(1)

        Approach 2 (Optimized One-Pass Solution - Two Pointers):
        1. Use a fast and a slow pointer.
        2. Move the fast pointer `n+1` steps ahead (to account for the dummy node).
        3. Move both pointers one step at a time until fast reaches the end.
        4. Slow pointer will now be just before the target node; delete it.
        5. Return the updated list, handling edge cases with a dummy node.
        - Time Complexity: O(sz)
        - Space Complexity: O(1)
        """
        # Create a dummy node to handle edge cases like removing the head
        dummy = ListNode(0, head)
        slow, fast = dummy, dummy

        # Move fast pointer n+1 steps ahead
        for _ in range(n + 1):
            fast = fast.next

        # Move both pointers until fast reaches the end
        while fast:
            slow = slow.next
            fast = fast.next

        # Remove the nth node from the end
        slow.next = slow.next.next

        return dummy.next
