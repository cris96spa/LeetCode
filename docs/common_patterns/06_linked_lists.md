# Linked Lists

## Node Definitions

### Singly Linked List
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

### Doubly Linked List
```python
class DListNode:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None
```

---

## Core Techniques

### Dummy Head Node

Use a dummy (sentinel) node before the real head to avoid special-casing insertions/deletions at the head.

```python
dummy = ListNode(0)
dummy.next = head
# ... work with the list ...
return dummy.next  # new head
```

When to use: any problem where the head might change (deletion, insertion, merging).

### Two Pointers on Linked Lists

**Find middle node** (slow lands on middle for odd-length, first-of-two-middles or second depending on init):
```python
def find_middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow  # middle (for even-length, this is the second middle)
```

**Cycle detection (Floyd's Tortoise and Hare):**
```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
```

**Find cycle start:** after slow and fast meet, reset one pointer to head. Advance both one step at a time; they meet at cycle entry.

**Nth from end:** advance one pointer n steps ahead, then move both until the leader hits null.
```python
def remove_nth_from_end(head, n):
    dummy = ListNode(0, head)
    first = second = dummy
    for _ in range(n + 1):
        first = first.next
    while first:
        first = first.next
        second = second.next
    second.next = second.next.next
    return dummy.next
```

---

## Key Problems

### Reverse Linked List (LC 206)

**Iterative** - O(n) time, O(1) space:
```python
def reverseList(head):
    prev = None
    curr = head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev
```

**Recursive** - O(n) time, O(n) space (call stack):
```python
def reverseList(head):
    if not head or not head.next:
        return head
    new_head = reverseList(head.next)
    head.next.next = head
    head.next = None
    return new_head
```

### Reverse Linked List II (LC 92) - Reverse Between Positions

Reverse nodes from position `left` to `right` (1-indexed).

O(n) time, O(1) space:
```python
def reverseBetween(head, left, right):
    dummy = ListNode(0, head)
    prev = dummy
    for _ in range(left - 1):
        prev = prev.next
    
    curr = prev.next
    for _ in range(right - left):
        nxt = curr.next
        curr.next = nxt.next
        nxt.next = prev.next
        prev.next = nxt
    
    return dummy.next
```

### Merge Two Sorted Lists (LC 21)

O(n + m) time, O(1) space:
```python
def mergeTwoLists(l1, l2):
    dummy = ListNode(0)
    tail = dummy
    while l1 and l2:
        if l1.val <= l2.val:
            tail.next = l1
            l1 = l1.next
        else:
            tail.next = l2
            l2 = l2.next
        tail = tail.next
    tail.next = l1 or l2
    return dummy.next
```

### Remove Nth Node From End (LC 19)

O(n) time, O(1) space. See the two-pointer template above.

### Linked List Cycle II (LC 142) - Find Cycle Entry Point

O(n) time, O(1) space:
```python
def detectCycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            # Found cycle, now find entry
            slow = head
            while slow != fast:
                slow = slow.next
                fast = fast.next
            return slow
    return None
```

**Why this works:** Let the distance from head to cycle start be `a`, cycle start to meeting point be `b`, and remaining cycle be `c`. At meeting: slow traveled `a + b`, fast traveled `a + b + b + c`. Since fast goes 2x speed: `2(a + b) = a + 2b + c`, so `a = c`. Moving one pointer from head and one from meeting point, both at speed 1, they meet at cycle start.

### Reorder List (LC 143)

Reorder `L0 -> L1 -> ... -> Ln` to `L0 -> Ln -> L1 -> Ln-1 -> ...`

O(n) time, O(1) space:
```python
def reorderList(head):
    if not head or not head.next:
        return
    
    # 1. Find middle
    slow = fast = head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    
    # 2. Reverse second half
    prev = None
    curr = slow.next
    slow.next = None
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    
    # 3. Merge two halves
    first, second = head, prev
    while second:
        tmp1, tmp2 = first.next, second.next
        first.next = second
        second.next = tmp1
        first, second = tmp1, tmp2
```

### LRU Cache (LC 146)

**Approach 1: OrderedDict** - O(1) for both get and put:
```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity
    
    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
```

**Approach 2: Doubly Linked List + HashMap** - O(1) for both get and put:
```python
class DListNode:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}  # key -> DListNode
        # Sentinel head and tail
        self.head = DListNode()
        self.tail = DListNode()
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev
    
    def _add_to_end(self, node):
        node.prev = self.tail.prev
        node.next = self.tail
        self.tail.prev.next = node
        self.tail.prev = node
    
    def get(self, key):
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._add_to_end(node)
        return node.val
    
    def put(self, key, value):
        if key in self.cache:
            self._remove(self.cache[key])
        node = DListNode(key, value)
        self._add_to_end(node)
        self.cache[key] = node
        if len(self.cache) > self.capacity:
            # Remove from front (least recently used)
            lru = self.head.next
            self._remove(lru)
            del self.cache[lru.key]
```

### Copy List with Random Pointer (LC 138)

O(n) time, O(n) space:
```python
def copyRandomList(head):
    if not head:
        return None
    
    old_to_new = {}
    curr = head
    while curr:
        old_to_new[curr] = Node(curr.val)
        curr = curr.next
    
    curr = head
    while curr:
        old_to_new[curr].next = old_to_new.get(curr.next)
        old_to_new[curr].random = old_to_new.get(curr.random)
        curr = curr.next
    
    return old_to_new[head]
```

**O(1) space approach:** interleave copies (A->A'->B->B'->...), set random pointers, then separate lists.

### Add Two Numbers (LC 2)

Numbers stored in reverse order. O(max(m,n)) time, O(max(m,n)) space:
```python
def addTwoNumbers(l1, l2):
    dummy = ListNode(0)
    curr = dummy
    carry = 0
    while l1 or l2 or carry:
        val = carry
        if l1:
            val += l1.val
            l1 = l1.next
        if l2:
            val += l2.val
            l2 = l2.next
        carry, val = divmod(val, 10)
        curr.next = ListNode(val)
        curr = curr.next
    return dummy.next
```

### Intersection of Two Linked Lists (LC 160)

O(n + m) time, O(1) space:
```python
def getIntersectionNode(headA, headB):
    a, b = headA, headB
    while a != b:
        a = a.next if a else headB
        b = b.next if b else headA
    return a
```

**Why this works:** pointer `a` traverses list A then list B; pointer `b` traverses list B then list A. Both travel `len(A) + len(B)` steps total, so they align at the intersection (or both reach None if no intersection).

---

## Complexity Reference

| Operation          | Singly Linked | Doubly Linked |
|--------------------|---------------|---------------|
| Access by index    | O(n)          | O(n)          |
| Insert at head     | O(1)          | O(1)          |
| Insert at tail     | O(n)*         | O(1)          |
| Delete given node  | O(n)**        | O(1)          |
| Search             | O(n)          | O(n)          |

\* O(1) if you maintain a tail pointer.
\** O(1) if you have a pointer to the previous node; otherwise O(n) to find it. Trick: copy next node's value and delete next node (only works if not the tail).

Space: O(n) for n nodes, plus pointer overhead per node (1 for singly, 2 for doubly).

---

## Common Mistakes

- **Not handling null/empty list:** always check `if not head` at the start.
- **Losing the head reference:** use a dummy node or save the head before traversal.
- **Not using dummy node when head might change:** merging, deleting, inserting at front.
- **Off-by-one in nth from end:** advance the fast pointer `n+1` times from dummy (not `n`).
- **Forgetting to terminate the list:** when splitting or reversing, set the last node's `.next = None`.
- **Modifying a list while iterating:** save `.next` before changing pointers.
- **Recursive solutions hitting stack overflow:** iterative is safer for very long lists.
