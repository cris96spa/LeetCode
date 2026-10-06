# Two Pointers & Sliding Window

A huge number of array and string problems ask about **pairs** of positions: two elements that sum to a target, two walls that hold the most water, the start and end of the best subarray. An array of $n$ elements has $\binom{n}{2} \approx n^2/2$ pairs, so brute force is quadratic — fine for $n = 1{,}000$, hopeless for $n = 10^5$.

Two pointers and sliding windows are techniques for examining only $O(n)$ of those pairs **while provably not missing the answer**. That "provably" is the whole point. Each technique rests on an argument that, once some pair has been examined, a whole row or column of other pairs can be discarded without looking at them. If you understand the argument, you can apply the technique to problems you've never seen; if you only memorize the template, you'll apply it to problems where it silently gives wrong answers.

---

## Sorting as a Building Block

Many pair problems become easy once the data is sorted. Sorting costs $O(n \log n)$, which is almost never the bottleneck, and it buys you structure: equal elements become adjacent, close elements become neighbors, and moving a pointer changes a value in a *known direction*.

| Problem | Brute force | After sorting |
|---|---|---|
| Are there duplicates? | Compare all pairs, $O(n^2)$ | Duplicates are adjacent: one scan, $O(n)$ |
| Closest pair of numbers | All pairs, $O(n^2)$ | Closest pair is adjacent: one scan |
| Most frequent element (mode) | Count each, $O(n^2)$ | Equal elements form runs: one scan |
| Two elements summing to $t$ | All pairs, $O(n^2)$ | Two pointers, $O(n)$ |
| Do two sets intersect? | All pairs, $O(nm)$ | Merge-style scan, $O(n + m)$ |

!!! tip "Take-Home Lesson"
    Sorting the data is one of the first things to try in the quest for efficiency. A problem that looks quadratic on unsorted input is often linear on sorted input, and paying $O(n \log n)$ to get there is a good deal.

??? question "Stop and Think: Sorting vs. hashing"
    **Problem:** Hash tables give $O(1)$ expected lookups. For which of the problems in the table above can hashing replace sorting and get $O(n)$ expected time?

    **Solution:**

    - **Duplicates, intersection, mode, two-sum:** yes. Insert elements into a `set` or `Counter` and look each one up. Expected $O(n)$.
    - **Closest pair:** no. Hashing scatters close values into unrelated buckets, destroying exactly the order information the problem needs.

    The general rule: hashing answers "**is this exact value present?**" Sorting answers that *and* "**what is near this value?**" When a problem involves order, ranges, or nearness, you need sorting (or a tree); when it involves only equality, hashing usually wins.

---

## Pattern 1: Opposite-Direction Pointers

### Two Sum on a sorted array (LC 167)

Given a sorted array, find two elements summing to `target`.

```python
def two_sum_sorted(nums: list[int], target: int) -> tuple[int, int] | None:
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        s = nums[lo] + nums[hi]
        if s == target:
            return lo, hi
        if s < target:
            lo += 1
        else:
            hi -= 1
    return None
```

**Why is it correct?** Imagine the $n \times n$ grid of all pairs $(i, j)$ with $i < j$. Brute force checks every cell. The two-pointer algorithm starts at the corner $(0, n-1)$ and argues away an entire row or column with every step:

- If `nums[lo] + nums[hi] < target`, then `nums[lo] + nums[j] < target` for **every** `j <= hi`, because the array is sorted and `nums[j] <= nums[hi]`. So `lo` cannot be part of any solution among the remaining candidates — eliminate the whole row and advance `lo`.
- Symmetrically, if the sum is too large, `hi` pairs too large with every remaining `i`, so eliminate the column.

Each step discards a full row or column, and there are only $n$ of each, so the loop runs at most $n$ times: $O(n)$ time, $O(1)$ space. On *unsorted* input, use a hash map instead (LC 1) — same $O(n)$, but $O(n)$ space.

!!! tip "Take-Home Lesson"
    A two-pointer algorithm is only as good as its **elimination argument**: "when I move this pointer, every pair I skip is provably not the answer." Before using the pattern, say the argument out loud. If you can't, the pattern probably doesn't apply.

### 3Sum (LC 15)

Find all unique triplets summing to zero. Fix the smallest element `nums[i]`, and the rest of the problem is Two Sum on the suffix with target `-nums[i]`:

