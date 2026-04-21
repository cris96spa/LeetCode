# Binary Search

## When to Use

Binary search applies whenever you can define a condition that partitions a search space into two halves: one where the condition is true and one where it's false. This includes:

- Searching in a sorted array
- Finding boundaries (first/last occurrence, lower/upper bound)
- Searching in a rotated sorted array
- Searching in a 2D sorted matrix
- Finding a peak element
- **Minimizing/maximizing an answer** where you can check feasibility in O(n) or O(n log n)

**Time:** O(log n) for the search itself, times the cost of each feasibility check.
**Space:** O(1) for iterative implementations.

---

## Template 1: Standard Binary Search

Find exact target in a sorted array.

```python
def binary_search(nums, target):
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1
```

**Time:** O(log n). **Space:** O(1).

---

## Template 2: Lower / Upper Bound

### Lower Bound

Smallest index where `nums[i] >= target`. Equivalent to `bisect_left`.

```python
def lower_bound(nums, target):
    left, right = 0, len(nums)

    while left < right:
        mid = (left + right) // 2
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid

    return left
```

### Upper Bound

Smallest index where `nums[i] > target`. Equivalent to `bisect_right`.

```python
def upper_bound(nums, target):
    left, right = 0, len(nums)

    while left < right:
        mid = (left + right) // 2
        if nums[mid] <= target:
            left = mid + 1
        else:
            right = mid

    return left
```

**Time:** O(log n). **Space:** O(1).

---

## Key Patterns

### Finding First / Last Occurrence

**First occurrence:** find target, then keep searching left.

```python
def first_occurrence(nums, target):
    left, right = 0, len(nums) - 1
    result = -1

    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            result = mid
            right = mid - 1  # keep searching left
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return result
```

**Last occurrence:** same idea, but search right after finding.

```python
def last_occurrence(nums, target):
    left, right = 0, len(nums) - 1
    result = -1

    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            result = mid
            left = mid + 1  # keep searching right
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return result
```

### Rotated Sorted Array (LC 33)

One half is always sorted. Determine which half, then check if target lies in the sorted half.

```python
def search_rotated(nums, target):
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid

        if nums[left] <= nums[mid]:  # left half sorted
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:  # right half sorted
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1

    return -1
```

**Time:** O(log n). **Space:** O(1).

### Search a 2D Matrix (LC 74)

Matrix where each row is sorted and the first element of each row is greater than the last element of the previous row. Treat as a flat sorted array.

```python
def searchMatrix(matrix, target):
    if not matrix:
        return False
    m, n = len(matrix), len(matrix[0])
    left, right = 0, m * n - 1

    while left <= right:
        mid = (left + right) // 2
        val = matrix[mid // n][mid % n]
        if val == target:
            return True
        elif val < target:
            left = mid + 1
        else:
            right = mid - 1

    return False
```

**Time:** O(log(m * n)). **Space:** O(1).

For LC 240 (Search a 2D Matrix II) where rows and columns are sorted independently, use the staircase search from top-right corner in O(m + n) instead.

### Peak Element (LC 162)

Find any peak in an unsorted array where `nums[i] != nums[i+1]`. Binary search works because moving toward the larger neighbor guarantees a peak exists on that side.

```python
def findPeakElement(nums):
    left, right = 0, len(nums) - 1

    while left < right:
        mid = (left + right) // 2
        if nums[mid] < nums[mid + 1]:
            left = mid + 1  # peak is to the right
        else:
            right = mid  # peak is at mid or to the left

    return left
```

**Time:** O(log n). **Space:** O(1).

### Binary Search on Answer

This is arguably the most common binary search pattern in interviews. Instead of searching an array, you binary search on the **answer space** -- the range of possible results.

**When to use:** The problem asks to minimize/maximize some value, and you can write a function `feasible(x)` that checks whether `x` is an achievable answer. The feasibility function must be monotonic: if `x` works, then all values "beyond" `x` also work.

**Template:**

```python
def binary_search_on_answer(lo, hi):
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid  # mid works, try smaller (for minimization)
        else:
            lo = mid + 1  # mid doesn't work, need larger

    return lo  # smallest feasible answer
```

For **maximization**, flip the logic:

```python
def binary_search_on_answer_max(lo, hi):
    while lo < hi:
        mid = (lo + hi + 1) // 2  # round up to avoid infinite loop
        if feasible(mid):
            lo = mid  # mid works, try larger
        else:
            hi = mid - 1

    return lo  # largest feasible answer
```

#### Example 1: Koko Eating Bananas (LC 875)

Koko eats bananas at speed `k` bananas/hour. Given piles and `h` hours, find minimum `k`.

