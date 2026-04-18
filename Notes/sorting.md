# Sorting

## Built-in Sorting

Python uses **Timsort**: O(n log n) time, O(n) space, stable.

```python
# Returns new sorted list (original unchanged)
sorted_list = sorted(arr)

# In-place sort (returns None)
arr.sort()

# Custom key
sorted(arr, key=lambda x: x[1])                    # sort by second element
sorted(arr, key=lambda x: (-x[1], x[0]))           # sort by x[1] desc, then x[0] asc

# Custom comparator (when key function isn't enough)
from functools import cmp_to_key
def compare(a, b):
    # return negative if a < b, 0 if equal, positive if a > b
    if a + b > b + a:
        return -1
    elif a + b < b + a:
        return 1
    return 0
sorted(strs, key=cmp_to_key(compare))
```

---

## Comparison-Based Sorts

### Merge Sort

Divide array in half, recursively sort each half, merge the sorted halves.

- **Time:** O(n log n) always
- **Space:** O(n) for the auxiliary arrays
- **Stable:** Yes
- **When to use:** need stability, linked list sorting (O(1) space possible), external sorting, counting inversions

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:   # <= for stability
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

**In-place merge sort** (reduces copies but still O(n) space for merge):
```python
def merge_sort_inplace(arr, left, right):
    if right - left <= 1:
        return
    mid = (left + right) // 2
    merge_sort_inplace(arr, left, mid)
    merge_sort_inplace(arr, mid, right)
    merge_inplace(arr, left, mid, right)

def merge_inplace(arr, left, mid, right):
    temp = []
    i, j = left, mid
    while i < mid and j < right:
        if arr[i] <= arr[j]:
            temp.append(arr[i])
            i += 1
        else:
            temp.append(arr[j])
            j += 1
    temp.extend(arr[i:mid])
    temp.extend(arr[j:right])
    arr[left:right] = temp
```

### Quick Sort

Pick a pivot, partition array into elements < pivot and >= pivot, recursively sort partitions.

- **Time:** O(n log n) average, O(n^2) worst (already sorted + bad pivot)
- **Space:** O(log n) average (recursion stack), O(n) worst
- **Stable:** No
- **When to use:** in-place sorting, average case performance matters

```python
import random

def quick_sort(arr, lo, hi):
    if lo >= hi:
        return
    pivot_idx = partition(arr, lo, hi)
    quick_sort(arr, lo, pivot_idx - 1)
    quick_sort(arr, pivot_idx + 1, hi)

def partition(arr, lo, hi):
    # Randomized pivot to avoid O(n^2) on sorted input
    rand_idx = random.randint(lo, hi)
    arr[rand_idx], arr[hi] = arr[hi], arr[rand_idx]
    
    pivot = arr[hi]
    i = lo  # i tracks where next smaller element goes
    for j in range(lo, hi):
        if arr[j] < pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    arr[i], arr[hi] = arr[hi], arr[i]
    return i

# Usage:
# quick_sort(arr, 0, len(arr) - 1)
```

**Lomuto partition** (shown above): pivot goes to final position, everything left is smaller, everything right is >= pivot.

### Heap Sort

Build a max heap, repeatedly extract the max.

- **Time:** O(n log n) always
- **Space:** O(1) in-place
- **Stable:** No
- **When to use:** O(1) space needed with guaranteed O(n log n). Rarely asked to implement; know the properties.

```python
def heap_sort(arr):
    import heapq
    heapq.heapify(arr)  # min heap, O(n)
    return [heapq.heappop(arr) for _ in range(len(arr))]
```

Note: the above uses extra space. A true in-place heap sort builds a max heap and swaps the root to the end repeatedly, but Python's `heapq` is a min heap so the manual approach is verbose. Know the concept; you won't be asked to code it.

---

## Non-Comparison Sorts

These break the O(n log n) lower bound by not comparing elements.

### Counting Sort

