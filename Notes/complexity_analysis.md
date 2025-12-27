# Complexity Analysis - Master Big O

**Why This Matters:** Understanding complexity is crucial for:
- Choosing optimal algorithms
- Passing Google's efficiency bar
- Scaling solutions to production
- Communicating tradeoffs clearly

---

## Big O Notation Fundamentals

**Big O describes growth rate** as input size (n) approaches infinity.

### Common Complexities (Best to Worst)

| Big O | Name | Example |
|-------|------|---------|
| O(1) | Constant | Array access, hash lookup |
| O(log n) | Logarithmic | Binary search |
| O(n) | Linear | Array traversal |
| O(n log n) | Linearithmic | Merge sort, heap sort |
| O(n²) | Quadratic | Nested loops, bubble sort |
| O(n³) | Cubic | 3 nested loops |
| O(2ⁿ) | Exponential | Recursive Fibonacci |
| O(n!) | Factorial | Permutations |

### Visual Growth Comparison

```
n = 10:
O(1) = 1
O(log n) = 3
O(n) = 10
O(n log n) = 30
O(n²) = 100
O(2ⁿ) = 1,024
O(n!) = 3,628,800

n = 100:
O(1) = 1
O(log n) = 7
O(n) = 100
O(n log n) = 664
O(n²) = 10,000
O(2ⁿ) = 1.27 × 10³⁰
O(n!) = 9.33 × 10¹⁵⁷
```

---

## Rules for Calculating Time Complexity

### Rule 1: Drop Constants

```python
# O(2n) → O(n)
for i in range(n):
    print(i)
for i in range(n):
    print(i)

# O(n + 1000) → O(n)
for i in range(n):
    print(i)
for i in range(1000):
    print(i)
```

### Rule 2: Drop Non-Dominant Terms

```python
# O(n² + n) → O(n²)
for i in range(n):
    for j in range(n):
        print(i, j)
for i in range(n):
    print(i)

# O(n log n + n) → O(n log n)
```

### Rule 3: Different Inputs → Different Variables

```python
# O(a + b) NOT O(n)
for i in range(len(array_a)):
    print(i)
for j in range(len(array_b)):
    print(j)

# O(a * b) NOT O(n²)
for i in range(len(array_a)):
    for j in range(len(array_b)):
        print(i, j)
```

### Rule 4: Amortized Analysis

```python
# Dynamic array append: O(1) amortized
# Occasional O(n) resize, but average is O(1)
arr = []
for i in range(n):
    arr.append(i)  # O(1) amortized, total O(n)
```

---

## Common Time Complexities Explained

### O(1) - Constant Time

**Operations that don't depend on input size:**

```python
# Array/dict access
value = arr[5]
value = hash_map['key']

# Math operations
result = a + b
result = a * b

# Comparison
if a > b:
    pass
```

**Real Interview Example:**
```python
def get_middle(arr):
    return arr[len(arr) // 2]  # O(1)
```

---

### O(log n) - Logarithmic Time

**Halving search space each iteration:**

```python
# Binary search
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:  # O(log n) iterations
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1
```

**Why log n?** 
- Each iteration cuts problem in half
- n → n/2 → n/4 → ... → 1
- Number of steps = log₂(n)

**Other O(log n) operations:**
- Binary tree height (balanced)
- Heap operations
- Balanced BST operations

---

### O(n) - Linear Time

**Iterate through data once:**

```python
# Single loop
def find_max(arr):
    max_val = arr[0]
    for num in arr:  # O(n)
        max_val = max(max_val, num)
    return max_val

# Multiple loops (still O(n))
def process(arr):
    # O(n + n + n) = O(3n) = O(n)
    sum_val = sum(arr)
    max_val = max(arr)
    min_val = min(arr)
    return sum_val, max_val, min_val
```

**Real Interview Example:**
```python
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):  # O(n)
        if target - num in seen:
            return [seen[target - num], i]
        seen[num] = i
    return []
```

---

### O(n log n) - Linearithmic Time

**Optimal sorting complexity:**

```python
# Merge sort
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])   # T(n/2)
    right = merge_sort(arr[mid:])  # T(n/2)
    
    return merge(left, right)      # O(n)

# Recurrence: T(n) = 2T(n/2) + O(n) = O(n log n)
```

**Why n log n?**
- log n levels of recursion
- O(n) work per level
- Total: O(n) × O(log n) = O(n log n)

**Common O(n log n) scenarios:**
- Sorting: merge sort, heap sort, quick sort (average)
- Building heap from unsorted array
- Divide and conquer with linear merge

---

### O(n²) - Quadratic Time

**Nested loops over same input:**

```python
# Checking all pairs
def has_duplicate_pairs(arr):
    for i in range(len(arr)):      # O(n)
        for j in range(i + 1, len(arr)):  # O(n)
            if arr[i] == arr[j]:
                return True
    return False

# Total: O(n²)
```

**Optimizing to O(n):**
```python
def has_duplicate_pairs(arr):
    seen = set()
    for num in arr:  # O(n)
        if num in seen:
            return True
        seen.add(num)
    return False
```

---

### O(2ⁿ) - Exponential Time

**Branching recursion without memoization:**

```python
# Naive Fibonacci
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)  # Two recursive calls

# Call tree for fib(5):
#           fib(5)
#          /      \
#      fib(4)    fib(3)
#      /   \      /   \
#   fib(3) fib(2) ...
```

**Optimization to O(n):**
```python
def fib(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    
    memo[n] = fib(n - 1, memo) + fib(n - 2, memo)
    return memo[n]
```

---

## Space Complexity Analysis

**Space = Memory used beyond input**

### O(1) Space - Constant

```python
def swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]  # Only temp variables

def reverse(arr):
    left, right = 0, len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
```

