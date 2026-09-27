# Algorithm Design Cheat Sheet

A one-page reference for choosing data structures and algorithms. It is organized around the question that should come first in any design: **which operations does my algorithm perform, and how often?** Once you know that, the tables below tell you which structure makes those operations cheap.

Each section links to the chapter that explains the material in depth.

!!! tip "Take-Home Lesson"
    Data structure design is a balancing act. The fastest structure for operations A *and* B is often not the fastest for A alone or B alone. Picking the wrong structure can be disastrous; picking the very best one matters much less, because several good choices usually perform similarly.

---

## Dictionary Operations: The Master Table

Rows are data structures; columns are operations on $n$ stored items. In each column, the **best** cost is in bold. Unless noted, costs are worst case.

**Conventions:** *Delete*, *successor*, and *predecessor* are given a reference (index or node) to the item, so they don't include the cost of finding it. *Successor* / *predecessor* mean the next item in **sorted** order, not physical order. $h$ is the height of a tree.

| Structure | Access $i$-th | Search by key | Insert | Delete | Min / Max | Successor / Predecessor | Build from $n$ items | Iterate in sorted order |
|---|---|---|---|---|---|---|---|---|
| Unsorted array (`list`) | **$O(1)$** | $O(n)$ | **$O(1)$** ¹ | **$O(1)$** ² | $O(n)$ | $O(n)$ | **$O(n)$** | $O(n \log n)$ |
| Sorted array | **$O(1)$** | $O(\log n)$ | $O(n)$ | $O(n)$ | **$O(1)$** | **$O(1)$** | $O(n \log n)$ | **$O(n)$** |
| Singly linked list | $O(n)$ | $O(n)$ | **$O(1)$** | $O(n)$ ³ | $O(n)$ | $O(n)$ | **$O(n)$** | $O(n \log n)$ |
| Doubly linked list | $O(n)$ | $O(n)$ | **$O(1)$** | **$O(1)$** | $O(n)$ | $O(n)$ | **$O(n)$** | $O(n \log n)$ |
| Sorted doubly linked list | $O(n)$ | $O(n)$ | $O(n)$ | **$O(1)$** | **$O(1)$** | **$O(1)$** | $O(n \log n)$ | **$O(n)$** |
| Hash table (`dict`, `set`) | — | **$O(1)$** ⁴ | **$O(1)$** ⁴ | **$O(1)$** ⁴ | $O(n)$ | $O(n)$ | **$O(n)$** ⁴ | $O(n \log n)$ |
| Binary search tree (unbalanced) | $O(h)$ ⁵ | $O(h)$ | $O(h)$ | $O(h)$ | $O(h)$ | $O(h)$ | $O(n h)$ | **$O(n)$** |
| Balanced BST (AVL, red–black, `SortedList`) | $O(\log n)$ ⁵ | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ ⁶ | $O(\log n)$ | $O(n \log n)$ | **$O(n)$** |
| Binary heap (`heapq`) | — | $O(n)$ | $O(\log n)$ | $O(\log n)$ ⁷ | **$O(1)$** min only | $O(n)$ | **$O(n)$** | $O(n \log n)$ |

1. Amortized: append to the end of a dynamic array. Inserting at a *specific* position costs $O(n)$.
2. Overwrite the deleted item with the last one and shrink. Order is not preserved; if it must be, delete costs $O(n)$.
3. The *predecessor's* pointer must change, and finding it takes $O(n)$. Copying the successor's value into the node gives $O(1)$ except for the last node (LC 237).
4. Expected, assuming a good hash function. The worst case is $O(n)$ per operation.
5. By rank only if each node stores its subtree size (an order-statistic tree). `sortedcontainers.SortedList` supports indexing.
6. $O(1)$ if a pointer to the extreme element is cached and maintained.
7. Delete-min. Deleting an arbitrary item needs its index; `heapq` doesn't track indices, so use lazy deletion instead.

**Reading the table.** No row is bold everywhere, which is exactly the point:

- **Hash tables** win at exact-key lookup and update, and are useless for anything involving order.
- **Sorted arrays** win at order queries (min, successor, sorted iteration, binary search) and lose at updates.
- **Heaps** win at "give me the minimum" and nothing else — which is often all you need.
- **Balanced BSTs** are never the fastest at any single operation, but they are the only structure with **no bad column**. Use one when you need both updates *and* ordered queries.

