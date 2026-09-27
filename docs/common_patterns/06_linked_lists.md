# Linked Lists

Data structures come in two fundamental flavors. **Contiguous** structures — arrays, dynamic arrays, heaps, hash tables — live in a single block of memory. **Linked** structures — lists, trees, graph adjacency lists — are separate chunks of memory tied together by pointers. Nearly every data structure you will ever use is built from one of these two, or both.

The linked list is the simplest linked structure, and it is worth studying less for its own sake (in Python, you'll rarely choose one) than for what it teaches: how to reason about pointer manipulation, how to exploit recursive structure, and how the choice between contiguous and linked storage makes some operations cheap and others expensive.

---

## Contiguous vs. Linked

| | Array (contiguous) | Linked list |
|---|---|---|
| Access the $i$-th element | $O(1)$: compute the address | $O(i)$: follow $i$ pointers |
| Insert / delete at a **known position** | $O(n)$: shift elements | $O(1)$: rewire a couple of pointers |
| Insert / delete at the front | $O(n)$ | $O(1)$ |
| Append at the end | $O(1)$ amortized (dynamic array) | $O(1)$ with a tail pointer |
| Memory overhead | None beyond the data | One or two pointers per element |
| Cache behavior | Excellent: sequential memory | Poor: every hop may be a cache miss |
| Growth | Occasional $O(n)$ copy on resize | Never needs to move existing elements |

Arrays win on random access, space, and locality. Linked lists win when you need to **splice**: insert or remove elements in the middle, given a reference to where, without disturbing anything else. They also let you move large records around by moving pointers instead of copying the records themselves.

!!! note "Python's `list` is an array"
    Python's `list` is a dynamic array, and `collections.deque` is a doubly linked list of fixed-size blocks, giving $O(1)$ operations at both ends. In real Python code, explicit node-based linked lists appear mainly inside other structures — the LRU cache below, `OrderedDict`'s internals — where $O(1)$ removal of a node you already hold is exactly what's needed.

### The same operations, different costs

It's illuminating to compare how each list variant supports the basic dictionary operations. Assume we're handed a reference to the node $x$ for delete / successor / predecessor.

| Operation | Singly, unsorted | Singly, sorted | Doubly, unsorted | Doubly, sorted |
|---|---|---|---|---|
| Search($k$) | $O(n)$ | $O(n)$ | $O(n)$ | $O(n)$ |
| Insert($x$) | $O(1)$ | $O(n)$ | $O(1)$ | $O(n)$ |
| Delete($x$) | $O(n)$ † | $O(n)$ † | $O(1)$ | $O(1)$ |
| Successor($x$) | $O(n)$ | $O(1)$ | $O(n)$ | $O(1)$ |
| Predecessor($x$) | $O(n)$ | $O(n)$ | $O(n)$ | $O(1)$ |
| Minimum / Maximum | $O(n)$ | $O(1)$ | $O(n)$ | $O(1)$ |

A few entries deserve explanation:

- **Sorting a list doesn't speed up search.** Binary search needs the middle element in $O(1)$, and a list can't provide it.
- **Deletion in a singly linked list needs the predecessor**, since it's the predecessor's `next` that must change. Given only $x$, finding the predecessor takes a linear scan. A doubly linked list stores it directly.
- † **Deleting from a singly linked list in $O(1)$ is possible with a trick:** instead of removing node $x$, copy its *successor's* value into $x$ and remove the successor. This fails for the last node, and it changes which node object holds which value — which matters if other code holds references to nodes. It's LC 237, Delete Node in a Linked List.

!!! tip "Take-Home Lesson"
    Data structure design is a balancing act between operations. The fastest structure for operations A *and* B is often not the fastest for A alone or B alone. Pick representations by listing the operations your algorithm actually performs, and how often.

---

## Lists Are Recursive Objects

Remove the first node of a linked list and what remains is — a smaller linked list. This recursive view is often the cleanest way to design list algorithms: handle the head, recurse on the rest, and trust induction for correctness.

```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ListNode:
    val: int = 0
    next: ListNode | None = None


def length(head: ListNode | None) -> int:
    return 0 if head is None else 1 + length(head.next)


def merge_two_lists(a: ListNode | None, b: ListNode | None) -> ListNode | None:
    """LC 21: merge two sorted lists by relinking their nodes."""
    if a is None or b is None:
        return a or b
    if a.val <= b.val:
        a.next = merge_two_lists(a.next, b)
        return a
    b.next = merge_two_lists(a, b.next)
    return b
```

`merge_two_lists` is correct by induction: the smaller head must come first, and assuming the recursive call correctly merges what remains, attaching it after that head gives a correctly merged list.

The recursive versions are elegant but use $O(n)$ stack space, and Python's recursion limit (about 1000) makes them fail on long lists. In practice, write the iterative version — with the recursive argument in mind.

---

## Core Techniques

### 1. The dummy (sentinel) head

Many list algorithms have an annoying special case: the head itself might change (it gets deleted, or a new node goes before it). A **dummy node** placed before the head turns the head into an ordinary node, so the special case disappears.

```python
def merge_two_lists_iter(a: ListNode | None, b: ListNode | None) -> ListNode | None:
    dummy = tail = ListNode()
    while a and b:
        if a.val <= b.val:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b
    return dummy.next


def remove_elements(head: ListNode | None, val: int) -> ListNode | None:
    """LC 203: delete every node with the given value."""
    dummy = ListNode(0, head)
    prev = dummy
    while prev.next:
        if prev.next.val == val:
            prev.next = prev.next.next      # splice out; don't advance prev
        else:
            prev = prev.next
    return dummy.next
```

Note how `remove_elements` walks with `prev` rather than the current node: in a singly linked list, you delete a node by standing on its predecessor.

### 2. Rewire carefully: save before you overwrite

Every pointer manipulation bug has the same shape: a `next` field is overwritten while it was still the only path to the rest of the list. Before assigning to `x.next`, ask: *is anything reachable only through the old value?* If so, save it first.

**Reversal** is the canonical example:

```python
def reverse_list(head: ListNode | None) -> ListNode | None:
    """LC 206."""
    prev = None
    curr = head
    while curr:
        nxt = curr.next          # 1. save the rest of the list
        curr.next = prev         # 2. reverse this one pointer
        prev, curr = curr, nxt   # 3. advance both
    return prev
```

**Invariant:** `prev` is the head of the already-reversed prefix; `curr` is the head of the untouched suffix. Each iteration moves one node from the suffix to the front of the prefix. When `curr` is `None`, `prev` is the whole reversed list.

When in doubt, draw three boxes and arrows on paper and trace one iteration. Pointer code is much easier to get right by picture than by reasoning in your head.

### 3. Runners: two pointers at different speeds

Arrays let you jump to the middle; lists don't. But two pointers moving at different speeds can compute positions in a single pass.

**Find the middle.** `slow` moves one step, `fast` moves two. When `fast` reaches the end, `slow` has gone half as far.

```python
def middle_node(head: ListNode) -> ListNode:
    """LC 876: second middle for even lengths."""
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```

**The $n$-th node from the end** (LC 19). Advance `fast` $n$ steps first, then move both at the same speed. When `fast` falls off the end, `slow` is $n$ nodes behind it. Starting both at a dummy node leaves `slow` at the *predecessor* of the target, which is exactly where you need to stand to delete it.

```python
def remove_nth_from_end(head: ListNode | None, n: int) -> ListNode | None:
    dummy = ListNode(0, head)
    slow = fast = dummy
    for _ in range(n):
        fast = fast.next
    while fast.next:
        slow, fast = slow.next, fast.next
    slow.next = slow.next.next
    return dummy.next
```

---

## Cycle Detection: Floyd's Tortoise and Hare

A list might loop back on itself. A `set` of visited nodes detects this in $O(n)$ space, but two runners do it in $O(1)$.

**Detection (LC 141).** Move `slow` one step and `fast` two. If there's no cycle, `fast` reaches the end. If there is, both eventually enter the cycle, and from then on `fast` gains exactly one node per step on `slow` — so the gap between them shrinks by one each step and must hit zero. They meet within one lap.

**Finding the entrance (LC 142).** Let $a$ be the distance from the head to the cycle's entrance, $L$ the cycle length, and suppose they meet $b$ steps past the entrance. When they meet, `slow` has walked $a + b$ and `fast` has walked twice that. The extra distance `fast` covered is a whole number of laps:

$$2(a + b) - (a + b) = a + b = kL \quad\Longrightarrow\quad a = kL - b$$

So from the meeting point, walking $a$ more steps means walking $kL - b$ steps — which lands exactly on the entrance (you're $b$ past it; $L - b$ more steps completes the lap, and the extra $(k-1)$ laps change nothing). A pointer starting from the head also reaches the entrance after $a$ steps. Walk both at the same speed; they meet at the entrance.

```python
def detect_cycle(head: ListNode | None) -> ListNode | None:
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            finder = head
            while finder is not slow:
                finder, slow = finder.next, slow.next
            return finder
    return None
```

The same algorithm works on any function iterated from a starting point, $x \to f(x) \to f(f(x)) \to \cdots$, which is how it solves Find the Duplicate Number (LC 287) with $f(i) = \text{nums}[i]$ and Happy Number (LC 202).

---

## Composing Primitives

Harder list problems are usually a few of the primitives above, glued together. Recognizing the pieces is most of the work.

### Reorder list (LC 143): middle + reverse + merge

Rearrange $L_0 \to L_1 \to \cdots \to L_n$ into $L_0 \to L_n \to L_1 \to L_{n-1} \to \cdots$.

```python
def reorder_list(head: ListNode | None) -> None:
    if not head or not head.next:
        return
    # 1. split at the middle
    slow, fast = head, head.next
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    second, slow.next = slow.next, None
    # 2. reverse the second half
    second = reverse_list(second)
    # 3. interleave the two halves
    first = head
    while second:
        first.next, first = second, first.next
        second.next, second = first, second.next
```

The same split-and-reverse approach checks whether a list is a palindrome in $O(1)$ space (LC 234): reverse the second half and compare it against the first.

### Reverse a sublist (LC 92)

Reverse nodes at positions `left` through `right`. Walk a pointer to the node *before* the sublist, then repeatedly take the node right after the sublist's current first node and move it to the front:

```python
def reverse_between(head: ListNode | None, left: int, right: int) -> ListNode | None:
    dummy = ListNode(0, head)
    before = dummy
    for _ in range(left - 1):
        before = before.next
    first = before.next                  # will end up as the sublist's tail
    for _ in range(right - left):
        moved = first.next
        first.next = moved.next
        moved.next = before.next
        before.next = moved
    return dummy.next
```

Reversing in groups of $k$ (LC 25) is this same operation applied to successive blocks.

### Sort a list (LC 148): mergesort

Mergesort is the natural sort for linked lists: splitting uses the middle-finding runners, merging relinks nodes with no extra space, and nothing needs random access. $O(n \log n)$ time. See [Sorting](05_sorting.md#mergesort-divide-and-conquer).

### Merge $k$ sorted lists (LC 23)

Merging lists pairwise, one after another, costs $O(nk)$ for $n$ total nodes. Two better approaches, both $O(n \log k)$: keep the $k$ current heads in a **min-heap** and repeatedly pop the smallest (see [Heaps](09_heaps.md)), or merge lists in pairs like the levels of mergesort.

---

## More Classic Problems

### Intersection of two lists (LC 160)

Two lists merge at some node and share a tail. Let the unshared parts have lengths $a$ and $b$, and the shared tail $c$. A pointer that walks list A and then switches to list B travels $a + c + b$ before reaching the intersection a second time; one that walks B then A travels $b + c + a$. Same distance — so they arrive at the intersection at the same step (or both reach `None` together if there is none).

```python
def get_intersection_node(a: ListNode | None, b: ListNode | None) -> ListNode | None:
    p, q = a, b
    while p is not q:
        p = p.next if p else b
        q = q.next if q else a
    return p
```

### Add two numbers (LC 2)

Digits stored in reverse order are exactly the order in which grade-school addition processes them, least significant first. Walk both lists together, carrying as you go; a dummy head collects the result.

```python
def add_two_numbers(l1: ListNode | None, l2: ListNode | None) -> ListNode | None:
    dummy = tail = ListNode()
    carry = 0
    while l1 or l2 or carry:
        total = carry + (l1.val if l1 else 0) + (l2.val if l2 else 0)
        carry, digit = divmod(total, 10)
        tail.next = tail = ListNode(digit)
        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None
    return dummy.next
```

### Copy a list with random pointers (LC 138)

Each node has an extra `random` pointer to an arbitrary node. The difficulty: when copying node $x$, $x$'s random target may not have been copied yet. The clean fix is a **hash map from original node to copy**: one pass creates all the copies, a second pass wires `next` and `random` through the map. $O(n)$ time and space. (An $O(1)$-extra-space version interleaves each copy right after its original, uses `x.next.random = x.random.next`, then unweaves the lists.)

---

## Design: The LRU Cache (LC 146)

An LRU (least-recently-used) cache with capacity $c$ supports `get(key)` and `put(key, value)` in $O(1)$, evicting the least recently used key when full.

No single structure does this:

- A **hash map** finds a key in $O(1)$, but knows nothing about recency.
- A **list ordered by recency** can move an item to the front and evict from the back in $O(1)$ — *if* you already hold a reference to the node, and *if* it's doubly linked so that the node can unlink itself.

Combine them: the hash map stores, for each key, a pointer to its node in a doubly linked recency list. The map provides the reference; the list provides the $O(1)$ splicing.

```python
class _Node:
    __slots__ = ("key", "val", "prev", "next")

    def __init__(self, key: int = 0, val: int = 0):
        self.key, self.val = key, val
        self.prev: _Node | None = None
        self.next: _Node | None = None


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.nodes: dict[int, _Node] = {}
        self.head, self.tail = _Node(), _Node()   # sentinels: head.next is most recent
        self.head.next, self.tail.prev = self.tail, self.head

    def _unlink(self, node: _Node) -> None:
        node.prev.next, node.next.prev = node.next, node.prev

    def _push_front(self, node: _Node) -> None:
        node.prev, node.next = self.head, self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        node = self.nodes.get(key)
        if node is None:
            return -1
        self._unlink(node)
        self._push_front(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.nodes:
            node = self.nodes[key]
            node.val = value
            self._unlink(node)
        else:
            if len(self.nodes) == self.capacity:
                lru = self.tail.prev
                self._unlink(lru)
                del self.nodes[lru.key]            # why nodes store their key
            node = _Node(key, value)
            self.nodes[key] = node
        self._push_front(node)
```

Two sentinels (`head` and `tail`) mean `_unlink` and `_push_front` never check for `None` — no special cases for the first or last element.

!!! tip "Take-Home Lesson"
    Building algorithms around the right combination of data structures leads to both clean code and good performance. When no single structure supports all the operations you need, look for two that each support half, and link them with pointers.

In production Python, `collections.OrderedDict` implements exactly this design: `move_to_end(key)` and `popitem(last=False)` give an LRU cache in a few lines. In an interview, be ready to build it by hand.

---

## Common Mistakes

1. **Losing the rest of the list.** Overwriting `node.next` before saving it. Always save first.

2. **Forgetting the head can change.** Deleting the first node, inserting before it, or reversing changes which node is the head. Use a dummy node, and return `dummy.next`.

3. **Null-pointer errors in runners.** `fast.next.next` fails if `fast.next` is `None`. The condition `while fast and fast.next` protects both hops.

4. **Comparing values instead of identities.** Two different nodes can hold equal values. Use `is` to compare nodes (intersection, cycle detection), `==` only for values.

5. **Leaving a cycle behind.** After splitting a list, set the end of the first half to `None`; otherwise later code will traverse into the second half or loop forever.

6. **Recursion depth.** A recursive solution on a 10⁵-node list will exceed Python's recursion limit. Prefer iteration.

---

## Practice Problems

| Problem | Technique |
|---|---|
| Reverse Linked List (LC 206) | Three-pointer reversal |
| Merge Two Sorted Lists (LC 21) | Dummy head |
| Remove Nth Node From End (LC 19) | Runners with a gap |
| Middle of the Linked List (LC 876) | Slow / fast |
| Linked List Cycle II (LC 142) | Floyd + entrance argument |
| Delete Node in a Linked List (LC 237) | Copy successor into the node |
| Palindrome Linked List (LC 234) | Middle + reverse + compare |
| Reorder List (LC 143) | Middle + reverse + merge |
| Reverse Linked List II (LC 92) | Move-to-front within a sublist |
| Reverse Nodes in k-Group (LC 25) | Repeated sublist reversal |
| Intersection of Two Linked Lists (LC 160) | Switch heads, equal distances |
| Add Two Numbers (LC 2) | Grade-school addition with carry |
| Copy List with Random Pointer (LC 138) | Hash map old → new |
| Sort List (LC 148) | Mergesort |
| Merge k Sorted Lists (LC 23) | Min-heap of heads |
| LRU Cache (LC 146) | Hash map + doubly linked list |