Count occurrences of each value, reconstruct the sorted array.

- **Time:** O(n + k) where k = range of values
- **Space:** O(n + k)
- **Stable:** Yes (with the right implementation)
- **When to use:** small range of non-negative integer values

```python
def counting_sort(arr):
    if not arr:
        return arr
    max_val = max(arr)
    count = [0] * (max_val + 1)
    for x in arr:
        count[x] += 1
    
    result = []
    for val, cnt in enumerate(count):
        result.extend([val] * cnt)
    return result
```

**Stable version** (preserves relative order, needed when sorting objects by key):
```python
def counting_sort_stable(arr):
    if not arr:
        return arr
    max_val = max(arr)
    count = [0] * (max_val + 1)
    for x in arr:
        count[x] += 1
    
    # Prefix sum: count[i] = number of elements <= i
    for i in range(1, len(count)):
        count[i] += count[i - 1]
    
    result = [0] * len(arr)
    for x in reversed(arr):  # reversed for stability
        count[x] -= 1
        result[count[x]] = x
    return result
```

### Bucket Sort

Distribute elements into buckets, sort each bucket, concatenate.

- **Time:** O(n) average (when elements are uniformly distributed), O(n^2) worst
- **Space:** O(n + k) where k = number of buckets
- **When to use:** uniformly distributed floating point numbers, or when range is known

```python
def bucket_sort(arr, num_buckets=10):
    if not arr:
        return arr
    min_val, max_val = min(arr), max(arr)
    if min_val == max_val:
        return arr[:]
    
    bucket_range = (max_val - min_val) / num_buckets
    buckets = [[] for _ in range(num_buckets)]
    
    for x in arr:
        idx = min(int((x - min_val) / bucket_range), num_buckets - 1)
        buckets[idx].append(x)
    
    result = []
    for bucket in buckets:
        bucket.sort()  # or use insertion sort for small buckets
        result.extend(bucket)
    return result
```

### Radix Sort

Sort by each digit position, from least significant to most significant (LSD) or vice versa (MSD). Uses counting sort as a subroutine.

- **Time:** O(d * (n + k)) where d = number of digits, k = base (usually 10)
- **Space:** O(n + k)
- **Stable:** Yes (relies on stable per-digit sort)
- **When to use:** fixed-length integers, strings of same length

```python
def radix_sort(arr):
    if not arr:
        return arr
    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        arr = counting_sort_by_digit(arr, exp)
        exp *= 10
    return arr

def counting_sort_by_digit(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    
    for x in arr:
        digit = (x // exp) % 10
        count[digit] += 1
    
    for i in range(1, 10):
        count[i] += count[i - 1]
    
    for x in reversed(arr):
        digit = (x // exp) % 10
        count[digit] -= 1
        output[count[digit]] = x
    
    return output
```

---

## QuickSelect (Kth Element)

Find the kth smallest element without fully sorting. Uses the same partition as quicksort but only recurses into one side.

- **Time:** O(n) average, O(n^2) worst
- **Space:** O(1) (iterative version)
- **Used in:** Kth Largest Element (LC 215), see also `heaps.md` for heap-based approach

```python
import random

def quick_select(arr, k):
    """Find the kth smallest element (0-indexed)."""
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        pivot_idx = partition(arr, lo, hi)
        if pivot_idx == k:
            return arr[k]
        elif pivot_idx < k:
            lo = pivot_idx + 1
        else:
            hi = pivot_idx - 1
    return arr[lo]

def partition(arr, lo, hi):
    rand_idx = random.randint(lo, hi)
    arr[rand_idx], arr[hi] = arr[hi], arr[rand_idx]
    pivot = arr[hi]
    i = lo
    for j in range(lo, hi):
        if arr[j] < pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    arr[i], arr[hi] = arr[hi], arr[i]
    return i

# Kth largest = (n - k)th smallest
# quick_select(arr, len(arr) - k)
```

