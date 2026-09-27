# Heaps & Priority Queues

Many algorithms need to process items in order of importance: the cheapest edge, the earliest deadline, the closest unexplored vertex, the next event in a simulation. If all the items were known in advance, you could sort them once. But usually they aren't — new items keep arriving *while* you are processing old ones, and re-sorting after each arrival would be ruinous.

A **priority queue** is the data structure for this situation. It supports three operations:

- **Insert** an item with a key.
- **Find-min**: return the item with the smallest key.
- **Delete-min**: remove and return that item.

(Or max instead of min — the choice is symmetric.) The **binary heap** implements all three in $O(\log n)$ or better, with a representation so compact it needs no pointers at all.

!!! tip "Take-Home Lesson"
    Building algorithms around the right abstract data type — dictionaries, priority queues — leads to both clean structure and good performance. Many famous algorithms (Dijkstra, Prim, Huffman coding, heapsort, event simulation) are "a priority queue plus a loop."

---

## How Should a Priority Queue Be Built?

Before looking at heaps, consider the obvious alternatives. The table has one subtlety: find-min can be $O(1)$ for *every* structure, by caching a pointer to the current minimum and updating it on each insert and delete (a delete must then find the new minimum, which is where the real cost goes).

| | Unsorted array | Sorted array | Balanced BST | Binary heap |
|---|---|---|---|---|
| Insert | $O(1)$ | $O(n)$ | $O(\log n)$ | $O(\log n)$ |
| Find-min | $O(1)$ (cached) | $O(1)$ | $O(1)$ (cached) | $O(1)$ |
| Delete-min | $O(n)$ | $O(1)$ (min stored at the end) | $O(\log n)$ | $O(\log n)$ |
| Build from $n$ items | $O(n)$ | $O(n \log n)$ | $O(n \log n)$ | $O(n)$ |

A balanced search tree matches the heap asymptotically, and supports more operations besides (search, successor, delete arbitrary item). So why heaps? Because they are dramatically simpler, use no pointers, build in linear time, and are several times faster in practice. When all you need is "give me the minimum," a heap is the right tool.

---

## The Binary Heap

