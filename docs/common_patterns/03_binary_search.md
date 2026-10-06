# Binary Search

Binary search is the mother of all divide-and-conquer algorithms. Its power is easy to underestimate: it finds any item among a billion in about thirty comparisons. But the real reason it deserves a chapter is that "search a sorted array" is only its most obvious application. Binary search works on *anything* with a monotone yes/no structure — the boundary inside a sorted array, the minimum feasible capacity of a ship, the square root of a number, the first bad commit in a history.

This chapter develops one template, proves why it is correct, and then shows that almost every binary search problem is that template with a different predicate plugged in.

---

## Twenty Questions

In the game of twenty questions, one player thinks of a word and the other asks yes/no questions until they guess it. The second player has a guaranteed winning strategy: open a dictionary to the middle, and ask "does your word come before *this* one alphabetically?" Every answer eliminates half of the remaining words. A dictionary has at most a few hundred thousand entries, and $2^{20} \approx 10^6$, so twenty questions always suffice.

That is binary search: each comparison with the middle element halves the candidate set, so $n$ candidates are reduced to one in $\lceil \log_2 n \rceil$ steps.

| $n$ | Linear scan (worst case) | Binary search (worst case) |
|---|---|---|
| $10^3$ | 1,000 | 10 |
| $10^6$ | 1,000,000 | 20 |
| $10^9$ | 1,000,000,000 | 30 |

The price is a precondition: the data must be *ordered* so that a single comparison tells you which half to discard. Paying $O(n \log n)$ once to sort, then $O(\log n)$ per query, is one of the most common trades in algorithm design.

---

## The Classic Algorithm

```python
def binary_search(nums: list[int], target: int) -> int:
    """Return an index i with nums[i] == target, or -1 if absent."""
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1           # target can only be in nums[mid+1 .. hi]
        else:
            hi = mid - 1           # target can only be in nums[lo .. mid-1]
    return -1
```

**Why it is correct.** The loop maintains an *invariant*: if `target` is anywhere in `nums`, it is in `nums[lo..hi]`. Initially this is the whole array, so the invariant holds. Each branch discards only elements that provably cannot equal `target` (they are all strictly smaller or strictly larger, because the array is sorted), so the invariant is preserved. The window shrinks by at least one each iteration, so the loop terminates; when it does with `lo > hi`, the window is empty, and by the invariant `target` is not present.

**Time:** $O(\log n)$. **Space:** $O(1)$ iteratively, $O(\log n)$ if written recursively.

!!! tip "Take-Home Lesson"
    Every correct binary search rests on an invariant about what lies inside, left of, and right of the current window. If you can't state the invariant, you can't trust the off-by-ones. Write it down as a comment before writing the loop.

---

## The Real Pattern: Finding a Boundary

The classic algorithm answers "is `target` here?" But most problems ask a different question: *where does something start?* The first element $\ge x$, the first day a condition holds, the smallest capacity that works.

All of these are the same problem. Suppose we have a **predicate** $P(i)$ over indices $\text{lo} \dots \text{hi}$ that is **monotone**: once it becomes true, it stays true.

```text
index:  0     1     2     3     4     5     6     7
P(i):   F     F     F     F     T     T     T     T
                              ^
                        first True — this is what we want
```

The following template finds the first index where $P$ is true. Memorize this one; everything else in the chapter is a variation.

```python
from typing import Callable


def first_true(lo: int, hi: int, pred: Callable[[int], bool]) -> int:
    """Smallest i in [lo, hi) with pred(i) True, or hi if there is none.

    Requires pred to be monotone: False ... False True ... True.
    """
    while lo < hi:
        mid = (lo + hi) // 2
        if pred(mid):
            hi = mid           # mid might be the answer; keep it
        else:
            lo = mid + 1       # mid is definitely not the answer
    return lo
```

**Invariant:** everything left of `lo` is False; everything at or right of `hi` is True (treating `hi` as a virtual True sentinel when it is past the end). The search space is the half-open interval $[\text{lo}, \text{hi})$. Each iteration shrinks it strictly, because `mid < hi` always holds when `lo < hi`. When `lo == hi`, the False region and the True region meet: `lo` is the boundary.

