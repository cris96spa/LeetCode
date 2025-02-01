# Binary Search Cheatsheet

## 1. **Standard Binary Search**

### **Problem:** Find a target element in a sorted array.

```python
from typing import List

def binary_search(nums: List[int], target: int) -> int:
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid  # Found target, return index
        elif nums[mid] < target:
            left = mid + 1  # Search right half
        else:
            right = mid - 1  # Search left half

    return -1  # Target not found
```

**Time Complexity:** \(O(\log n)\)

---

## 2. **Binary Search for First Occurrence**

### **Problem:** Find the first occurrence of `target` in a sorted array.

```python
from typing import List

def first_occurrence(nums: List[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    first_index = -1

    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            first_index = mid  # Update first occurrence
            right = mid - 1  # Keep searching left half
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return first_index
```

---

## 3. **Binary Search for Last Occurrence**

```python
from typing import List

def last_occurrence(nums: List[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    last_index = -1

    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            last_index = mid  # Update last occurrence
            left = mid + 1  # Keep searching right half
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return last_index
```

---

## 4. **Binary Search for Insert Position (Lower Bound)**

### **Problem:** Find the smallest index where `target` can be inserted while maintaining sorted order.

```python
from typing import List

def lower_bound(nums: List[int], target: int) -> int:
    left, right = 0, len(nums)

    while left < right:
        mid = (left + right) // 2
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid

    return left  # Insertion index
```

---

## 5. **Binary Search for Upper Bound**

### **Problem:** Find the first index where an element is greater than `target`.

```python
from typing import List

def upper_bound(nums: List[int], target: int) -> int:
    left, right = 0, len(nums)

    while left < right:
        mid = (left + right) // 2
        if nums[mid] <= target:
            left = mid + 1
        else:
            right = mid

    return left  # First index greater than target
```

---

## 6. **Binary Search in Rotated Sorted Array**

### **Problem:** Find an element in a rotated sorted array.

```python
from typing import List

def search_rotated(nums: List[int], target: int) -> int:
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid

        if nums[left] <= nums[mid]:  # Left half is sorted
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:  # Right half is sorted
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1

    return -1
```

---

## 7. **Square Root using Binary Search**

### **Problem:** Compute `sqrt(n)` without using `math.sqrt`.

```python

def sqrt(n: int) -> int:
    if n == 0 or n == 1:
        return n

    left, right = 1, n
    while left <= right:
        mid = (left + right) // 2
        if mid * mid == n:
            return mid
        elif mid * mid < n:
            left = mid + 1
            ans = mid  # Store possible integer sqrt
        else:
            right = mid - 1

    return ans  # Return the integer part of sqrt(n)
```

---

## **Common Binary Search Patterns**

| **Pattern**          | **Condition**                    | **Update Left/Right** |
| -------------------- | -------------------------------- | --------------------- |
| Standard Search      | `nums[mid] == target`            | Return `mid`          |
| First Occurrence     | `nums[mid] == target`            | `right = mid - 1`     |
| Last Occurrence      | `nums[mid] == target`            | `left = mid + 1`      |
| Lower Bound          | `nums[mid] < target`             | `left = mid + 1`      |
| Upper Bound          | `nums[mid] <= target`            | `left = mid + 1`      |
| Rotated Sorted Array | Check sorted half, adjust search | `left/right` updates  |

---

## **Binary Search Tips & Tricks**

1. **Always check for `left <= right` vs `left < right`.**

   - `left <= right`: When searching for an exact element.
   - `left < right`: When searching for bounds (lower/upper bound).

2. **Use `(left + right) // 2` cautiously to prevent overflow.**

   - In some languages (like C++/Java), use `left + (right - left) // 2`.

3. **Binary search works on monotonic functions.**

   - It doesn’t always require a sorted array. It can be used in function-based problems where values change in a predictable way.

4. **If stuck, manually simulate iterations with a small array.**

   - Writing out index updates for each iteration helps in debugging.

5. **Binary search can be used for optimization problems.**
   - E.g., "minimum time to complete tasks" (Binary search on answer).

---

### 🚀 Master these patterns, and you'll solve a wide range of problems using binary search efficiently!