```python
def three_sum(nums: list[int]) -> list[list[int]]:
    nums.sort()
    n = len(nums)
    result = []
    for i in range(n - 2):
        if nums[i] > 0:
            break                           # smallest element positive: no zero sum
        if i > 0 and nums[i] == nums[i - 1]:
            continue                        # same first element: same triplets
        lo, hi = i + 1, n - 1
        while lo < hi:
            s = nums[i] + nums[lo] + nums[hi]
            if s < 0:
                lo += 1
            elif s > 0:
                hi -= 1
            else:
                result.append([nums[i], nums[lo], nums[hi]])
                lo += 1
                while lo < hi and nums[lo] == nums[lo - 1]:
                    lo += 1                 # skip duplicate second elements
    return result
```

**Time:** $O(n^2)$ — $n$ iterations of an $O(n)$ scan; the sort is dominated. **Space:** $O(1)$ beyond the output (plus the sort).

This reduction — "fix one element, solve the smaller problem on the rest" — generalizes: $k$-Sum costs $O(n^{k-1})$. For 3Sum, $O(n^2)$ is believed to be essentially optimal; the "3SUM conjecture" is used to argue that many geometric problems can't be solved in subquadratic time either.

### Container with most water (LC 11)

Choose two walls to maximize `min(h[i], h[j]) * (j - i)`.

```python
def max_area(height: list[int]) -> int:
    lo, hi = 0, len(height) - 1
    best = 0
    while lo < hi:
        best = max(best, min(height[lo], height[hi]) * (hi - lo))
        if height[lo] < height[hi]:
            lo += 1
        else:
            hi -= 1
    return best
```

The array isn't sorted, but an elimination argument still exists. Suppose `height[lo] < height[hi]`. Any container using wall `lo` with some other wall `j < hi` is *narrower* than the current one, and its height is still at most `height[lo]`. So every remaining pair involving `lo` is no better than the one we just measured — `lo` can be discarded. The shorter wall is always the one to move.

### Trapping rain water (LC 42)

Water above position $i$ is $\min(\text{maxLeft}_i, \text{maxRight}_i) - h_i$. The obvious solution precomputes both maximum arrays in $O(n)$ space. The two-pointer version uses $O(1)$ space:

```python
def trap(height: list[int]) -> int:
    lo, hi = 0, len(height) - 1
    left_max = right_max = water = 0
    while lo < hi:
        if height[lo] < height[hi]:
            left_max = max(left_max, height[lo])
            water += left_max - height[lo]
            lo += 1
        else:
            right_max = max(right_max, height[hi])
            water += right_max - height[hi]
            hi -= 1
    return water
```

**Why can we settle position `lo` knowing only `left_max`?** Its water depends on $\min(\text{maxLeft}, \text{maxRight})$, and we don't know the true $\text{maxRight}$ yet. We don't need to; we only need to know that it is *at least* `left_max`. That follows from an invariant: whenever `left_max` was raised to some `height[lo']`, it happened in the `if` branch, where `height[lo'] < height[hi']` for a wall `hi'` at or right of the current `hi`. So some wall on the right is taller than `left_max`, the minimum is `left_max`, and the water at `lo` is exactly `left_max - height[lo]`. The `else` branch is symmetric.

!!! note "Correctness needs care, even for short code"
    Trapping rain water is 12 lines, and the argument for why it works is longer than the code. That is normal. Reasonable-looking pointer algorithms are easy to write and easy to get wrong; the way to be sure is an invariant, not a few passing test cases.

### Palindromes (LC 125) and reversals

Two pointers from the ends, comparing and moving inward, check whether a sequence is a palindrome or reverse it in place, in $O(n)$ time and $O(1)$ space. Expand-around-center (two pointers moving *outward* from each of the $2n - 1$ possible centers) finds the longest palindromic substring in $O(n^2)$ (LC 5).

---

## Pattern 2: Same-Direction Pointers

### Reader and writer: in-place compaction

A `read` pointer scans every element; a `write` pointer marks where the next *kept* element goes. Everything before `write` is the finished output.

```python
def remove_duplicates(nums: list[int]) -> int:
    """LC 26: dedupe a sorted array in place; return the new length."""
    write = 0
    for read in range(len(nums)):
        if write == 0 or nums[read] != nums[write - 1]:
            nums[write] = nums[read]
            write += 1
    return write


def move_zeroes(nums: list[int]) -> None:
    """LC 283: move zeros to the end, preserving the order of the rest."""
    write = 0
    for read in range(len(nums)):
        if nums[read] != 0:
            nums[write], nums[read] = nums[read], nums[write]
            write += 1
```

