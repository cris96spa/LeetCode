# Sorting

Sorting is the most thoroughly studied problem in computer science, and for good reason. It is the basic building block of countless algorithms: once data is sorted, searching becomes logarithmic, duplicates become adjacent, and closest pairs become neighbors (see [Two Pointers & Sliding Window](03_two_pointers_sliding_window.md#sorting-as-a-building-block)). A rule of thumb worth adopting: **when stuck on an array problem, ask what would become easy if the input were sorted.**

Sorting is also the best showcase of algorithm design paradigms. Every major technique produces a good sorting algorithm: incremental insertion gives insertion sort, data structures give heapsort, divide and conquer gives mergesort, randomization gives quicksort, and bucketing gives distribution sort. Studying them together is studying algorithm design in miniature.

In practice, you will almost never implement a sort — Python's built-in is excellent. What you *will* do is (1) specify precisely what "sorted" means for your data, (2) reuse the *ideas* inside the sorting algorithms (merging, partitioning, bucketing) to solve other problems, and (3) recognize when you can beat $O(n \log n)$.

---

## Pragmatics: What Does "Sorted" Mean?

Before choosing an algorithm, answer four questions about the order you want.

**Increasing or decreasing?** Pass `reverse=True`, or negate a numeric key.

**Sort by what key?** Records are usually sorted by a field, and the rest of the record must travel with it. Python's `key` function extracts the field; it is called once per element, so it's cheap even when expensive to compute.

**What happens to ties?** A sort is **stable** if elements with equal keys keep their original relative order. Python's sort is guaranteed stable. Stability matters whenever you sort in several passes, or when the input order carries meaning (e.g., arrival time).

**How do non-numeric values compare?** Tuples compare lexicographically, strings compare by code point (so `"Z" < "a"`), and custom orders need a custom key or comparator.

```python
people = [("alice", 30), ("bob", 25), ("carol", 30), ("dave", 25)]
words = ["banana", "Apple", "cherry"]

sorted(people, key=lambda p: p[1])                 # by age; ties keep input order
sorted(people, key=lambda p: (-p[1], p[0]))        # age descending, then name ascending
sorted(words, key=str.lower)                       # case-insensitive

# Multi-pass: because the sort is stable, sort by the SECONDARY key first
people.sort(key=lambda p: p[0])                    # secondary: name
people.sort(key=lambda p: p[1], reverse=True)      # primary: age descending
```

### When a key isn't enough: comparators

Some orders can't be expressed as a key. **Largest Number (LC 179)** asks for the arrangement of numbers forming the largest concatenation: `[3, 30, 34, 5, 9]` → `"9534330"`. The right order between two numbers $a$ and $b$ depends on both: put $a$ first iff `a + b > b + a` as strings.

```python
from functools import cmp_to_key


def largest_number(nums: list[int]) -> str:
    strs = [str(x) for x in nums]

    def compare(a: str, b: str) -> int:
        if a + b > b + a:
            return -1           # a goes first
        if a + b < b + a:
            return 1
        return 0

    strs.sort(key=cmp_to_key(compare))
    result = "".join(strs)
    return "0" if result[0] == "0" else result
```

!!! warning "A comparator must define a consistent order"
    Sorting algorithms assume the comparison is **transitive**: if $a$ precedes $b$ and $b$ precedes $c$, then $a$ precedes $c$. An inconsistent comparator doesn't raise an error; it silently produces garbage. (The concatenation order above *is* transitive, but that requires proof — it's not obvious!) When writing a comparator, ask whether it is really comparing some underlying quantity.

---

## Incremental Insertion: Insertion Sort

The simplest design strategy is **incremental**: solve the problem for the first $n - 1$ items, then add the $n$-th. For sorting, that means inserting each new element into its place in an already-sorted prefix.

```python
def insertion_sort(a: list[int]) -> None:
    for i in range(1, len(a)):
        x = a[i]
        j = i - 1
        while j >= 0 and a[j] > x:
            a[j + 1] = a[j]          # shift larger elements right
            j -= 1
        a[j + 1] = x
```

$O(n^2)$ in the worst case, but $O(n + d)$ where $d$ is the number of **inversions** (out-of-order pairs). On nearly-sorted data it is linear, which is why hybrid sorts use it for small or nearly-sorted pieces.

The incremental idea gets faster with a better data structure. Insert into a balanced search tree instead of an array, and each insertion costs $O(\log n)$; an in-order traversal then reads out the sorted order. That is $O(n \log n)$ sorting by incremental insertion.

---

## Heapsort: Selection Sort with the Right Data Structure

Selection sort repeatedly finds the smallest remaining element. Finding it by scanning costs $O(n)$ per step, $O(n^2)$ total. But "repeatedly extract the minimum" is exactly the operation a **priority queue** supports — a binary heap does it in $O(\log n)$. Same algorithm, better data structure: $O(n \log n)$.

```python
import heapq


def heapsort(a: list[int]) -> list[int]:
    heap = a[:]
    heapq.heapify(heap)                                  # O(n)
    return [heapq.heappop(heap) for _ in range(len(heap))]
```

Heapsort is worst-case $O(n \log n)$, can run in place with $O(1)$ extra space, and is not stable. Heaps get a full treatment in [Heaps](09_heaps.md).

!!! tip "Take-Home Lesson"
    Selection sort and heapsort are the *same* algorithm. The difference between $O(n^2)$ and $O(n \log n)$ is entirely the data structure used to find the minimum. Many "new" algorithms are old algorithms with a better data structure plugged in.

---

## Mergesort: Divide and Conquer

Split the array in half, sort each half recursively, and **merge** the two sorted halves. The smallest remaining element overall is always at the front of one of the two halves, so merging is a linear two-pointer scan.

```python
def merge_sort(a: list[int]) -> list[int]:
    if len(a) <= 1:
        return a
    mid = len(a) // 2
    left, right = merge_sort(a[:mid]), merge_sort(a[mid:])
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:          # <= keeps the sort stable
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged
```

**Analysis.** Picture the recursion tree. Level $k$ has $2^k$ subproblems of size $n / 2^k$; merging them all costs $O(n)$ because every element appears in exactly one subproblem per level. There are $\log_2 n$ levels. Total: $\Theta(n \log n)$ in **every** case — best, average, and worst. Formally, $T(n) = 2T(n/2) + \Theta(n)$, case 2 of the [master theorem](01_complexity_analysis.md#the-master-theorem).

**Properties:**

- **Stable**, as long as the merge takes from the left on ties.
- **Needs $O(n)$ auxiliary space** for arrays — merging in place without a buffer would overwrite unmerged elements.
- **Ideal for linked lists**: merging two lists just relinks nodes, with no extra space and no need for random access (LC 148).
- **Ideal for external sorting**: data too large for memory is sorted in chunks, then the sorted chunks are merged by streaming them sequentially.

### Piggybacking on the merge: counting inversions

Mergesort's real value in interviews is that the merge step sees every "cross" pair — one element from the left half, one from the right — in sorted order. Any quantity summed over cross pairs can be computed during the merge for free.

**Count inversions:** how many pairs $i < j$ have $a_i > a_j$? When the merge takes `right[j]` before the remaining `left[i:]`, then `right[j]` is smaller than every one of those `len(left) - i` elements, all of which were originally to its left.

```python
def count_inversions(a: list[int]) -> int:
    def sort_count(lo: int, hi: int) -> int:
        if hi - lo <= 1:
            return 0
        mid = (lo + hi) // 2
        count = sort_count(lo, mid) + sort_count(mid, hi)
        merged, i, j = [], lo, mid
        while i < mid and j < hi:
            if a[i] <= a[j]:
                merged.append(a[i])
                i += 1
            else:
                merged.append(a[j])
                count += mid - i          # a[j] jumps ahead of a[i:mid]
                j += 1
        merged += a[i:mid] + a[j:hi]
        a[lo:hi] = merged
        return count

    return sort_count(0, len(a))
```

Brute force is $O(n^2)$; this is $O(n \log n)$. The same technique solves Reverse Pairs (LC 493) and Count of Smaller Numbers After Self (LC 315).

---

## Quicksort: Sorting by Randomization

Pick a **pivot** element $p$. Partition the array into elements less than $p$, then $p$, then elements greater than or equal to $p$. Now $p$ is in its final position, and no element will ever cross from one side to the other — so sort each side independently, recursively.

```python
import random


def quicksort(a: list[int], lo: int = 0, hi: int | None = None) -> None:
    if hi is None:
        hi = len(a) - 1
    if lo >= hi:
        return
    p = partition(a, lo, hi)
    quicksort(a, lo, p - 1)
    quicksort(a, p + 1, hi)


def partition(a: list[int], lo: int, hi: int) -> int:
    """Lomuto partition around a random pivot; returns the pivot's final index."""
    r = random.randint(lo, hi)
    a[r], a[hi] = a[hi], a[r]            # move the random pivot to the end
    pivot = a[hi]
    first_high = lo                      # a[lo:first_high] < pivot
    for i in range(lo, hi):
        if a[i] < pivot:
            a[i], a[first_high] = a[first_high], a[i]
            first_high += 1
    a[first_high], a[hi] = a[hi], a[first_high]
    return first_high
```

The partition maintains three regions: `a[lo:first_high]` is less than the pivot, `a[first_high:i]` is at least the pivot, and `a[i:hi]` is unexplored. It's the reader–writer pattern from the two-pointers chapter.

### How fast is it?

Like mergesort, quicksort does $O(n)$ work per level of recursion, so its running time is $O(n \cdot h)$ where $h$ is the height of the recursion tree. Everything depends on the pivots.

- **Best case:** every pivot is the median, the tree has height $\log_2 n$, and quicksort is $O(n \log n)$.
- **Worst case:** every pivot is the smallest or largest element, each level peels off just one element, the height is $n$, and quicksort is $\Theta(n^2)$ — it has turned into selection sort.

**The expected case.** Call a pivot *good enough* if it lies in the middle half of the sorted order (between the 25th and 75th percentiles). Half of all elements are good enough, so a random pivot is good enough with probability $1/2$. A good-enough pivot leaves at most $3n/4$ elements on the bigger side. Along any root-to-leaf path, the subproblem shrinks by a factor of $3/4$ at least every other level on average, so it reaches size 1 after about $2 \log_{4/3} n = O(\log n)$ levels. Hence $O(n \log n)$ expected. (A careful analysis gives about $2n \ln n \approx 1.39\, n \log_2 n$ comparisons.)

### Why randomize?

With a *fixed* pivot rule, such as "always use the last element," there is a specific input that forces the worst case — and for the last-element rule, that input is an already-sorted array, which is extremely common in practice.

Choosing the pivot **at random** changes the nature of the guarantee. There is no longer a bad *input*; there are only bad *coin flips*, and they are astronomically unlikely. Randomized quicksort runs in $O(n \log n)$ expected time **on every input**.

!!! tip "Take-Home Lesson"
    Randomization makes an algorithm's performance depend on its own coin flips rather than on the input. It is a powerful way to defeat worst-case inputs, and it often produces algorithms far simpler than their deterministic counterparts. When quicksort "goes quadratic," nothing mysterious happens — you just lost a lottery you were overwhelmingly likely to win.

??? question "Stop and Think: Nuts and bolts"
    **Problem:** You have $n$ bolts of different widths and their $n$ matching nuts. You can try a nut on a bolt and learn whether the nut is too large, too small, or a match — but you cannot compare two nuts or two bolts directly. Match every bolt to its nut efficiently.

    **Solution:** Trying each bolt against every remaining nut is $O(n^2)$. To do better, emulate quicksort. Pick a random bolt $b$ and test every nut against it, partitioning the nuts into smaller-than-$b$, larger-than-$b$, and its match $m$. Now use $m$ as a pivot to partition the **bolts** the same way. In $2n - 2$ tests we've matched one pair and split the problem into two independent subproblems, exactly as quicksort does. Expected time: $O(n \log n)$.

    Remarkably, no simple *deterministic* $O(n \log n)$ algorithm is known for this problem. Randomization makes the bad cases disappear, leaving a short and elegant algorithm.

### Many duplicates: three-way partitioning

If the array is all copies of one value, the partition above puts everything on one side: quadratic again. The fix is to partition into **three** regions: less than, equal to, and greater than the pivot. Equal elements are finished and never recursed on. This is the **Dutch national flag** problem (LC 75, Sort Colors):

```python
def three_way_partition(a: list[int], pivot: int) -> tuple[int, int]:
    """Rearrange a into  < pivot | == pivot | > pivot ; return the middle bounds."""
    lt, i, gt = 0, 0, len(a)      # a[:lt] < p, a[lt:i] == p, a[gt:] > p
    while i < gt:
        if a[i] < pivot:
            a[lt], a[i] = a[i], a[lt]
            lt += 1
            i += 1
        elif a[i] > pivot:
            gt -= 1
            a[gt], a[i] = a[i], a[gt]   # don't advance i: new a[i] is unexamined
        else:
            i += 1
    return lt, gt
```

### Is quicksort really quick?

Mergesort, heapsort, and quicksort are all $\Theta(n \log n)$, so asymptotic analysis can't rank them. In practice a well-implemented quicksort is typically two to three times faster than the others: its inner loop is tiny and it scans memory sequentially, which caches love. When algorithms tie asymptotically, only experiments can break the tie.

---

## Selection: The $k$-th Smallest Element

To find the median, or the $k$-th largest element (LC 215), sorting costs $O(n \log n)$ — but it does far more work than needed. **Quickselect** partitions like quicksort, then recurses into **only the side containing position $k$**:

```python
def quickselect(a: list[int], k: int) -> int:
    """Return the k-th smallest element (0-indexed). Rearranges a."""
    lo, hi = 0, len(a) - 1
    while True:
        p = partition(a, lo, hi)
        if p == k:
            return a[p]
        if p < k:
            lo = p + 1
        else:
            hi = p - 1


def find_kth_largest(nums: list[int], k: int) -> int:
    return quickselect(nums[:], len(nums) - k)
```

With good pivots, the work is $n + n/2 + n/4 + \cdots < 2n$ — a geometric series — so quickselect runs in $O(n)$ expected time. (The worst case is $O(n^2)$; the "median of medians" algorithm guarantees $O(n)$ deterministically, but it's rarely worth the complexity.) For the $k$ largest elements when $k \ll n$, a size-$k$ heap in $O(n \log k)$ is often simpler; see [Heaps](09_heaps.md).

---

## The Lower Bound: Why $n \log n$?

Mergesort, heapsort, and quicksort all take $\Theta(n \log n)$. Is a linear-time sort possible?

Not if the algorithm learns about the input only by **comparing** pairs of elements. Any such algorithm can be drawn as a **decision tree**: each internal node is a comparison, each branch an outcome, and each leaf a final ordering. The algorithm must reach a *different* leaf for each of the $n!$ input permutations — if two permutations led to the same leaf, the same rearrangement would be applied to both, and at least one would come out unsorted. A binary tree with $n!$ leaves has height at least $\log_2(n!)$, and

$$\log_2(n!) = \sum_{i=1}^{n} \log_2 i \ \ge\ \frac{n}{2} \log_2 \frac{n}{2} = \Omega(n \log n)$$

So every comparison sort needs $\Omega(n \log n)$ comparisons in the worst case. Mergesort and heapsort are **optimal**. The same argument gives $\Omega(n \log n)$ lower bounds for problems that sorting solves, such as element uniqueness in the comparison model.

The only way around the bound is to **not compare**: to use the values themselves as addresses. That's what distribution sorts do.

---

## Distribution Sorts: Beating $n \log n$

To sort names for a phone book, you might first split them into 26 piles by first letter. Every name in pile J belongs after every name in pile I, so each pile can be sorted independently and the piles concatenated. This is **bucketing**, and when keys are small integers or evenly distributed, it sorts in linear time.

### Counting sort

When keys are integers in a small range $[0, k)$, count occurrences of each key and read them back in order. $O(n + k)$ time.

```python
def counting_sort(a: list[int], k: int) -> list[int]:
    """Sort integers in range [0, k)."""
    counts = [0] * k
    for x in a:
        counts[x] += 1
    result = []
    for value, c in enumerate(counts):
        result.extend([value] * c)
    return result
```

For sorting *records* by an integer key, the stable version computes prefix sums of the counts to find each key's starting position, then places records in input order. That stable version is what radix sort needs.

### Radix sort

To sort $d$-digit numbers, run a **stable** counting sort on each digit from least to most significant. Stability is essential: after sorting by digit $i$, ties are broken by the previous passes on lower digits. Total: $O(d \cdot (n + b))$ for base $b$. For 32-bit integers with base $2^{16}$, that's two linear passes.

### Bucket sort

For real numbers roughly **uniformly distributed** in $[0, 1)$, create $n$ buckets, put $x$ in bucket $\lfloor n x \rfloor$, sort each (tiny) bucket, and concatenate. Expected $O(n)$.

!!! warning "Bucketing bets on the distribution"
    Bucket-based methods are fast when the data is spread out as expected and terrible when it isn't. If most keys land in one bucket, you're back to sorting everything with the fallback algorithm. Real data is often wildly non-uniform: surnames cluster regionally, timestamps cluster at business hours, and adversarial inputs cluster deliberately. Balanced trees and comparison sorts give guarantees on *every* input; bucketing gives them only on the inputs you expected.

### Bucketing in interviews

Distribution-sort ideas appear more often than distribution sorts themselves:

- **Top K Frequent Elements (LC 347):** a frequency is an integer in $[1, n]$, so bucket elements by frequency and read buckets from the top: $O(n)$.
- **H-Index (LC 274):** citations above $n$ can be capped at $n$, then counting sort.
- **Maximum Gap (LC 164):** with $n$ numbers spread over range $R$, the maximum gap is at least $R / (n - 1)$ by the pigeonhole principle. With buckets of that width, the maximum gap can't occur *inside* a bucket, only *between* adjacent non-empty buckets. So only each bucket's min and max matter: $O(n)$.
- **Sort Characters by Frequency (LC 451):** 26 or 128 possible characters make any key small.

---

## Python's Built-in Sort: Timsort

`list.sort()` and `sorted()` use **Timsort**, a hybrid of mergesort and insertion sort designed for real-world data:

- It scans for existing sorted runs ("natural runs") and merges them, so it is **$O(n)$ on already-sorted or reverse-sorted input** and fast on partially sorted input.
- Short runs are extended with binary insertion sort.
- When one run keeps "winning" during a merge, it switches to galloping (exponential search) to skip ahead.
- It is **stable**, worst-case $O(n \log n)$, and uses $O(n)$ auxiliary space.

Use it. A hand-written sort in pure Python is typically 10–100× slower than the built-in, which runs in C.

---

## Comparison Table

| Algorithm | Best | Average | Worst | Extra space | Stable | Notes |
|---|---|---|---|---|---|---|
| Insertion sort | $O(n)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | Yes | $O(n + \text{inversions})$; great for small / nearly sorted |
| Selection sort | $O(n^2)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | No | Minimal number of swaps |
| Heapsort | $O(n \log n)$ | $O(n \log n)$ | $O(n \log n)$ | $O(1)$ | No | Guaranteed bound, in place |
| Mergesort | $O(n \log n)$ | $O(n \log n)$ | $O(n \log n)$ | $O(n)$ | Yes | Linked lists, external sorting, inversions |
| Quicksort (random pivot) | $O(n \log n)$ | $O(n \log n)$ | $O(n^2)$ | $O(\log n)$ | No | Fastest in practice |
| Timsort | $O(n)$ | $O(n \log n)$ | $O(n \log n)$ | $O(n)$ | Yes | Python's built-in |
| Counting sort | $O(n + k)$ | $O(n + k)$ | $O(n + k)$ | $O(k)$ | Yes* | Integer keys in $[0, k)$ |
| Radix sort | $O(d(n + b))$ | $O(d(n + b))$ | $O(d(n + b))$ | $O(n + b)$ | Yes | $d$ digits in base $b$ |
| Bucket sort | $O(n)$ | $O(n)$ | $O(n^2)$ | $O(n)$ | Yes* | Assumes uniform distribution |

\* When implemented with the stable placement pass.

---

## Common Mistakes

1. **Sorting when you don't need order.** Sorting is $O(n \log n)$; a hash set answers "have I seen this?" in $O(n)$ total. Sort when the problem involves *order* or *nearness*; hash when it involves only *equality*.

2. **Forgetting that sorting destroys positions.** If you need original indices afterward, sort `range(n)` by key, or sort `(value, index)` pairs.

3. **Mutating instead of copying.** `list.sort()` sorts in place and returns `None`; `x = arr.sort()` sets `x` to `None`. Use `sorted(arr)` for a new list.

4. **Inconsistent comparators.** A comparator that isn't transitive produces an unspecified order without any error.

5. **Deterministic pivots.** Quicksort or quickselect with a first- or last-element pivot is quadratic on sorted input — a common test case. Randomize.

6. **Ignoring duplicates in quicksort.** Two-way partitioning degrades to $O(n^2)$ on arrays with few distinct values; use three-way partitioning.

7. **Assuming bucketing is always linear.** It is linear only when the keys are small integers or evenly distributed.

---

## Practice Problems

| Problem | Idea |
|---|---|
| Sort Colors (LC 75) | Three-way partition |
| Largest Number (LC 179) | Custom comparator |
| Sort List (LC 148) | Mergesort on a linked list |
| Kth Largest Element in an Array (LC 215) | Quickselect or size-$k$ heap |
| Top K Frequent Elements (LC 347) | Bucket by frequency |
| H-Index (LC 274) | Counting sort with capping |
| Maximum Gap (LC 164) | Pigeonhole buckets |
| Count of Smaller Numbers After Self (LC 315) | Mergesort with counting |
| Reverse Pairs (LC 493) | Mergesort with counting |
| Wiggle Sort II (LC 324) | Median via quickselect + three-way partition |
| Sort an Array (LC 912) | Implement mergesort / randomized quicksort |
