# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def reverseList(self, head: ListNode | None) -> ListNode | None:
        """
        Reverses a singly linked list iteratively.

        Args:
        head (ListNode | None): The head of the linked list.

        Returns:
        ListNode | None: The new head of the reversed linked list.

        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        prev_node, curr_node = None, head

        while curr_node:
            next_node = curr_node.next  # Save the next node
            curr_node.next = prev_node  # Reverse the pointer
            prev_node = curr_node  # Move prev_node forward
            curr_node = next_node  # Move curr_node forward

        return prev_node  # New head of the reversed list

    def reverseListRecursive(self, head: ListNode | None) -> ListNode | None:
        """
        Reverses a singly linked list recursively.

        Args:
        head (ListNode | None): The head of the linked list.

        Returns:
        ListNode | None: The new head of the reversed linked list.

        Time Complexity: O(n)
        Space Complexity: O(n) due to recursion stack.
        """

        def _reverse(
            prev_node: ListNode | None, curr_node: ListNode | None
        ) -> ListNode | None:
            if curr_node is None:
                return prev_node

            next_node = curr_node.next
            curr_node.next = prev_node
            return _reverse(curr_node, next_node)

        return _reverse(None, head)
