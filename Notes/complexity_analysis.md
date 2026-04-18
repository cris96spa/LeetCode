# Complexity Analysis

## Big O Fundamentals

Big O describes the growth rate of time or space as input size (n) approaches infinity.

### Common Complexities

| Big O | Name | Example |
|-------|------|---------|
| O(1) | Constant | Array access, hash lookup |
| O(log n) | Logarithmic | Binary search |
| O(n) | Linear | Array traversal |
| O(n log n) | Linearithmic | Merge sort |
| O(n^2) | Quadratic | Nested loops |
| O(2^n) | Exponential | Subsets, naive Fibonacci |
| O(n!) | Factorial | Permutations |

### Growth Comparison

| n | O(log n) | O(n) | O(n log n) | O(n^2) | O(2^n) |
|---|----------|------|------------|--------|--------|
| 10 | 3 | 10 | 33 | 100 | 1,024 |
| 100 | 7 | 100 | 664 | 10,000 | 1.27 x 10^30 |
| 1,000 | 10 | 1,000 | 9,966 | 10^6 | -- |

---

## Calculation Rules

### Drop Constants

`O(2n)` -> `O(n)`. Two sequential loops over `n` is still `O(n)`.

### Drop Non-Dominant Terms

`O(n^2 + n)` -> `O(n^2)`. The fastest-growing term dominates.

### Different Inputs = Different Variables

```python
# O(a + b), NOT O(n)
for i in range(len(a)):
    print(i)
for j in range(len(b)):
    print(j)

# O(a * b), NOT O(n^2)
for i in range(len(a)):
    for j in range(len(b)):
        print(i, j)
```

---

## Time Complexity by Pattern

### O(1) - Constant

```python
def get_middle(arr):
    return arr[len(arr) // 2]
```

### O(log n) - Logarithmic

Halving the search space each step. `n -> n/2 -> n/4 -> ... -> 1` takes `log2(n)` steps.

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

### O(n) - Linear

```python
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        if target - num in seen:
            return [seen[target - num], i]
        seen[num] = i
```

### O(n log n) - Linearithmic

Divide into `log n` levels, `O(n)` work per level.

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)  # merge is O(n)
```

### O(n^2) - Quadratic

```python
def has_duplicate_brute(arr):
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] == arr[j]:
                return True
    return False
```

### O(2^n) - Exponential

```python
def fib_naive(n):
    if n <= 1:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)
```

Two branches per call, `n` levels deep. Memoization reduces this to O(n).

### O(n!) - Factorial

```python
def permutations(arr, path=[]):
    if not arr:
        print(path)
        return
    for i in range(len(arr)):
        permutations(arr[:i] + arr[i+1:], path + [arr[i]])
```

---

## Space Complexity

### Stack Frames

Every recursive call adds a frame to the call stack.

```python
def factorial(n):          # O(n) space from call stack
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

Iterative binary search: O(1) space. Recursive binary search: O(log n) space from the call stack.

### Auxiliary Space vs Total Space

- **Auxiliary space:** extra space beyond the input.
- **Total space:** input + auxiliary.

When people say "O(1) space," they usually mean auxiliary space.

### In-place Algorithms

Modify the input directly instead of creating new data structures. Examples: in-place quicksort, reversing an array with two pointers.

---

## Analysis Techniques

### Counting Loops

```python
# Single loop = O(n)
for i in range(n): pass

# Nested loops, same input = O(n^2)
for i in range(n):
    for j in range(n): pass

# Inner loop depends on outer = O(n^2/2) = O(n^2)
for i in range(n):
    for j in range(i, n): pass

# Multiplicative shrinking = O(log n)
i = n
while i > 0:
    i //= 2
```

### Master Theorem

For divide-and-conquer recurrences `T(n) = aT(n/b) + O(n^d)`:

| Condition | Result |
|-----------|--------|
| a > b^d | O(n^(log_b(a))) |
| a = b^d | O(n^d * log n) |
| a < b^d | O(n^d) |

**Examples:**

| Algorithm | Recurrence | a, b, d | Complexity |
|-----------|-----------|---------|------------|
| Binary Search | T(n) = T(n/2) + O(1) | 1, 2, 0 | O(log n) |
| Merge Sort | T(n) = 2T(n/2) + O(n) | 2, 2, 1 | O(n log n) |
| Strassen | T(n) = 7T(n/2) + O(n^2) | 7, 2, 2 | O(n^2.81) |

