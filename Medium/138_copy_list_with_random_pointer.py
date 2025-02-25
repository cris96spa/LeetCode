"""
Problem Statement:
------------------
A linked list of length n is given, where each node contains an additional `random` pointer, which
could point to any node in the list or be null.

The task is to construct a deep copy of the list. The deep copy should consist of exactly `n` brand
new nodes, where each new node has its value set to the value of its corresponding original node.
Both the `next` and `random` pointers of the new nodes should point to new nodes in the copied list
such that the pointers in the original list and copied list represent the same list state.

None of the pointers in the new list should point to nodes in the original list.

For example, if there are two nodes X and Y in the original list, where X.random --> Y, then for
the corresponding two nodes x and y in the copied list, x.random --> y.

The linked list is represented as a list of nodes, where each node is represented as a pair:
    [val, random_index]
Where:
- `val` is an integer representing `Node.val`
- `random_index` is the index of the node (range from `0` to `n-1`) that the `random` pointer points to,
  or `null` if it does not point to any node.

Function Signature:
-------------------
def copyRandomList(self, head: Optional[Node]) -> Optional[Node]

Solutions:
----------
1. **O(n) Space Approach (Using Hash Map)**:
   - Traverse the original list and create a mapping of original nodes to their new copies.
   - Traverse the list again to assign the `next` and `random` pointers using the mapping.
   - Time Complexity: O(n)
   - Space Complexity: O(n)

2. **O(1) Space Approach (Interleaved Nodes)**:
   - Create interleaved copies of nodes in the original list.
   - Assign `random` pointers to copied nodes.
   - Separate the copied list from the original list while restoring the original.
   - Time Complexity: O(n)
   - Space Complexity: O(1) (excluding the output list)
"""

from typing import Optional


# Definition for a Node.
class Node:
    def __init__(self, x: int, next: "Node" = None, random: "Node" = None):
        self.val = int(x)
        self.next = next
        self.random = random


class Solution:
    def copyRandomList_hashmap(self, head: Optional[Node]) -> Optional[Node]:
        """
        Creates a deep copy of the linked list using a hash map.

        Time Complexity: O(n)
        Space Complexity: O(n) (due to dictionary storing node mappings)
        """
        if not head:
            return None

        # Mapping of original nodes to their copied versions
        mapping = {}
        curr = head

        # First pass: Create copies of nodes and store them in the mapping
        while curr:
            mapping[curr] = Node(curr.val)
            curr = curr.next

        # Second pass: Assign next and random pointers
        curr = head
        while curr:
            curr_copy = mapping[curr]
            curr_copy.next = mapping.get(
                curr.next
            )  # Get returns None if key is not found
            curr_copy.random = mapping.get(curr.random)
            curr = curr.next

        return mapping[head]

    def copyRandomList_optimized(self, head: Optional[Node]) -> Optional[Node]:
        """
        Creates a deep copy of the linked list using O(1) extra space.

        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        if not head:
            return None

        # Step 1: Create interleaved copies of nodes
        curr = head
        while curr:
            new_node = Node(curr.val)  # Create a copy
            new_node.next = curr.next  # Insert copy between original nodes
            curr.next = new_node
            curr = new_node.next  # Move to the next original node

        # Step 2: Assign random pointers to copied nodes
        curr = head
        while curr:
            if curr.random:
                curr.next.random = curr.random.next  # Copy random pointer
            curr = curr.next.next  # Move two steps ahead

        # Step 3: Separate copied list from original list
        curr, new_head = head, head.next
        copy_curr = new_head
        while curr:
            curr.next = copy_curr.next  # Restore original list
            curr = curr.next
            if curr:
                copy_curr.next = curr.next  # Set correct next pointer for copied list
                copy_curr = copy_curr.next

        return new_head
