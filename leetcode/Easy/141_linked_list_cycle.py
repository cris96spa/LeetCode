# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    """Detect whether a singly linked list contains a cycle.

    Problem Statement:
        Given the head of a linked list, determine if the linked list has a
        cycle in it. A cycle exists if some node can be reached again by
        continuously following the next pointer.

    Approach:
        Use Floyd's Tortoise and Hare algorithm. Two pointers start at the head:
        slow advances one step at a time, fast advances two steps. If there is a
        cycle, the two pointers will eventually meet inside it. If fast reaches
        None, there is no cycle.

    Complexity:
        Time: O(n), where n is the number of nodes in the linked list.
        Space: O(1), only two pointer variables are used.
    """

    def hasCycle(self, head: ListNode | None) -> bool:
        if not head or not head.next:
            return False

        slow, fast = head, head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

            if slow == fast:
                return True

        return False