### Amortized Analysis

**Amortized cost** = total cost of all operations / number of operations.

Individual operations may be expensive, but the average over a sequence is cheap.

**Dynamic array (e.g., Python list.append):**
- Most appends: O(1) -- just write to preallocated space.
- Occasional resize: copy all n elements -> O(n).
- Resizes happen at sizes 1, 2, 4, 8, ..., n. Total copy cost: `1 + 2 + 4 + ... + n = 2n`.
- Over n appends, total cost is ~3n. Amortized per append: **O(1)**.

**Accounting method intuition:** "charge" each cheap operation a little extra (e.g., 3 units instead of 1). The surplus pays for the rare expensive operation. If the account never goes negative, the amortized cost is the charge per operation.

---

## Data Structure Operations

| Data Structure | Access | Search | Insert | Delete | Notes |
|---------------|--------|--------|--------|--------|-------|
| Array | O(1) | O(n) | O(n) | O(n) | Insert/delete shift elements |
| Sorted Array | O(1) | O(log n) | O(n) | O(n) | Binary search for lookup |
| Hash Map | O(1)* | O(1)* | O(1)* | O(1)* | *Average case |
| Linked List | O(n) | O(n) | O(1) | O(1) | Insert/delete at known position |
| Binary Heap | O(1) top | O(n) | O(log n) | O(log n) | Min/max at top |
| BST (balanced) | O(log n) | O(log n) | O(log n) | O(log n) | AVL, Red-Black |
| Trie | -- | O(k) | O(k) | O(k) | k = key length |

**Hash table collision note:** Average O(1) assumes a good hash function with low collision rate. Worst case is O(n) when all keys hash to the same bucket (e.g., adversarial input). Python dicts use open addressing with perturbation, making pathological cases rare but not impossible. In interviews, state "O(1) average, O(n) worst case" when precision matters.

## Sorting Algorithms Comparison

| Algorithm | Best | Average | Worst | Space | Stable | Notes |
|-----------|------|---------|-------|-------|--------|-------|
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes | Predictable, good for linked lists |
| Quick Sort | O(n log n) | O(n log n) | O(n^2) | O(log n) | No | Fastest in practice (cache-friendly) |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) | No | In-place, guaranteed O(n log n) |
| Counting Sort | O(n + k) | O(n + k) | O(n + k) | O(k) | Yes | k = range of values; integers only |
| Radix Sort | O(nk) | O(nk) | O(nk) | O(n + k) | Yes | k = number of digits |
| Timsort | O(n) | O(n log n) | O(n log n) | O(n) | Yes | Python's built-in `sorted()` |

**When to use which:**
- Default: use the language's built-in sort (Timsort in Python, O(n log n)).
- Need O(1) space: heap sort.
- Need stability: merge sort.
- Integer keys in small range: counting sort.

## Input Size -> Acceptable Complexity

| n | Max Complexity | Typical Approach |
|---|---------------|-----------------|
| n <= 10 | O(n!) | Brute force, permutations |
| n <= 20 | O(2^n) | Bitmask DP, backtracking |
| n <= 500 | O(n^3) | Floyd-Warshall, interval DP |
| n <= 5,000 | O(n^2) | DP, nested loops |
| n <= 100,000 | O(n log n) | Sorting, heaps, balanced BST |
| n <= 10^6 | O(n) | Linear scan, hash map |
| n <= 10^9 | O(log n) or O(1) | Binary search, math |

## Common Mistakes

1. **Confusing O(n) with O(log n).**
   ```python
   # O(n) -- linear increment
   while i < n:
       i += 1

   # O(log n) -- multiplicative increment
   while i < n:
       i *= 2
   ```

2. **Forgetting space from recursion.** A recursive function with depth `d` uses O(d) stack space even if no extra data structures are allocated.

3. **Hidden O(n) operations inside loops.**
   ```python
   for i in range(n):
       arr.pop(0)    # O(n) shift! Total: O(n^2)

   for i in range(n):
       if x in my_list:  # O(n) search! Total: O(n^2)
           pass
   ```

4. **String concatenation in a loop.** In Python, `s += char` inside a loop is O(n) per concatenation (creates a new string). Total: O(n^2). Use `"".join(parts)` instead.

5. **Ignoring the cost of slicing.** `arr[1:]` creates a copy in O(n). Passing slices in recursion can silently add O(n) per level.
