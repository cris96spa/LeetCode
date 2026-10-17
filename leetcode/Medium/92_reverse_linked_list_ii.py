# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    """Reverse the nodes of a linked list between two positions.

    Problem Statement:
        Given the head of a singly linked list and two integers left and
        right, where left <= right, reverse the nodes of the list from
        position left to position right (1-indexed) and return the list.
        The boundaries are assumed to be valid.

    Approach:
        A dummy node pointing to head avoids special-casing left == 1.

        - Starting from the dummy, advance left - 1 times to reach
          before_first, the node just before the window. Its next is first,
          the first node of the window.
        - Reverse the right - left + 1 nodes of the window in place with the
          usual prev/curr loop. When it ends, prev is the last node of the
          window (now its head) and curr is the node right after it.
        - Reconnect: before_first -> prev and first -> curr.

    Complexity:
        Time: O(n), a single pass up to position right.
        Space: O(1), constant extra space.
    """

    def reverseBetween(self, head: ListNode | None, left: int, right: int) -> ListNode | None:
        # Base case when no swaps are required
        if left == right:
            return head

        dummy_node = ListNode(0, head)
        before_first = dummy_node

        # Find the pointer to the entry of the sublist to be reversed
        for _ in range(left - 1):
            before_first = before_first.next

        # Reverse whatever is inside the right - left window
        first = before_first.next
        prev, curr = None, first
        for _ in range(right - left + 1):
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt

        before_first.next = prev
        first.next = curr

        return dummy_node.next