Notice what this template does *not* have: an equality check, a `result` variable, a `<=` loop condition, or a `mid - 1`. Every one of those is a place to make an off-by-one mistake, and none of them is needed.

### Lower bound, upper bound, and counting

With `first_true`, the standard bounds are one-liners:

```python
def lower_bound(nums: list[int], x: int) -> int:
    """First index i with nums[i] >= x (== bisect.bisect_left)."""
    return first_true(0, len(nums), lambda i: nums[i] >= x)


def upper_bound(nums: list[int], x: int) -> int:
    """First index i with nums[i] > x (== bisect.bisect_right)."""
    return first_true(0, len(nums), lambda i: nums[i] > x)
```

These two boundaries bracket the block of elements equal to `x`, which gives several classic problems for free:

| Question | Answer |
|---|---|
| Is `x` present? | `lo = lower_bound(nums, x)`; check `lo < len(nums) and nums[lo] == x` |
| First occurrence of `x` (LC 34) | `lower_bound(nums, x)` if present |
| Last occurrence of `x` (LC 34) | `upper_bound(nums, x) - 1` if present |
| How many times does `x` occur? | `upper_bound(nums, x) - lower_bound(nums, x)` |
| How many elements are $< x$? | `lower_bound(nums, x)` |
| How many elements lie in $[a, b]$? | `upper_bound(nums, b) - lower_bound(nums, a)` |
| Where should `x` be inserted to keep order? (LC 35) | `lower_bound(nums, x)` |

??? question "Stop and Think: Counting occurrences"
    **Problem:** Count how many times a key $k$ occurs in a sorted array of $n$ elements.

    **A tempting solution:** binary search for any copy of $k$, then walk left and right until the values change. This costs $O(\log n + s)$, where $s$ is the number of copies. That looks fine — until the array is a million copies of $k$, and the "binary search" algorithm quietly becomes a linear scan.

    **The fix:** don't search for $k$; search for the *boundaries* of its block. Two boundary searches cost $O(\log n)$ no matter how large the block is: `upper_bound(nums, k) - lower_bound(nums, k)`.

    The lesson generalizes: when an answer is a contiguous range, search for its **endpoints**, not for a member.

### Use the standard library

Python's `bisect` module implements exactly these searches in C:

```python
import bisect

nums = [1, 3, 3, 3, 5, 8]
bisect.bisect_left(nums, 3)    # 1 — first index with nums[i] >= 3
bisect.bisect_right(nums, 3)   # 4 — first index with nums[i] >  3
bisect.insort(nums, 4)         # insert keeping order: O(log n) search + O(n) shift

# Python 3.10+: search by key without building a separate list
events = [(1, "a"), (4, "b"), (9, "c")]
bisect.bisect_left(events, 5, key=lambda e: e[0])   # 2
```

In an interview, `bisect` is almost always acceptable — but be ready to write `first_true` by hand, since the interesting problems need a custom predicate.

---

## Recognizing a Monotone Predicate

The skill that separates binary search experts from everyone else is spotting a monotone predicate in data that is **not sorted**. Here are three examples where the array is not sorted, yet a clean F…FT…T structure exists.

### Rotated sorted array — find the minimum (LC 153)

A sorted array rotated at an unknown pivot, e.g. `[4, 5, 6, 7, 0, 1, 2]`. The predicate $P(i) = \text{nums}[i] \le \text{nums}[-1]$ is False on the left part (values larger than the last element) and True on the right part (the rotated-in smaller values):

```text
nums:  4  5  6  7  0  1  2
P(i):  F  F  F  F  T  T  T      P(i) = nums[i] <= nums[-1]
```

```python
def find_min_rotated(nums: list[int]) -> int:
    i = first_true(0, len(nums), lambda i: nums[i] <= nums[-1])
    return nums[i]
```

### Rotated sorted array — search (LC 33)

With the pivot found, the array is two sorted runs, and ordinary binary search on the correct run finishes the job. An alternative single-pass approach uses the observation that **at least one half around `mid` is always sorted**, and a sorted half lets you decide in $O(1)$ whether the target lies in it:

```python
def search_rotated(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:                    # left half is sorted
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:                                        # right half is sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1
```