**Invariant:** `nums[:write]` is exactly the output for `nums[:read]`. Since `write <= read`, we never overwrite an element we haven't read yet. The same pattern is the partition step in quicksort (see [Sorting](06_sorting.md)).

### Merging two sorted sequences

Two pointers, one per sorted input, repeatedly take the smaller head. This is the merge step of merge sort, and it also answers set questions on sorted inputs in $O(n + m)$: intersection, union, difference, "do these sets overlap?"

```python
def intersect_sorted(a: list[int], b: list[int]) -> list[int]:
    i = j = 0
    out = []
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            i += 1              # a[i] is smaller than everything left in b
        elif a[i] > b[j]:
            j += 1
        else:
            out.append(a[i])
            i += 1
            j += 1
    return out
```

When merging into an array that has spare room at its end (LC 88), fill it **from the back** so you never overwrite unread elements.

### Fast and slow

Pointers moving at different speeds find the middle of a list, detect cycles, and locate cycle entrances. These are covered in [Linked Lists](07_linked_lists.md); the same idea finds the duplicate in LC 287, where the array is interpreted as a linked list `i -> nums[i]`.

---

## Pattern 3: Sliding Window

A **subarray** (or substring) is determined by its endpoints $[l, r]$, so there are $\Theta(n^2)$ of them. A sliding window enumerates only $O(n)$ of them: it moves `r` forward one step at a time, and for each `r`, moves `l` forward only as far as necessary.

### When does it work?

The sliding window needs one structural property. For a "find the longest valid window" problem:

> **If a window is valid, every window inside it is also valid.**

Equivalently: extending a window can only make it *less* valid, and shrinking it can only make it *more* valid. Under this property, when `r` advances and the window becomes invalid, some prefix of the window must be dropped — and since `l` only has to move right to restore validity, and never back, `l` and `r` each move at most $n$ times.

| Condition | Monotone? | Sliding window? |
|---|---|---|
| "At most $k$ distinct characters" | Yes — sub-windows have fewer distinct chars | Yes |
| "No repeated characters" | Yes | Yes |
| "Sum $\le k$", all elements $\ge 0$ | Yes — removing elements can't increase the sum | Yes |
| "Sum $= k$", elements may be negative | **No** — removing a negative increases the sum | No: use prefix sums |
| "Exactly $k$ distinct" | **No** — a sub-window may have fewer than $k$ | Not directly: use at-most($k$) − at-most($k-1$) |

### The template

```python
def longest_valid_window(s: str) -> int:
    window = {}          # state describing s[left..right]
    left = best = 0
    for right, ch in enumerate(s):
        # 1. extend: add s[right] to the window state
        window[ch] = window.get(ch, 0) + 1

        # 2. shrink: restore validity by dropping from the left
        while window[ch] > 1:           # <- the validity condition goes here
            window[s[left]] -= 1
            left += 1

        # 3. record: s[left..right] is now the longest valid window ending at right
        best = max(best, right - left + 1)
    return best
```

This instance solves **Longest Substring Without Repeating Characters (LC 3)**: the window is valid when no character appears twice, and the only character that can have become duplicated is the one just added.