### O(n) Space - Linear

```python
# Creating new array
def double(arr):
    return [x * 2 for x in arr]  # O(n) space

# Hash map
def count_freq(arr):
    freq = {}  # O(n) space worst case
    for num in arr:
        freq[num] = freq.get(num, 0) + 1
    return freq
```

### O(log n) Space - Logarithmic

```python
# Binary search recursion (call stack)
def binary_search(arr, target, left, right):
    if left > right:
        return -1
    
    mid = (left + right) // 2
    
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search(arr, target, mid + 1, right)
    else:
        return binary_search(arr, target, left, mid - 1)

# Call stack depth: O(log n)
```

### Recursive Call Stack

```python
# O(n) space from recursion
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)  # n recursive calls

# Call stack:
# factorial(5)
#   factorial(4)
#     factorial(3)
#       factorial(2)
#         factorial(1)
```

---

## Complexity Analysis Strategies

### Strategy 1: Count Loops

```python
# Single loop = O(n)
for i in range(n):
    pass

# Nested loops (same input) = O(n²)
for i in range(n):
    for j in range(n):
        pass

# Independent loops = O(n + m)
for i in range(n):
    pass
for j in range(m):
    pass
```

### Strategy 2: Identify Recursive Pattern

**Master Theorem** for divide and conquer:
```
T(n) = aT(n/b) + O(n^d)

If a > b^d: O(n^log_b(a))
If a = b^d: O(n^d log n)
If a < b^d: O(n^d)
```

**Examples:**
```python
# Merge Sort: T(n) = 2T(n/2) + O(n)
# a=2, b=2, d=1 → a = b^d → O(n log n)

# Binary Search: T(n) = T(n/2) + O(1)
# a=1, b=2, d=0 → a = b^d → O(log n)
```

### Strategy 3: Analyze Data Structures

| Data Structure | Access | Search | Insert | Delete |
|---------------|--------|--------|--------|--------|
| Array | O(1) | O(n) | O(n) | O(n) |
| Sorted Array | O(1) | O(log n) | O(n) | O(n) |
| Hash Map | O(1) | O(1) | O(1) | O(1) |
| Linked List | O(n) | O(n) | O(1) | O(1) |
| Binary Heap | O(1) | O(n) | O(log n) | O(log n) |
| BST (balanced) | O(log n) | O(log n) | O(log n) | O(log n) |

---

## Common Interview Patterns

### Pattern 1: Trading Space for Time

**Problem: Two Sum**

```python
# O(n²) time, O(1) space
def two_sum_slow(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]

# O(n) time, O(n) space
def two_sum_fast(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        if target - num in seen:
            return [seen[target - num], i]
        seen[num] = i
```

### Pattern 2: Amortized Analysis

**Dynamic Array Doubling:**
```
Insertions: n
Resizes: 1 + 2 + 4 + 8 + ... + n/2 = 2n
Total cost: 3n
Amortized per insertion: O(1)
```

### Pattern 3: Best, Average, Worst Case

**Quick Sort:**
- Best: O(n log n) - balanced partitions
- Average: O(n log n)
- Worst: O(n²) - already sorted

**Hash Map:**
- Average: O(1) - good hash function
- Worst: O(n) - all collisions

---

## Google Interview Tips

### 1. Always State Complexity

**Template:**
```
"My solution has O(n log n) time complexity due to sorting,
and O(n) space complexity for the hash map."
```

### 2. Discuss Tradeoffs

```
"We can optimize from O(n²) to O(n log n) by sorting first,
which costs O(n log n) time but reduces the nested loop."
```

### 3. Consider Input Constraints

```
If n ≤ 100: O(n³) is acceptable
If n ≤ 10,000: O(n²) is acceptable
If n ≤ 1,000,000: O(n log n) required
If n ≤ 10⁹: O(n) or O(log n) required
```

### 4. Optimize Step by Step

1. Brute force → state complexity
2. Identify bottleneck
3. Apply data structure or algorithm
4. Analyze new complexity

---

## Practice Problems by Complexity

### O(log n)
- LC 33 - Search in Rotated Array
- LC 153 - Find Minimum in Rotated Array
- LC 875 - Koko Eating Bananas

### O(n)
- LC 1 - Two Sum
- LC 121 - Best Time to Buy Stock
- LC 3 - Longest Substring Without Repeating

### O(n log n)
- LC 56 - Merge Intervals
- LC 15 - 3Sum
- LC 347 - Top K Frequent

### O(n²)
- LC 15 - 3Sum (optimized from O(n³))
- LC 200 - Number of Islands

---

## Common Mistakes

1. **Confusing O(n) loops with O(log n)**
   ```python
   # This is O(n), not O(log n)
   while i < n:
       i += 1  # Linear increment
   
   # This is O(log n)
   while i < n:
       i *= 2  # Exponential increment
   ```

2. **Forgetting space complexity of recursion**
   ```python
   def sum_array(arr):
       if not arr:
           return 0
       return arr[0] + sum_array(arr[1:])
   
   # Time: O(n), Space: O(n) from call stack
   ```

3. **Missing hidden complexity**
   ```python
   for i in range(n):
       arr.pop(0)  # O(n) operation!
   
   # Total: O(n²), not O(n)
   ```

---

## Quick Reference Table

| n size | Max acceptable complexity |
|--------|--------------------------|
| n ≤ 10 | O(n!) |
| n ≤ 20 | O(2ⁿ) |
| n ≤ 500 | O(n³) |
| n ≤ 5,000 | O(n²) |
| n ≤ 100,000 | O(n log n) |
| n ≤ 1,000,000 | O(n) |
| n ≤ 10⁹ | O(log n) or O(1) |

---

**Master complexity analysis, and you'll write efficient code from the start!**