!!! warning "Duplicates break the invariant"
    With duplicates (LC 81), `nums[lo] == nums[mid] == nums[hi]` gives no information about which half is sorted. The only safe move is to shrink both ends by one, and the worst case degrades to $O(n)$ — try `[1, 1, 1, 1, 0, 1, 1]`. This is inherent, not a flaw in the code: no algorithm can do better.

### Peak element (LC 162)

Find any index with `nums[i] > nums[i-1]` and `nums[i] > nums[i+1]` (with $-\infty$ outside the array; adjacent values differ). The array can be anything, yet the predicate $P(i) = \text{nums}[i] > \text{nums}[i+1]$ ("we are going downhill") has a useful property: if $P(\text{mid})$ is False, we are going uphill, so *some* peak must exist to the right (the slope can't go up forever); if True, some peak exists at `mid` or to its left.

```python
def find_peak_element(nums: list[int]) -> int:
    n = len(nums)
    return first_true(0, n - 1, lambda i: nums[i] > nums[i + 1])
```

Here the predicate isn't globally monotone, but the invariant "a peak exists in $[\text{lo}, \text{hi}]$" is preserved by each step, and that is all correctness requires.

!!! note "Why `nums[i + 1]` never goes out of bounds"
    The search range is `[0, n - 1)`, and `first_true` only evaluates `pred(mid)` with `mid < hi`, so `i ≤ n - 2` and `i + 1 ≤ n - 1` always. The last index is never tested: if no `True` is found, `first_true` returns `hi = n - 1`, which is correct because the array was increasing all the way and $\text{nums}[n] = -\infty$. For `n == 1` the loop doesn't run and the answer is `0`.

    This depends on the half-open `lo < hi` loop. With the closed-interval `lo <= hi` style, `mid` can reach `n - 1`: on `[1, 2]` the second iteration has `lo = hi = mid = 1` and reads `nums[2]`. That loop also never ends once `lo == hi` and `hi = mid` is taken.

### Search a 2D matrix (LC 74)

If each row is sorted and each row starts after the previous row ends, the matrix *is* a sorted array of length $mn$ stored row by row. Map index $k$ to `matrix[k // n][k % n]` and run the ordinary search in $O(\log mn)$.

If instead rows and columns are sorted independently (LC 240), no such flattening exists. Start at the top-right corner: if the value is too large, the entire column is too large (move left); if too small, the entire row is too small (move down). Each step discards a row or a column, giving $O(m + n)$.

---

## Binary Search on the Answer

This is the single most important binary search pattern in interviews. The array being searched is not in the input at all — it is the **range of possible answers**.

The pattern applies when a problem asks for the *minimum* (or maximum) value of something, and it is much easier to **check** whether a given candidate works than to **compute** the optimum directly. If feasibility is monotone — any value larger than a feasible one is also feasible — then:

```text
candidate:  1    2    3    4    5    6    7    8
feasible?:  F    F    F    T    T    T    T    T
                           ^
                  minimum feasible answer
```

and the answer is `first_true(lo, hi + 1, feasible)`. The total cost is $O(C \cdot \log R)$, where $C$ is the cost of one feasibility check and $R$ is the size of the answer range.

### Koko eating bananas (LC 875)

Koko has `piles` of bananas and `h` hours. At speed $k$ she needs $\lceil p / k \rceil$ hours for a pile of size $p$. Find the minimum $k$ that finishes in time.

Computing the optimal $k$ directly is awkward. Checking a *given* $k$ is trivial — sum the hours. And if speed $k$ works, any faster speed also works. That is all we need.

```python
def min_eating_speed(piles: list[int], h: int) -> int:
    def can_finish(k: int) -> bool:
        return sum((p + k - 1) // k for p in piles) <= h   # ceil(p / k)

    return first_true(1, max(piles) + 1, can_finish)
```

**Bounds:** speed 1 is the slowest meaningful speed; speed `max(piles)` finishes every pile in one hour, and since `h >= len(piles)` it always works. **Time:** $O(n \log M)$ with $M = $ `max(piles)`.

### Capacity to ship packages within D days (LC 1011)

Packages must ship **in order**; each day the ship loads consecutive packages up to its capacity. Find the minimum capacity to ship everything in `days` days.

Feasibility of a capacity $c$ is a **greedy** check: load each day as full as possible. (Greedy is optimal here because leaving room on an earlier day can never help a later day.)

```python
def ship_within_days(weights: list[int], days: int) -> int:
    def fits(capacity: int) -> bool:
        needed, load = 1, 0
        for w in weights:
            if load + w > capacity:
                needed += 1
                load = 0
            load += w
        return needed <= days

    return first_true(max(weights), sum(weights) + 1, fits)
```

**Bounds matter:** the capacity must be at least `max(weights)` or the heaviest package never ships; `sum(weights)` ships everything in one day. Starting `lo` below `max(weights)` makes the greedy check silently wrong.

### Split array largest sum (LC 410)

Split `nums` into `k` contiguous parts to minimize the largest part sum. This is the *same problem* as LC 1011 in disguise — "capacity" is "largest part sum," "days" is "number of parts" — and the same code solves it. Recognizing that two problems are really one is the whole game.

### A catalog of answer-space searches

| Problem | Search over | Feasibility check |
|---|---|---|
| Koko Eating Bananas (LC 875) | eating speed | total hours $\le h$ |
| Ship Packages (LC 1011) | ship capacity | greedy day count $\le D$ |
| Split Array Largest Sum (LC 410) | max part sum | greedy part count $\le k$ |
| Minimum Days to Make Bouquets (LC 1482) | day | count adjacent bloomed runs |
| Magnetic Force Between Balls (LC 1552) | min distance (maximize) | greedy placement count $\ge m$ |
| Kth Smallest in Sorted Matrix (LC 378) | value | count of entries $\le$ value $\ge k$ |
| Find the Smallest Divisor (LC 1283) | divisor | sum of ceilings $\le$ threshold |

### Maximizing instead of minimizing

When the question asks for the *largest* feasible value, feasibility is monotone in the other direction (T…TF…F). Don't write a second template — flip the predicate and step back one:

```python
# Largest x in [lo, hi] with ok(x) True, given ok is True...True False...False
largest = first_true(lo, hi + 1, lambda x: not ok(x)) - 1
```

!!! tip "Take-Home Lesson"
    If you can't see how to *compute* an optimal value but can easily *verify* a candidate, and verification is monotone in the candidate, you have a binary search. Checking is often dramatically easier than optimizing.

---

## One-Sided (Exponential) Search

Suppose the array is unbounded — a stream of 0s followed by an endless run of 1s — and we want the transition point $p$. Without a known upper bound, we can't pick a midpoint.

The fix is to probe at exponentially increasing positions $1, 2, 4, 8, 16, \dots$ until we hit a 1. That takes $\lceil \log_2 p \rceil$ probes and produces a window $[2^{j-1}, 2^j]$ that contains $p$; an ordinary binary search inside it takes $\log_2 p$ more. Total: at most $2 \log_2 p$ comparisons, **independent of the total size** of the data.

```python
def exponential_search(pred: Callable[[int], bool]) -> int:
    """First i >= 0 with pred(i) True, for a monotone pred with no known upper bound."""
    if pred(0):
        return 0
    hi = 1
    while not pred(hi):
        hi *= 2
    return first_true(hi // 2 + 1, hi + 1, pred)
```

Exponential search shines when the answer is likely to be **near the start**: the cost depends on where the answer is, not on how much data there is. LC 702 (Search in a Sorted Array of Unknown Size) is the direct application; Timsort's "galloping mode" uses the same idea to merge runs quickly.

---

## Bisection on Real Numbers

Binary search doesn't need integers. To compute $\sqrt{n}$, note that $f(x) = x^2 - n$ is increasing, negative at $x = 0$, and non-negative at $x = \max(1, n)$. Halving the interval that brackets the sign change is the **bisection method**, and it finds a root of any continuous function once you know two points where its sign differs.

```python
def real_sqrt(n: float) -> float:
    lo, hi = 0.0, max(1.0, n)
    for _ in range(100):          # each iteration halves the interval
        mid = (lo + hi) / 2
        if mid * mid < n:
            lo = mid
        else:
            hi = mid
    return lo
```

!!! note "Iterate a fixed number of times"
    With floats, a loop like `while hi - lo > 1e-9` can spin forever if the tolerance is below the floating-point spacing at that magnitude. A fixed iteration count is simpler and always terminates: 100 halvings shrink any interval by $2^{100} \approx 10^{30}$, far more precision than a `float` holds.

For the integer version (LC 69, $\lfloor \sqrt{n} \rfloor$), search for the first $x$ with $x^2 > n$ and subtract one:

```python
def my_sqrt(n: int) -> int:
    return first_true(0, n + 2, lambda x: x * x > n) - 1
```

---

## Divide and Conquer Beyond the Array

Binary search is best understood not as an array algorithm but as a **question-asking strategy**: every yes/no answer should split the remaining possibilities in half. That view explains two further applications.

**Debugging by bisection.** A test passed at commit A and fails at commit B, a thousand commits later. Checking out the midpoint and running the test tells you which half contains the culprit; ten rounds find it. `git bisect` automates exactly this. The same strategy works for commenting out halves of a failing function, or halves of a failing input file.

**Binary search is inherently sequential** — each question depends on the previous answer. When each question is expensive (a lab experiment that takes a week, a build that takes an hour), that's a problem. If you're allowed to ask *arbitrary subsets* rather than halves, you can ask all $\log_2 n$ questions at once: label the $n$ candidates with the binary numbers $0 \dots n-1$, and let question $j$ be "is the answer among the candidates whose bit $j$ is set?" The $\log_2 n$ answers spell out the answer's label directly. The number of questions is the same; the rounds collapse to one.

---

## Common Mistakes

1. **No invariant.** Most binary search bugs come from mixing templates: a `<=` loop with `hi = mid`, or a `<` loop with `hi = len(nums) - 1`. Pick one template (the half-open `first_true` is recommended), state its invariant, and never mix.

2. **Infinite loop from rounding.** In a `lo < hi` loop, `mid = (lo + hi) // 2` rounds *down*, so `mid < hi` always and `hi = mid` makes progress. But `lo = mid` does **not** make progress when `hi == lo + 1`. The `first_true` template avoids this by only ever assigning `lo = mid + 1`.

3. **Wrong answer-space bounds.** The initial range must contain the answer. Ship capacity below `max(weights)` is not merely infeasible — it makes the greedy check return wrong results.

4. **Non-monotone predicate.** Binary search on the answer only works if feasibility is monotone. Before coding, argue explicitly: "if $x$ works, why does $x + 1$ work?"

5. **Linear work hiding in the check.** The total cost is (cost of check) × $\log R$. A check that sorts, copies, or slices can dominate. Also note that `bisect.insort` is $O(n)$ per insertion because of the shift, even though the search is $O(\log n)$.

6. **Integer overflow in other languages.** `(lo + hi) / 2` overflows in Java, C, and C++ when `lo + hi` exceeds $2^{31} - 1$ — a bug that famously sat in the JDK's own binary search for nearly a decade. Python integers don't overflow, but write `lo + (hi - lo) // 2` if you're translating.

---

## Practice Problems

| Problem | Idea |
|---|---|
| Binary Search (LC 704) | Classic search |
| Search Insert Position (LC 35) | Lower bound |
| First and Last Position of Element (LC 34) | Lower and upper bound |
| Find Minimum in Rotated Sorted Array (LC 153) | Predicate `nums[i] <= nums[-1]` |
| Search in Rotated Sorted Array (LC 33) | One half is always sorted |
| Find Peak Element (LC 162) | Follow the uphill slope |
| Search a 2D Matrix (LC 74) | Flatten to 1-D |
| Search a 2D Matrix II (LC 240) | Staircase from the top-right corner |
| Time Based Key-Value Store (LC 981) | `bisect_right` on timestamps |
| Koko Eating Bananas (LC 875) | Search on the answer |
| Capacity to Ship Packages (LC 1011) | Search on the answer + greedy check |
| Split Array Largest Sum (LC 410) | Same problem as LC 1011 |
| Median of Two Sorted Arrays (LC 4) | Binary search on the partition point |
