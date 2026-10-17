# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    """Check whether a singly linked list is a palindrome.

    Problem Statement:
        Given the head of a singly linked list, return true if it is a
        palindrome, or false otherwise.

    Approach:
        Easy approach: copy the values into an array and walk two pointers,
        one from the start and one from the end, until they meet in the
        middle. This takes O(n) time and O(n) space for the array.

        Better: the list is already made of pointers, so the array is not
        needed. We just need to:
            - find the middle with slow/fast pointers;
            - reverse the second half in place;
            - walk the first half and the reversed second half together,
              stopping when the second half runs out.

        For odd lengths the middle node ends up at the tail of the first
        half and is never compared, so even and odd lengths need no
        special handling.

    Complexity:
        Time: O(n), three linear scans: find the middle, reverse the second
            half, compare values.
        Space: O(1), constant extra space.
    """

    def isPalindrome(self, head: ListNode | None) -> bool:
        if not head or not head.next:
            return True

        # 1. Find the middle
        slow, fast = head, head.next

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        slow = slow.next

        # 2. Reverse the second half
        def reverse_list(node):
            prev = None
            curr = node

            while curr:
                nxt = curr.next
                curr.next = prev
                prev = curr
                curr = nxt

            return prev

        second = reverse_list(slow)

        # 3. Compare both halves
        first = head

        while second:
            if first.val != second.val:
                return False

            first = first.next
            second = second.next

        return True
