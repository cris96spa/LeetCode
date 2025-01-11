# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def reorderList(self, head: ListNode | None) -> None:
        """
        Do not return anything, modify head in-place instead.

        Problem Statement:
        You are given the head of a singly linked list. The list can be represented as:
        L0 → L1 → … → Ln - 1 → Ln

        Reorder the list to be in the following form:
        L0 → Ln → L1 → Ln - 1 → L2 → Ln - 2 → …

        You may not modify the values in the list's nodes. Only nodes themselves may be changed.

        Approach:
        1. Find the middle of the linked list using the slow and fast pointer technique.
           - The slow pointer moves one step at a time, while the fast pointer moves two steps.
           - When the fast pointer reaches the end, the slow pointer will be at the middle.

        2. Reverse the second half of the list.
           - Starting from the node after the middle, reverse the `next` pointers to reverse the list.
           - Disconnect the first half from the second half by setting `slow.next = None`.

        3. Merge the two halves alternately.
           - Use two pointers to traverse the first and reversed second halves.
           - Alternate the nodes from the first and second halves by updating the `next` pointers.

        Complexity:
        - Time Complexity: O(n)
          - Finding the middle: O(n)
          - Reversing the second half: O(n)
          - Merging two halves: O(n)
        - Space Complexity: O(1)
          - The solution modifies the list in-place and uses no extra space.

        Edge Cases:
        - An empty list or a list with fewer than three nodes is handled directly by the early return condition.

        Parameters:
        - head: ListNode
            The head of the singly linked list.

        Returns:
        - None
            The function modifies the list in-place without returning anything.
        """
        if not head or not head.next or not head.next.next:
            return

        # Step 1: Find the middle of the list
        slow, fast = head, head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        # Step 2: Reverse the second half of the list
        prev, curr = None, slow.next
        slow.next = None  # Disconnect the first half from the second half
        while curr:
            _next = curr.next
            curr.next, prev = prev, curr
            curr = _next

        # Step 3: Merge the two halves
        left, right = head, prev
        while right:
            _left, _right = left.next, right.next
            left.next, right.next = right, left.next
            left, right = _left, _right