A heap maintains a **partial order**: weaker than sorted order (so it's cheap to maintain) but stronger than no order (so the minimum is always easy to find).

> **Heap property:** every node's key is less than or equal to the keys of its children.

So the root holds the minimum, every root-to-leaf path is sorted, and — importantly — *nothing* is promised about the order between siblings or cousins.

### An implicit tree

A heap is a **complete** binary tree: every level is full except possibly the last, which is filled from the left. Complete trees can be stored in an array with no pointers: put the root at index 0 and lay out the levels left to right.

```text
            1                    index:  0  1  2  3  4  5  6  7
         /     \                 value:  1  3  2  7  4  5  9  8
        3       2
       / \     / \               children of i:  2i + 1, 2i + 2
      7   4   5   9              parent of i:    (i - 1) // 2
     /
    8
```

Because the tree is complete, an $n$-element heap has height $\lfloor \log_2 n \rfloor$. That's what makes every operation logarithmic.

The price of the implicit representation is inflexibility: you can't store an arbitrary tree shape without wasting space, and you can't move a subtree by changing one pointer. Fine for heaps — fatal for search trees.

??? question "Stop and Think: Who's where in the heap?"
    **Problem:** How do you efficiently search a heap for a particular key $k$?

    **Solution:** You can't. A heap is not a search tree: knowing that $k$ is larger than a node tells you nothing about which of its two subtrees to explore. About half of the elements are leaves, and the heap property says nothing about their relative order. Searching takes $O(n)$. If you need both "find the minimum" and "find key $k$" quickly, you need a balanced BST — or a heap *plus* a hash map from key to position.

### Insert: sift up

Put the new element in the first free slot (the end of the array). The shape is right, but the new element might be smaller than its parent. Swap it upward until it isn't. Each swap fixes the parent–child pair and moves the problem one level up: $O(\log n)$.

### Delete-min: sift down

Remove the root, move the last element into its place, and swap it downward with its **smaller** child until it's no larger than both children. Swapping with the smaller child is essential: that child becomes the parent of the other, so it had better be the smaller of the two. Again $O(\log n)$.

```python
class MinHeap:
    def __init__(self) -> None:
        self.a: list[int] = []

    def __len__(self) -> int:
        return len(self.a)

    def peek(self) -> int:
        return self.a[0]

    def push(self, x: int) -> None:
        a = self.a
        a.append(x)
        i = len(a) - 1
        while i > 0 and a[(i - 1) // 2] > a[i]:          # sift up
            parent = (i - 1) // 2
            a[i], a[parent] = a[parent], a[i]
            i = parent

    def pop(self) -> int:
        a = self.a
        top = a[0]
        last = a.pop()
        if a:
            a[0] = last
            self._sift_down(0)
        return top

    def _sift_down(self, i: int) -> None:
        a, n = self.a, len(self.a)
        while True:
            smallest = i
            for child in (2 * i + 1, 2 * i + 2):
                if child < n and a[child] < a[smallest]:
                    smallest = child
            if smallest == i:
                return
            a[i], a[smallest] = a[smallest], a[i]
            i = smallest
```

### Building a heap in linear time

Inserting $n$ items one at a time costs $O(n \log n)$. But there's a faster way. Dump all the items into the array in any order. The leaves — the last half of the array — are already valid one-element heaps. Walk backward through the remaining nodes, sifting each one down; when you reach node $i$, both of its subtrees are already valid heaps, which is exactly the situation sift-down repairs.

```python
def build_heap(items: list[int]) -> MinHeap:
    h = MinHeap()
    h.a = list(items)
    for i in range(len(h.a) // 2 - 1, -1, -1):
        h._sift_down(i)
    return h
```

$n/2$ calls to an $O(\log n)$ procedure suggests $O(n \log n)$. But that bound is loose: sift-down costs time proportional to the node's **height**, and most nodes are near the bottom. About $n/4$ nodes have height 1, $n/8$ have height 2, and in general $n/2^{h+1}$ have height $h$:

$$\sum_{h=0}^{\log n} \frac{n}{2^{h+1}} \cdot h \;=\; \frac{n}{2} \sum_{h \ge 0} \frac{h}{2^h} \;\le\; \frac{n}{2} \cdot 2 \;=\; n$$

The $h$ in the numerator is crushed by the $2^h$ in the denominator, and the sum converges to a constant. **Heap construction is $O(n)$.** It's another free lunch courtesy of a geometric-flavored series.

### Heapsort

Build a heap, then delete-min $n$ times. This is just **selection sort with a better data structure**: selection sort repeatedly finds the minimum by scanning in $O(n)$; heapsort finds it in $O(\log n)$. Worst-case $O(n \log n)$, and it can run in place. See [Sorting](05_sorting.md#heapsort-selection-sort-with-the-right-data-structure).

---

## Python's `heapq`

`heapq` implements a **min-heap** as functions operating on a plain `list`:

```python
import heapq

h: list[int] = []
heapq.heappush(h, 5)             # O(log n)
heapq.heappush(h, 1)
heapq.heappush(h, 3)
h[0]                             # peek at the min: 1, O(1)
heapq.heappop(h)                 # remove and return the min: 1, O(log n)

data = [9, 4, 7, 1]
heapq.heapify(data)              # in place, O(n)

heapq.heappushpop(h, 2)          # push, then pop: faster than the two calls
heapq.heapreplace(h, 8)          # pop, then push: heap size unchanged

heapq.nsmallest(2, [9, 4, 7, 1])             # [1, 4], O(n log k)
heapq.nlargest(2, [9, 4, 7, 1])              # [9, 7]
list(heapq.merge([1, 4, 9], [2, 3, 10]))     # lazy k-way merge of sorted inputs
```

### Max-heaps

`heapq` is a min-heap. The standard trick for a max-heap is to **negate the keys** on the way in and out:

```python
maxh: list[int] = []
for x in [3, 1, 4, 1, 5]:
    heapq.heappush(maxh, -x)
largest = -heapq.heappop(maxh)     # 5
```

(Python 3.14 also adds `heapq.heappush_max`, `heappop_max`, and `heapify_max`, which avoid the negation.)

### Ordering by key, and ties

Push tuples: they compare lexicographically, so `(priority, item)` orders by priority. If two priorities tie, Python compares the items — which crashes if the items aren't comparable (e.g., `ListNode` objects). Insert a **tiebreaker** that is always unique:

```python
from itertools import count

tiebreak = count()
tasks: list[tuple[int, int, object]] = []
heapq.heappush(tasks, (2, next(tiebreak), object()))
heapq.heappush(tasks, (2, next(tiebreak), object()))   # no comparison of objects needed
```

A monotonically increasing counter also makes the heap FIFO among equal priorities — a stable priority queue.

---

## Pattern 1: The $k$ Best of $n$

To find the $k$ largest elements, keep a **min-heap of size $k$** holding the best $k$ seen so far. Its root is the *smallest* of those $k$ — the one to evict when something better arrives.

```python
def find_kth_largest(nums: list[int], k: int) -> int:
    """LC 215."""
    heap = nums[:k]
    heapq.heapify(heap)
    for x in nums[k:]:
        if x > heap[0]:
            heapq.heapreplace(heap, x)     # evict the weakest of the current top k
    return heap[0]
```

**Invariant:** after processing a prefix, `heap` holds the $k$ largest elements of that prefix. **Time:** $O(n \log k)$, **space:** $O(k)$ — and it works on a stream, never holding more than $k$ items.

It may seem backward that "$k$ largest" uses a **min**-heap. The heap exists to answer one question quickly: *which of my current candidates should be thrown out?* — and that's the smallest one.

| Approach for $k$-th largest | Time | Space | Notes |
|---|---|---|---|
| Sort | $O(n \log n)$ | $O(n)$ | Simplest |
| Size-$k$ min-heap | $O(n \log k)$ | $O(k)$ | Streams; best when $k \ll n$ |
| Heapify all, pop $k$ times | $O(n + k \log n)$ | $O(n)$ | |
| Quickselect | $O(n)$ expected | $O(1)$ | Fastest; see [Sorting](05_sorting.md#selection-the-k-th-smallest-element) |

The same pattern handles K Closest Points (LC 973; a max-heap of size $k$ on distance, via negation), Top K Frequent Elements (LC 347; heap over `Counter` items), and Kth Largest Element in a Stream (LC 703).

---

## Pattern 2: Merging Sorted Streams

To merge $k$ sorted lists with $n$ total elements (LC 23), keep a heap of the $k$ current heads. Pop the smallest, emit it, and push its successor from the same list. The heap never holds more than $k$ items.

```python
def merge_k_sorted(lists: list[list[int]]) -> list[int]:
    heap = [(lst[0], i, 0) for i, lst in enumerate(lists) if lst]
    heapq.heapify(heap)
    result = []
    while heap:
        val, i, j = heapq.heappop(heap)
        result.append(val)
        if j + 1 < len(lists[i]):
            heapq.heappush(heap, (lists[i][j + 1], i, j + 1))
    return result
```

**Time:** $O(n \log k)$. The list index `i` in each tuple doubles as a tiebreaker. Smallest Range Covering Elements from K Lists (LC 632) is a variation: the heap holds one element per list, and the range is `[heap min, running max]`.

---

## Pattern 3: Best-First Enumeration of a Frontier

Some problems ask for the $k$ smallest of a set of candidates that is far too large to build — but that has **order structure**: you can tell which candidates must come after which.

An airline wanted the cheapest valid two-leg fare between two cities. Each leg had its own sorted list of fares, $X$ and $Y$, and a black-box rule checker decided whether a particular combination was legal. The cheapest *legal* fare might be far down the list of $|X| \cdot |Y|$ combinations, and building and sorting all of them was too slow when the answer was usually near the top.

The key observation: if both lists are sorted, the pair $(i, j)$ is never more expensive than $(i + 1, j)$ or $(i, j + 1)$. So there's no need to consider those two until $(i, j)$ has been examined. Start the priority queue with just $(0, 0)$. Each time you pop a pair, push its two successors. Pairs come out in exactly increasing order of cost, and you stop as soon as you find what you want — having generated only a thin **frontier** of candidates.

This is **Find K Pairs with Smallest Sums** (LC 373). One detail: pair $(i, j)$ can be reached from both $(i - 1, j)$ and $(i, j - 1)$. Either keep a `seen` set, or use a trick that gives every pair a unique parent: seed the heap with $(i, 0)$ for every $i$, and only ever step to $(i, j + 1)$.

```python
def k_smallest_pairs(xs: list[int], ys: list[int], k: int) -> list[list[int]]:
    if not xs or not ys:
        return []
    heap = [(x + ys[0], i, 0) for i, x in enumerate(xs[:k])]
    heapq.heapify(heap)
    result = []
    while heap and len(result) < k:
        _, i, j = heapq.heappop(heap)
        result.append([xs[i], ys[j]])
        if j + 1 < len(ys):
            heapq.heappush(heap, (xs[i] + ys[j + 1], i, j + 1))
    return result
```

**Time:** $O(k \log k)$, independent of the lengths of the input lists. **Kth Smallest Element in a Sorted Matrix** (LC 378) and **Ugly Number II** (LC 264) use the same idea.

!!! tip "Take-Home Lesson"
    When the candidate set is huge but partially ordered — every candidate has "successors" that can't be better — don't generate it. Expand it lazily from the best candidate, with a priority queue holding the frontier. This is the same idea as Dijkstra's algorithm, and it lets you stop the moment you have your answer.

---

## Pattern 4: Two Heaps

To maintain the **median** of a growing stream (LC 295), split the elements into a lower half and an upper half:

- `low`: a **max**-heap holding the smaller half.
- `high`: a **min**-heap holding the larger half.

Maintain two invariants: every element of `low` is at most every element of `high`, and the sizes differ by at most one (with `low` allowed the extra element). Then the median is at the top of `low`, or the average of both tops.

```python
class MedianFinder:
    def __init__(self) -> None:
        self.low: list[int] = []    # max-heap via negation
        self.high: list[int] = []   # min-heap

    def add_num(self, x: int) -> None:
        # Route through low so the ordering invariant holds, then rebalance sizes.
        heapq.heappush(self.high, -heapq.heappushpop(self.low, -x))
        if len(self.high) > len(self.low):
            heapq.heappush(self.low, -heapq.heappop(self.high))

    def find_median(self) -> float:
        if len(self.low) > len(self.high):
            return -self.low[0]
        return (-self.low[0] + self.high[0]) / 2
```

`add_num` is $O(\log n)$ and `find_median` is $O(1)$. The same two-heap split answers any "running $k$-th order statistic" question, and appears in scheduling problems like IPO (LC 502), where one heap holds projects you can't afford yet (keyed by cost) and another holds those you can (keyed by profit).

---

## Pattern 5: Greedy Scheduling

Greedy algorithms repeatedly take "the best available option," and a priority queue is how you find it fast.

**Reorganize String** (LC 767): rearrange characters so no two adjacent ones are equal. Greedily place the most frequent remaining character that differs from the previous one. A max-heap of `(−count, char)` gives that character in $O(\log \Sigma)$; hold back the character just used for one step so it can't be picked twice in a row.

```python
from collections import Counter


def reorganize_string(s: str) -> str:
    heap = [(-c, ch) for ch, c in Counter(s).items()]
    heapq.heapify(heap)
    result: list[str] = []
    held: tuple[int, str] | None = None          # the char used last step
    while heap:
        count, ch = heapq.heappop(heap)
        result.append(ch)
        if held:
            heapq.heappush(heap, held)
        held = (count + 1, ch) if count + 1 < 0 else None
    return "".join(result) if len(result) == len(s) else ""
```

Other greedy-with-heap problems: Task Scheduler (LC 621), Meeting Rooms II (a heap of end times — see [Intervals](08_intervals.md#partitioning-how-many-rooms-lc-253)), Minimum Cost to Connect Sticks (LC 1167, which is Huffman coding), and, most importantly, **Dijkstra's shortest paths** and **Prim's minimum spanning tree** (see [Graphs](11_graphs.md)).

---

## Lazy Deletion

`heapq` can't delete an arbitrary element or change a key. The standard workaround is **lazy deletion**: leave stale entries in the heap, and discard them when they surface at the top.

```python
def top_valid(heap: list[tuple[int, int]], is_stale) -> tuple[int, int] | None:
    while heap and is_stale(heap[0]):
        heapq.heappop(heap)
    return heap[0] if heap else None
```

To "update" a key, push a new entry and mark the old one stale (for example, by checking against a dictionary of current values). Each entry is pushed once and popped at most once, so the amortized cost stays $O(\log n)$ per operation; the heap may just grow larger than the live set. Dijkstra's algorithm in Python is almost always written this way.

??? question "Stop and Think: Is the $k$-th smallest at least $x$?"
    **Problem:** Given an array-based min-heap of $n$ elements and a value $x$, decide whether the $k$-th smallest element is $\ge x$, in $O(k)$ time — independent of $n$.

    **Two correct but slow ideas:** pop $k$ times, $O(k \log n)$. Or note the $k$-th smallest must lie in the top $k$ levels and scan them, $O(\min(n, 2^k))$.

    **The $O(k)$ idea:** you don't need to *find* the $k$-th smallest, only to count elements below $x$. Do a DFS from the root that only descends through nodes $< x$ (by the heap property, everything below a node $\ge x$ is also $\ge x$), and stop as soon as $k$ such nodes have been found. Each counted node causes at most two children to be examined, so at most $2k + 1$ nodes are visited.

    ```python
    def kth_smallest_at_least(heap: list[int], k: int, x: int) -> bool:
        count = 0
        stack = [0]
        while stack and count < k:
            i = stack.pop()
            if i < len(heap) and heap[i] < x:
                count += 1
                stack.extend((2 * i + 1, 2 * i + 2))
        return count < k          # fewer than k elements are below x
    ```

---

## Common Mistakes

1. **Min vs. max confusion.** `heapq` is a min-heap. For "$k$ largest," use a min-heap of size $k$; for a max-heap, negate keys.

2. **Uncomparable ties.** `(priority, node)` tuples crash when priorities tie and nodes don't define `<`. Add a counter between them.

3. **Treating the heap list as sorted.** Only `h[0]` is meaningful. `h[1]` is *not* the second smallest; `h[-1]` is *not* the largest.

4. **Mutating keys in place.** Changing an element's priority inside the list silently breaks the heap property. Push a new entry and lazily delete the old one.

5. **Building with repeated pushes.** $n$ calls to `heappush` cost $O(n \log n)$; `heapify` costs $O(n)$.

6. **Using `nsmallest`/`nlargest` for $k$ close to $n$.** For large $k$ they're slower than just sorting; for $k = 1$, use `min`/`max`.

---

## Practice Problems

| Problem | Pattern |
|---|---|
| Kth Largest Element in an Array (LC 215) | Size-$k$ min-heap (or quickselect) |
| Kth Largest Element in a Stream (LC 703) | Size-$k$ min-heap |
| Last Stone Weight (LC 1046) | Max-heap simulation |
| K Closest Points to Origin (LC 973) | Size-$k$ max-heap |
| Top K Frequent Elements (LC 347) | Heap over counts |
| Merge k Sorted Lists (LC 23) | $k$-way merge |
| Find K Pairs with Smallest Sums (LC 373) | Best-first frontier |
| Kth Smallest Element in a Sorted Matrix (LC 378) | Best-first frontier |
| Find Median from Data Stream (LC 295) | Two heaps |
| IPO (LC 502) | Two heaps, greedy |
| Reorganize String (LC 767) | Greedy max-heap with hold-back |
| Task Scheduler (LC 621) | Greedy max-heap / counting |
| Smallest Range Covering Elements from K Lists (LC 632) | $k$-way merge + running max |
| Sliding Window Median (LC 480) | Two heaps + lazy deletion |