```python
import math

def minEatingSpeed(piles, h):
    lo, hi = 1, max(piles)

    def feasible(k):
        hours = sum(math.ceil(p / k) for p in piles)
        return hours <= h

    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1

    return lo
```

**Time:** O(n * log(max(piles))). **Space:** O(1).

#### Example 2: Capacity to Ship Packages (LC 1011)

Ship packages in order within `days` days. Find minimum ship capacity.

```python
def shipWithinDays(weights, days):
    lo, hi = max(weights), sum(weights)

    def feasible(cap):
        day_count, current = 1, 0
        for w in weights:
            if current + w > cap:
                day_count += 1
                current = 0
            current += w
        return day_count <= days

    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1

    return lo
```

**Time:** O(n * log(sum - max)). **Space:** O(1).

#### Example 3: Split Array Largest Sum (LC 410)

Split array into `k` subarrays to minimize the maximum subarray sum.

```python
def splitArray(nums, k):
    lo, hi = max(nums), sum(nums)

    def feasible(max_sum):
        count, current = 1, 0
        for num in nums:
            if current + num > max_sum:
                count += 1
                current = 0
            current += num
        return count <= k

    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1

    return lo
```

**Time:** O(n * log(sum - max)). **Space:** O(1).

### Square Root (LC 69)

Binary search on answer: find largest `x` where `x * x <= n`.

```python
def mySqrt(n):
    if n < 2:
        return n
    left, right = 1, n

    while left <= right:
        mid = (left + right) // 2
        if mid * mid == n:
            return mid
        elif mid * mid < n:
            left = mid + 1
        else:
            right = mid - 1

    return right  # largest integer where mid*mid <= n
```

**Time:** O(log n). **Space:** O(1).

---

## `left <= right` vs `left < right`

This is the most common source of binary search bugs. Here are the rules:

### Use `left <= right`

- Search space: `left, right = 0, len(nums) - 1`
- You want to find an **exact match** or the search space shrinks by at least 1 each iteration (`left = mid + 1` or `right = mid - 1`).
- When the loop exits, `left > right` and the search space is empty.
- Used in: standard search, first/last occurrence, rotated array.

### Use `left < right`

- Search space: usually `left, right = 0, len(nums)` (right is exclusive) or `left, right = 0, len(nums) - 1` but you set `right = mid` (not `mid - 1`).
- You want to **converge** to a single position. The loop exits when `left == right`.
- At least one branch must use `right = mid` (not `mid - 1`) -- otherwise you could skip the answer.
- Used in: lower/upper bound, peak element, binary search on answer (minimization).

### Watch out for infinite loops

When using `left < right` with `lo = mid` (maximization), you must round up: `mid = (lo + hi + 1) // 2`. Otherwise when `hi = lo + 1`, `mid = lo` and `lo = mid` never advances.

---

## Common Binary Search Patterns Table

| Pattern | Loop | Left Init | Right Init | Key Update |
|---|---|---|---|---|
| Exact match | `<=` | 0 | n-1 | `left = mid+1` / `right = mid-1` |
| First occurrence | `<=` | 0 | n-1 | Save result, `right = mid-1` |
| Last occurrence | `<=` | 0 | n-1 | Save result, `left = mid+1` |
| Lower bound | `<` | 0 | n | `right = mid` |
| Upper bound | `<` | 0 | n | `left = mid+1` |
| Search on answer (min) | `<` | lo | hi | `hi = mid` |
| Search on answer (max) | `<` | lo | hi | `lo = mid`, use `mid=(lo+hi+1)//2` |
| Peak element | `<` | 0 | n-1 | `right = mid` or `left = mid+1` |

---

## Complexity

All binary search variants: **O(log n)** time per search, **O(1)** space.

For binary search on answer: **O(f(n) * log(range))** where f(n) is the cost of the feasibility check and range is `hi - lo`.

---

## Common Mistakes

1. **Off-by-one in search bounds.** Using `right = len(nums)` with `left <= right` causes out-of-bounds access at `nums[mid]`. Match your bounds to your loop condition.
2. **Forgetting to handle empty arrays.** Check `if not nums` before searching.
3. **Integer overflow with `(left + right)`.** Not an issue in Python, but in C++/Java use `left + (right - left) // 2`.
4. **Using `right = mid - 1` in lower bound.** This skips the answer. Lower/upper bound needs `right = mid`.
5. **Not identifying the monotonic property.** Binary search on answer only works when feasibility is monotonic -- verify this before applying the pattern.
6. **Wrong bounds for binary search on answer.** The initial `lo` and `hi` must contain the answer. Think carefully: for shipping capacity, `lo = max(weights)` (must fit the heaviest package), `hi = sum(weights)` (ship everything in one day).