See: [Complexity Analysis](common_patterns/01_complexity_analysis.md), [Linked Lists](common_patterns/06_linked_lists.md#contiguous-vs-linked), [Heaps](common_patterns/09_heaps.md#how-should-a-priority-queue-be-built), [Trees](common_patterns/10_trees.md#binary-search-trees).

---

## Containers and Specialized Structures

Structures built for a narrower set of operations, and the best cost for each.

| Structure | Python | Operations and costs | Use it when |
|---|---|---|---|
| Stack | `list` | push, pop, peek: **$O(1)$** ¹ | Nesting, undo, DFS, "most recent unresolved item" |
| Queue | `collections.deque` | enqueue, dequeue, peek: **$O(1)$** | BFS, FIFO processing, fairness |
| Deque | `collections.deque` | push / pop at either end: **$O(1)$**; index: $O(n)$ | Sliding windows, 0-1 BFS |
| Monotonic stack / deque | `list` / `deque` | **$O(1)$** amortized per element | Next greater / smaller element, sliding window max / min |
| Priority queue | `heapq` | push, pop-min: $O(\log n)$; peek: **$O(1)$**; heapify: **$O(n)$** | Repeatedly extract the best item; top-$k$; Dijkstra, Prim |
| Two heaps | `heapq` ×2 | insert: $O(\log n)$; median: **$O(1)$** | Running median, split at an order statistic |
| Union-find | custom | find, union: **$O(\alpha(n))$** amortized ² | Dynamic connectivity, grouping, Kruskal |
| Trie | nested `dict` | insert, search, prefix query: **$O(L)$** for a key of length $L$ | Prefix queries, autocomplete, word search on grids |
| Bit vector | `int` | member, add, remove: **$O(1)$**; union, intersection: $O(n / w)$ ³ | Small fixed universe; sets as dictionary keys |
| Counter / multiset | `collections.Counter` | add, remove, count: **$O(1)$** expected | Frequencies, anagrams, window contents |
| Ordered map / multiset | `sortedcontainers.SortedList` | add, remove, rank, successor: $O(\log n)$ | Sliding window median, "closest value" queries, events |

1. Amortized for `list.append` / `list.pop()`.
2. $\alpha$ is the inverse Ackermann function: at most 4 for any realistic $n$.
3. $w$ is the machine word size; Python integers are arbitrary precision, so large unions cost time proportional to the size of the integer.

See: [Stacks & Queues](common_patterns/07_stacks_queues.md), [Heaps](common_patterns/09_heaps.md), [Trie & Union Find](common_patterns/12_trie_union_find.md), [Bit Manipulation](common_patterns/04_bit_manipulation.md#bit-vectors-integers-as-sets).

---

## Range Queries

Structures for questions about contiguous ranges of an array: sums, minimums, counts. The right choice depends on whether the array **changes** between queries. Best cost in each column in bold.

| Structure | Build | Point update | Range query | Range update | Supports |
|---|---|---|---|---|---|
| Prefix-sum array | **$O(n)$** | $O(n)$ | **$O(1)$** | $O(n)$ | Sums (any invertible operation) |
| Difference array | **$O(n)$** | **$O(1)$** | $O(n)$ ¹ | **$O(1)$** | Many range additions, one final read |
| Sparse table | $O(n \log n)$ | — | **$O(1)$** | — | Min, max, gcd (idempotent operations), static arrays |
| Fenwick tree (BIT) | **$O(n)$** | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ ² | Sums with updates |
| Segment tree | **$O(n)$** | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ ³ | Any associative operation, with updates |

1. Reading values requires a prefix sum over the differences.
2. Using the range-update / point-query variant, or two trees for range update and range query.
3. With lazy propagation.

**Rule of thumb:** static array → prefix sums (sums) or sparse table (min / max). Updates interleaved with queries → Fenwick tree (sums) or segment tree (anything else). Offline batch of range additions → difference array.

A Fenwick tree is short enough to write from memory. Index $i$ is responsible for the range ending at $i$ whose length is the lowest set bit of $i$ (see [Bit Manipulation](common_patterns/04_bit_manipulation.md#the-lowest-set-bit)):

```python
class FenwickTree:
    """Point update and prefix sum in O(log n). Indices are 0-based externally."""

    def __init__(self, n: int) -> None:
        self.tree = [0] * (n + 1)

    def add(self, i: int, delta: int) -> None:
        i += 1
        while i < len(self.tree):
            self.tree[i] += delta
            i += i & -i                     # move to the next range covering i

    def prefix_sum(self, i: int) -> int:
        """Sum of the first i elements (indices 0 .. i-1)."""
        total = 0
        while i > 0:
            total += self.tree[i]
            i -= i & -i                     # drop the range just added
        return total

    def range_sum(self, lo: int, hi: int) -> int:
        """Sum of indices lo .. hi-1."""
        return self.prefix_sum(hi) - self.prefix_sum(lo)
```

See: [Prefix Sums](common_patterns/03_two_pointers_sliding_window.md#prefix-sums), [Intervals: Difference Arrays](common_patterns/08_intervals.md#difference-arrays-sweep-lines-on-integer-grids).

---

## Which Structure Do I Need?

Start from the operations the algorithm performs; pick the simplest structure that makes all of them fast.

| I need to... | Use | Cost |
|---|---|---|
| Look up, insert, delete by exact key | Hash map / set | $O(1)$ expected |
| Count occurrences | `Counter` | $O(1)$ expected per update |
| Repeatedly take the smallest (or largest) item, with insertions | Binary heap | $O(\log n)$ |
| Keep the $k$ best items of a stream | Size-$k$ heap | $O(\log k)$ per item |
| Insert, delete, **and** ask ordered questions (successor, $k$-th, range) | Balanced BST / `SortedList` | $O(\log n)$ |
| Answer "what's nearest to $x$?" on fixed data | Sorted array + `bisect` | $O(\log n)$ |
| Process in LIFO order / match nested structure | Stack | $O(1)$ |
| Process in FIFO order / explore by distance | Queue (`deque`) | $O(1)$ |
| Find the next greater / smaller element for all items | Monotonic stack | $O(n)$ total |
| Max / min of every sliding window | Monotonic deque | $O(n)$ total |
| Merge groups and ask "same group?" | Union-find | $O(\alpha(n))$ |
| Query words by prefix | Trie | $O(L)$ |
| Range sums with updates | Fenwick tree | $O(\log n)$ |
| Evict the least recently used item | Hash map + doubly linked list (`OrderedDict`) | $O(1)$ |
| Represent a subset of $\le 64$ items compactly | Bitmask (`int`) | $O(1)$ |

---

## Algorithm Quick Reference

### Sorting and searching

| Task | Algorithm | Time | Notes |
|---|---|---|---|
| Sort anything | Timsort (`sorted`, `list.sort`) | $O(n \log n)$ | Stable; $O(n)$ on sorted runs |
| Sort small integer keys | Counting / radix sort | $O(n + k)$ | Beats the comparison lower bound |
| Search sorted data | Binary search (`bisect`) | $O(\log n)$ | Also: first / last occurrence, insertion point |
| Minimize a value with a monotone feasibility test | Binary search on the answer | $O(\text{check} \cdot \log R)$ | Range $R$ of possible answers |
| $k$-th smallest | Quickselect | $O(n)$ expected | Or a size-$k$ heap, $O(n \log k)$ |
| Merge $k$ sorted lists | Heap of heads | $O(n \log k)$ | |
| Count inversions | Mergesort with counting | $O(n \log n)$ | |

### Graphs

| Problem | Algorithm | Time | Requirements |
|---|---|---|---|
| Reachability, connected components | BFS / DFS | $O(V + E)$ | — |
| Shortest path, unweighted | BFS | $O(V + E)$ | — |
| Shortest path, weights 0 / 1 | 0-1 BFS (deque) | $O(V + E)$ | — |
| Shortest path, DAG | Relax in topological order | $O(V + E)$ | Acyclic; any weights |
| Shortest path, non-negative weights | Dijkstra (heap) | $O(E \log V)$ | No negative edges |
| Shortest path, negative weights / at most $k$ edges | Bellman–Ford | $O(VE)$ / $O(kE)$ | Detects negative cycles |
| All-pairs shortest paths | Floyd–Warshall | $O(V^3)$ | $V \lesssim 400$ |
| Minimum spanning tree | Kruskal (union-find) / Prim (heap) | $O(E \log E)$ / $O(E \log V)$ | Connected, undirected |
| Ordering with dependencies | Topological sort (Kahn / DFS) | $O(V + E)$ | Acyclic |
| Cycle detection | DFS (3 colors) / union-find | $O(V + E)$ | Directed / undirected |
| Two-coloring (bipartite?) | BFS / DFS coloring | $O(V + E)$ | — |
| Strongly connected components | Kosaraju / Tarjan | $O(V + E)$ | Directed |
| Bridges, articulation points | DFS low-link | $O(V + E)$ | Undirected |

See: [Sorting](common_patterns/05_sorting.md), [Binary Search](common_patterns/02_binary_search.md), [Graphs](common_patterns/11_graphs.md#which-shortest-path-algorithm).

### Design paradigms

| Paradigm | Use when | Correctness comes from | Chapter |
|---|---|---|---|
| Sorting first | Pairs, duplicates, nearness, intervals | Order makes neighbors meaningful | [Sorting](common_patterns/05_sorting.md) |
| Two pointers / sliding window | Pairs or subarrays with a monotone condition | An elimination argument | [Two Pointers](common_patterns/03_two_pointers_sliding_window.md) |
| Divide and conquer | The problem splits into independent halves | Induction; master theorem for cost | [Complexity](common_patterns/01_complexity_analysis.md#recurrences-and-divide-and-conquer) |
| Greedy | A local choice provably belongs to some optimum | Exchange argument, stays-ahead, or matching a lower bound | [Greedy](common_patterns/14_greedy.md) |
| Dynamic programming | Optimal / counting problems with overlapping subproblems | A correct recurrence over few states | [Dynamic Programming](common_patterns/15_dynamic_programming.md) |
| Backtracking | Enumerate or search all configurations; small $n$ | Exhaustive enumeration + pruning | [Backtracking](common_patterns/13_backtracking.md) |
| Graph modeling | Relationships, states, dependencies | A classical algorithm on a well-designed graph | [Graphs](common_patterns/11_graphs.md#design-graphs-not-algorithms) |

---

## From Constraints to Complexity

Budget roughly $10^7$–$10^8$ simple operations per second in Python. The input size usually tells you the intended complexity:

| $n$ up to | Target complexity | Typical techniques |
|---|---|---|
| 10 | $O(n!)$ | Permutations, brute force |
| 20 | $O(2^n)$, $O(n \cdot 2^n)$ | Subsets, bitmask DP, backtracking |
| 40 | $O(2^{n/2})$ | Meet in the middle |
| 500 | $O(n^3)$ | Floyd–Warshall, interval DP |
| 5,000 | $O(n^2)$ | 2-D DP, all pairs |
| $10^5$–$10^6$ | $O(n \log n)$, $O(n)$ | Sorting, heaps, binary search, two pointers, hashing, BFS / DFS |
| $10^9$ and beyond | $O(\log n)$, $O(\sqrt n)$, $O(1)$ | Binary search on the answer, math |

See: [Complexity Analysis](common_patterns/01_complexity_analysis.md#estimation-from-constraints-to-complexity).

---

## Problem Signals

| If the problem mentions... | Think of |
|---|---|
| Sorted input, "find a pair / triplet" | Two pointers, binary search |
| "Minimum possible maximum", "at least / at most" with large bounds | Binary search on the answer |
| "Longest / shortest subarray or substring such that..." | Sliding window (monotone condition) or prefix sums |
| "Subarray sum equals $k$", negative numbers | Prefix sums + hash map |
| "Next greater / smaller", "span", histogram | Monotonic stack |
| "$k$ largest / smallest / closest", "median of a stream" | Heap(s) |
| Overlapping ranges, meetings, "minimum rooms" | Sort by endpoint, sweep line |
| "All combinations / permutations / subsets", $n \le 20$ | Backtracking |
| "Number of ways", "minimum cost", "longest ..." with choices | Dynamic programming |
| "Shortest path", "fewest steps", grid moves | BFS (unweighted) / Dijkstra (weighted) |
| Prerequisites, ordering with dependencies | Topological sort |
| "Connected", "same group", merging accounts | Union-find or DFS |
| Prefixes, dictionary of words, word search | Trie |
| "Appears once / twice", XOR, subsets as masks | Bit manipulation |
| "Modulo $10^9 + 7$", "how many ways" with large $n$ | Combinatorics + DP |

---

## Python Performance Traps

| Looks cheap | Actually costs | Use instead |
|---|---|---|
| `list.pop(0)`, `list.insert(0, x)` | $O(n)$ | `deque.popleft()`, `deque.appendleft(x)` |
| `x in some_list` | $O(n)$ | `x in some_set` |
| `s += piece` in a loop | $O(n^2)$ total | `"".join(pieces)` |
| `arr[1:]` in recursion | $O(n)$ per call | Pass indices |
| `sorted()` inside a loop | $O(n \log n)$ per iteration | Sort once, or use a heap / `SortedList` |
| `min(arr)` / `max(arr)` in a loop | $O(n)$ per iteration | Heap, monotonic deque, or running value |
| Deep recursion (> ~1000 levels) | `RecursionError` | Explicit stack, or `sys.setrecursionlimit` |
| `heapq` with non-comparable items on ties | `TypeError` | `(priority, counter, item)` tuples |

See: [The Python Cost Model](common_patterns/01_complexity_analysis.md#the-python-cost-model).