Note: this modifies the input array. For LC 215, `k` is 1-indexed, so find the `(n - k)`th smallest.

---

## Sorting-Based Interview Patterns

### Sort Then Two Pointers
3Sum (LC 15): sort, fix one element, two-pointer on the rest. O(n^2).

### Sort Then Binary Search
Search for complement after sorting. Often O(n log n).

### Sort by Custom Key
**Largest Number (LC 179):** compare `a+b` vs `b+a` as strings.
```python
from functools import cmp_to_key

def largestNumber(nums):
    strs = list(map(str, nums))
    strs.sort(key=cmp_to_key(lambda a, b: (1 if a + b < b + a else -1)))
    result = ''.join(strs)
    return '0' if result[0] == '0' else result
```

**Merge Intervals:** sort by start time. See `intervals.md`.

### Bucket Sort for O(n)
**Top K Frequent Elements (LC 347):** use bucket sort where index = frequency.
```python
def topKFrequent(nums, k):
    from collections import Counter
    counts = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]
    for num, freq in counts.items():
        buckets[freq].append(num)
    
    result = []
    for i in range(len(buckets) - 1, -1, -1):
        for num in buckets[i]:
            result.append(num)
            if len(result) == k:
                return result
    return result
```

**Maximum Gap (LC 164):** bucket sort / pigeonhole principle to find max gap in O(n).

---

## Comparison Table

| Algorithm    | Best      | Average   | Worst     | Space   | Stable |
|-------------|-----------|-----------|-----------|---------|--------|
| Merge Sort  | O(n lg n) | O(n lg n) | O(n lg n) | O(n)    | Yes    |
| Quick Sort  | O(n lg n) | O(n lg n) | O(n^2)    | O(lg n) | No     |
| Heap Sort   | O(n lg n) | O(n lg n) | O(n lg n) | O(1)    | No     |
| Counting    | O(n + k)  | O(n + k)  | O(n + k)  | O(k)    | Yes    |
| Radix       | O(d(n+k)) | O(d(n+k)) | O(d(n+k)) | O(n+k)  | Yes    |
| Bucket      | O(n + k)  | O(n + k)  | O(n^2)    | O(n+k)  | Yes*   |
| Timsort     | O(n)      | O(n lg n) | O(n lg n) | O(n)    | Yes    |

\* Bucket sort stability depends on the inner sort.

---

## Stability: Why It Matters

A **stable** sort preserves the relative order of elements with equal keys.

**Practical use:** sort by multiple criteria. Sort by secondary key first, then by primary key with a stable sort. The secondary ordering is preserved within equal primary keys.

```python
# Sort students by grade (primary, desc) then name (secondary, asc)
# Because Python's sort is stable, we can do:
students.sort(key=lambda x: x.name)         # secondary first
students.sort(key=lambda x: -x.grade)       # primary second (stable preserves name order)

# Or in one pass with a tuple key:
students.sort(key=lambda x: (-x.grade, x.name))
```

---

## Common Mistakes

- **Forgetting Python's sort is stable:** exploit this for multi-key sorting.
- **Using O(n^2) sort when O(n log n) is needed:** insertion/selection/bubble sort are O(n^2). Never use them on large inputs in interviews unless specifically asked.
- **Not considering non-comparison sorts:** when the value range is bounded (e.g., ages 0-150, ASCII chars), counting sort gives O(n).
- **Partition bugs in quicksort:** off-by-one errors, infinite recursion when all elements are equal (Lomuto handles this but Hoare needs care), forgetting to randomize pivot.
- **Assuming quicksort is O(n log n):** it's O(n^2) worst case. Mention randomized pivot.
- **Modifying input in quickselect:** if the input shouldn't be modified, work on a copy.
- **Wrong direction in radix sort:** LSD (least significant digit first) is the standard approach for integers. Processing most significant first requires different handling (MSD radix sort with recursion).
