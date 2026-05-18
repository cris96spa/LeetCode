# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    """Reverse a singly linked list iteratively and recursively.

    Problem Statement:
        Given the head of a singly linked list, reverse the list and return the
        new head. Two implementations are provided.

    Approach:
        Iterative (reverseList): Traverse the list with two pointers, prev and
        curr. On each step, save the next node, reverse curr's pointer to prev,
        then advance both pointers forward. Return prev as the new head.

        Recursive (reverseListRecursive): A helper carries prev and curr. Base
        case: curr is None, return prev. Otherwise save next, reverse the
        pointer, and recurse with curr as prev and next as curr.

    Complexity:
        Time: O(n) for both approaches, where n is the number of nodes.
        Space: O(1) for the iterative approach; O(n) for the recursive approach
            due to the call stack depth.
    """

    def reverseList(self, head: ListNode | None) -> ListNode | None:
        prev_node, curr_node = None, head

        while curr_node:
            next_node = curr_node.next
            curr_node.next = prev_node
            prev_node = curr_node
            curr_node = next_node

        return prev_node

    def reverseListRecursive(self, head: ListNode | None) -> ListNode | None:
        def _reverse(prev_node: ListNode | None, curr_node: ListNode | None) -> ListNode | None:
            if curr_node is None:
                return prev_node

            next_node = curr_node.next
            curr_node.next = prev_node
            return _reverse(curr_node, next_node)

        return _reverse(None, head)
