# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    """Reorder a linked list to interleave nodes from the front and back halves.

    Problem Statement:
        Given the head of a singly linked list L0 -> L1 -> ... -> Ln-1 -> Ln,
        reorder it in-place to: L0 -> Ln -> L1 -> Ln-1 -> L2 -> Ln-2 -> ...
        Node values must not be modified; only the nodes themselves may change.

    Approach:
        1. Find the middle using slow/fast pointers; slow ends at the midpoint.
        2. Reverse the second half of the list in-place.
        3. Merge the two halves by alternating one node from each.

    Complexity:
        Time: O(n), each of the three passes over the list is linear.
        Space: O(1), all operations are performed in-place.
    """

    def reorderList(self, head: ListNode | None) -> None:
        if not head or not head.next or not head.next.next:
            return

        # Step 1: Find the middle of the list
        slow, fast = head, head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        # Step 2: Reverse the second half of the list
        prev, curr = None, slow.next
        slow.next = None
        while curr:
            next_node = curr.next
            curr.next, prev = prev, curr
            curr = next_node

        # Step 3: Merge the two halves
        left, right = head, prev
        while right:
            left_next, right_next = left.next, right.next
            left.next, right.next = right, left.next
            left, right = left_next, right_next