**Why is it $O(n)$ when there's a `while` inside a `for`?** Amortization: `left` only increases, and it can't pass `right`, so across the whole run the inner loop body executes at most $n$ times in total. (See [Complexity Analysis](01_complexity_analysis.md#amortized-analysis).)

### Shortest window: Minimum Window Substring (LC 76)

For "shortest valid window" problems, the logic flips: extend until the window becomes valid, then shrink **while it stays valid**, recording the answer inside the shrink loop.

```python
from collections import Counter


def min_window(s: str, t: str) -> str:
    need = Counter(t)
    missing = len(t)                 # characters of t not yet covered
    left = 0
    best_start, best_len = 0, float("inf")
    for right, ch in enumerate(s):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1                # may go negative: surplus copies
        while missing == 0:          # window is valid: try to shrink
            if right - left + 1 < best_len:
                best_start, best_len = left, right - left + 1
            need[s[left]] += 1
            if need[s[left]] > 0:    # just dropped a needed character
                missing += 1
            left += 1
    return "" if best_len == float("inf") else s[best_start:best_start + best_len]
```

The `missing` counter makes the validity check $O(1)$ instead of comparing two whole counters each step.

### Longest repeating character replacement (LC 424)

A window can be made uniform with at most $k$ replacements iff `window_size - count_of_most_frequent_char <= k`.

```python
def character_replacement(s: str, k: int) -> int:
    count: dict[str, int] = {}
    left = max_freq = 0
    for right, ch in enumerate(s):
        count[ch] = count.get(ch, 0) + 1
        max_freq = max(max_freq, count[ch])
        if (right - left + 1) - max_freq > k:
            count[s[left]] -= 1
            left += 1
    return len(s) - left
```

Two subtleties make this shorter than the template. First, `max_freq` is never decreased when the window shrinks, so it may be stale. That's harmless: the answer only improves when a window beats the best `max_freq` seen so far, and a stale (too high) value only prevents shrinking in cases where no improvement was possible. Second, the window never shrinks — it slides at constant size when invalid — so its final size is the answer.

### Counting subarrays: the "at most" trick

To count subarrays satisfying a monotone condition, note that for each `right`, **every** start in `[left, right]` gives a valid window, contributing `right - left + 1` subarrays. For non-monotone "exactly $k$" conditions, subtract two monotone counts:

```python
def subarrays_with_k_distinct(nums: list[int], k: int) -> int:
    """LC 992: number of subarrays with exactly k distinct values."""
    def at_most(k: int) -> int:
        count: dict[int, int] = {}
        left = total = 0
        for right, x in enumerate(nums):
            count[x] = count.get(x, 0) + 1
            while len(count) > k:
                count[nums[left]] -= 1
                if count[nums[left]] == 0:
                    del count[nums[left]]
                left += 1
            total += right - left + 1
        return total

    return at_most(k) - at_most(k - 1)
```

### Fixed-size windows

When the window size $k$ is given, there's no shrinking decision at all: add `nums[i]`, remove `nums[i - k]`, and update the answer once the window is full. Maximum average subarray (LC 643), anagram search (LC 438, LC 567 — compare character counts of the window to the pattern), and any "every window of size $k$" statistic follow this shape.

### Sliding window maximum (LC 239)

Maintaining a *sum* under add/remove is trivial; maintaining a *maximum* is not, since removing the current maximum requires knowing the next one. A **monotonic deque** stores indices whose values are decreasing from front to back. A new element evicts every smaller element from the back — those can never be a window's maximum again, since the newcomer is larger *and* will stay in the window longer.

```python
from collections import deque


def max_sliding_window(nums: list[int], k: int) -> list[int]:
    dq: deque[int] = deque()          # indices; nums[dq] strictly decreasing
    result = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()                  # dominated: older and not larger
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()              # front fell out of the window
        if i >= k - 1:
            result.append(nums[dq[0]])
    return result
```

Each index is appended once and popped at most once: $O(n)$ total. More on monotonic structures in [Stacks & Queues](08_stacks_queues.md).

---

## When the Window Breaks: Negative Numbers

With negative numbers, the window's key property fails: shrinking can *decrease* the sum, extending can *increase* it. We need different tools.

### Largest subrange: three algorithms for one problem

A hedge fund had these monthly returns, and wants to advertise its best stretch:

$$[-17,\ 5,\ 3,\ -10,\ 6,\ 1,\ 4,\ -3,\ 8,\ 1,\ -13,\ 4]$$

The year was a loss overall, but months 5 through 10 (`[6, 1, 4, -3, 8, 1]`) gained 17 — the **maximum subarray sum** (LC 53). This problem is a good lesson in how algorithm design improves on brute force step by step.

**$O(n^2)$ — try every start.** For each start, extend the end and keep a running sum.

**$O(n \log n)$ — divide and conquer.** Split the array in half. The best subarray lies entirely in the left half, entirely in the right half, or **straddles the middle**. The first two are recursive calls. The straddling one is the best subarray *ending* at the middle (a linear sweep leftward) plus the best one *starting* just after it (a linear sweep rightward). Linear work plus two half-size calls: $T(n) = 2T(n/2) + \Theta(n) = \Theta(n \log n)$.

**$O(n)$ — Kadane's algorithm.** Let $B_i$ be the best sum of a subarray *ending exactly at* $i$. Either it extends the best subarray ending at $i - 1$, or it starts fresh at $i$:

$$B_i = \max(a_i,\ B_{i-1} + a_i)$$

```python
def max_subarray(nums: list[int]) -> int:
    best = cur = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)     # extend, or start over if the prefix hurts
        best = max(best, cur)
    return best
```

That recurrence is a one-dimensional dynamic program (see [Dynamic Programming](16_dynamic_programming.md)), and a good example of how asking "what is the best answer **ending here**?" turns a quadratic search into a single pass.

### Prefix sums

Define $P_0 = 0$ and $P_j = a_0 + \cdots + a_{j-1}$. Then the sum of any subarray is a difference of two prefix sums:

$$\sum_{k=i}^{j-1} a_k = P_j - P_i$$

This turns questions about subarrays into questions about **pairs of prefix sums**, and pairs are something we know how to handle:

- **Range sum queries** (LC 303): precompute $P$, answer each query in $O(1)$.
- **Maximum subarray**: maximize $P_j - P_i$ over $i < j$ — track the minimum prefix seen so far. (This is also Best Time to Buy and Sell Stock, LC 121, where prices play the role of prefix sums.)
- **Count subarrays summing to $k$** (LC 560): for each $j$, count earlier $i$ with $P_i = P_j - k$. A hash map of prefix-sum counts does it in one pass:

```python
def subarray_sum(nums: list[int], k: int) -> int:
    seen = {0: 1}                # prefix sum -> how many times seen
    prefix = count = 0
    for x in nums:
        prefix += x
        count += seen.get(prefix - k, 0)
        seen[prefix] = seen.get(prefix, 0) + 1
    return count
```

The same idea handles "subarray sum divisible by $k$" (LC 974: key on `prefix % k`) and "longest subarray with equal 0s and 1s" (LC 525: map 0 to −1 and store the *first* index of each prefix sum). In 2-D, prefix sums over rectangles give $O(1)$ submatrix sums (LC 304).

---

## Recognizing the Pattern

| Signal in the problem | Technique |
|---|---|
| Sorted array, find a pair with a target sum/difference | Opposite pointers |
| Find triplets / quadruplets | Sort, fix one element, two pointers on the rest |
| Choose two boundaries to maximize a width × height | Opposite pointers; move the limiting side |
| Remove / compact elements in place | Reader–writer pointers |
| Two sorted inputs | Merge-style pointers |
| Longest / shortest substring or subarray satisfying a **monotone** condition | Variable sliding window |
| Every window of size $k$ | Fixed sliding window |
| Max / min over each window | Monotonic deque |
| "Exactly $k$" | at-most($k$) − at-most($k - 1$) |
| Subarray sums with negative numbers | Prefix sums + hash map |
| Best subarray sum | Kadane (DP on "best ending here") |

---

## Common Mistakes

1. **Using a sliding window on a non-monotone condition.** The classic failure: "subarray sum equals $k$" with negative numbers. Check the property before coding: *is every sub-window of a valid window valid?*

2. **Two pointers without an elimination argument.** Moving "the pointer that seems right" gives plausible code that fails on edge cases. Justify each move.

3. **Forgetting to skip duplicates** in $k$-Sum problems, producing repeated triplets — or skipping them before the first use, losing valid answers.

4. **Off-by-one in window size.** The window $[l, r]$ has size `r - l + 1`. The count of subarrays ending at `r` with start in $[l, r]$ is also `r - l + 1`.

5. **Recomputing window state from scratch.** `len(set(s[left:right + 1]))` inside the loop is $O(k)$ per step, making the whole algorithm $O(nk)$. Update state incrementally as elements enter and leave.

6. **Missing the empty prefix.** In prefix-sum-plus-hash-map problems, initialize the map with `{0: 1}` (or `{0: -1}` for index-based variants); otherwise subarrays starting at index 0 are never counted.

---

## Practice Problems

| Problem | Technique |
|---|---|
| Two Sum II (LC 167) | Opposite pointers |
| Valid Palindrome (LC 125) | Opposite pointers |
| 3Sum (LC 15) | Sort + fix one + two pointers |
| Container With Most Water (LC 11) | Move the shorter wall |
| Trapping Rain Water (LC 42) | Two pointers with running maxima |
| Remove Duplicates from Sorted Array (LC 26) | Reader–writer |
| Merge Sorted Array (LC 88) | Merge from the back |
| Longest Substring Without Repeating Characters (LC 3) | Variable window |
| Longest Repeating Character Replacement (LC 424) | Variable window |
| Permutation in String (LC 567) | Fixed window + counts |
| Minimum Window Substring (LC 76) | Shrinking window |
| Subarrays with K Different Integers (LC 992) | at-most trick |
| Sliding Window Maximum (LC 239) | Monotonic deque |
| Maximum Subarray (LC 53) | Kadane |
| Subarray Sum Equals K (LC 560) | Prefix sums + hash map |
