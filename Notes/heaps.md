# Heaps & Priority Queues - Complete Guide

**Interview Frequency:** ⭐⭐⭐⭐ (55% of FAANG interviews)  
**Google Frequency:** ⭐⭐⭐⭐ (Common in system design context)  
**Mastery Time:** 4-5 hours

## What is a Heap?

A **heap** is a complete binary tree that satisfies the heap property:
- **Min Heap:** Parent ≤ Children (smallest at root)
- **Max Heap:** Parent ≥ Children (largest at root)

**Key Properties:**
- **Complete binary tree:** All levels filled except possibly last (filled left-to-right)
- **Efficient operations:** Insert and extract in O(log n)
- **Array representation:** Parent at `i`, children at `2i+1` and `2i+2`

---

## Python's `heapq` Module

Python only provides **min heap** by default.

### Basic Operations

```python
import heapq

# Create heap from list (in-place)
nums = [3, 1, 4, 1, 5, 9, 2, 6]
heapq.heapify(nums)  # O(n)

# Push element
heapq.heappush(nums, 7)  # O(log n)

# Pop smallest
smallest = heapq.heappop(nums)  # O(log n)

# Peek smallest (without removing)
smallest = nums[0]  # O(1)

# Push and pop in one operation
result = heapq.heappushpop(nums, 8)  # O(log n)

# Pop and push (slightly more efficient than separate)
result = heapq.heapreplace(nums, 8)  # O(log n)

# Get n smallest/largest
smallest_3 = heapq.nsmallest(3, nums)  # O(n log k)
largest_3 = heapq.nlargest(3, nums)   # O(n log k)
```

### Max Heap Trick

**Negate values** to simulate max heap:

```python
# Max heap
max_heap = []
heapq.heappush(max_heap, -5)
heapq.heappush(max_heap, -3)
heapq.heappush(max_heap, -7)

max_val = -heapq.heappop(max_heap)  # 7
```

### Heap with Custom Objects

```python
# Using tuples (compared by first element)
heap = []
heapq.heappush(heap, (priority, item))
priority, item = heapq.heappop(heap)

# Using dataclass with comparison
from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any = field(compare=False)

heap = []
heapq.heappush(heap, PrioritizedItem(5, "task"))
```

---

## Pattern 1: K-th Largest/Smallest Element

### K-th Largest Element (LC 215) ⭐⭐⭐⭐⭐

**Approach 1: Min Heap of size K**
```python
def findKthLargest(nums: List[int], k: int) -> int:
    # Maintain min heap of k largest elements
    # Root of heap is k-th largest
    
    heap = []
    
    for num in nums:
        heapq.heappush(heap, num)
        
        # Keep only k largest
        if len(heap) > k:
            heapq.heappop(heap)
    
    return heap[0]
```

**Complexity:** O(n log k) time, O(k) space

**Approach 2: Heapify (faster for large k)**
```python
def findKthLargest(nums: List[int], k: int) -> int:
    # Negate for max heap
    nums = [-num for num in nums]
    heapq.heapify(nums)
    
    # Pop k-1 times
    for _ in range(k - 1):
        heapq.heappop(nums)
    
    return -heapq.heappop(nums)
```

**Complexity:** O(n + k log n) time, O(1) space

**Approach 3: QuickSelect (Optimal but not heap-based)**
```python
def findKthLargest(nums: List[int], k: int) -> int:
    k = len(nums) - k  # Convert to k-th smallest
    
    def quickselect(left, right):
        pivot = nums[right]
        i = left
        
        for j in range(left, right):
            if nums[j] <= pivot:
                nums[i], nums[j] = nums[j], nums[i]
                i += 1
        
        nums[i], nums[right] = nums[right], nums[i]
        
        if i == k:
            return nums[i]
        elif i < k:
            return quickselect(i + 1, right)
        else:
            return quickselect(left, i - 1)
    
    return quickselect(0, len(nums) - 1)
```

**Complexity:** O(n) average, O(n²) worst case

---

## Pattern 2: Top K Frequent Elements

### Top K Frequent Elements (LC 347) ⭐⭐⭐⭐⭐

**Approach: Heap**
```python
def topKFrequent(nums: List[int], k: int) -> List[int]:
    from collections import Counter
    
    # Count frequencies
    count = Counter(nums)
    
    # Use heap to find k most frequent
    # Negate frequency for max heap behavior
    return [num for num, freq in count.most_common(k)]

# Manual heap implementation
def topKFrequent(nums: List[int], k: int) -> List[int]:
    from collections import Counter
    
    count = Counter(nums)
    
    # Min heap of size k (by frequency)
    heap = []
    
    for num, freq in count.items():
        heapq.heappush(heap, (freq, num))
        
        if len(heap) > k:
            heapq.heappop(heap)
    
    return [num for freq, num in heap]
```

**Complexity:** O(n log k) time, O(n) space

**Bucket Sort Approach (Optimal):**
```python
def topKFrequent(nums: List[int], k: int) -> List[int]:
    from collections import Counter
    
    count = Counter(nums)
    
    # Bucket sort by frequency
    buckets = [[] for _ in range(len(nums) + 1)]
    
    for num, freq in count.items():
        buckets[freq].append(num)
    
    # Collect k most frequent
    result = []
    for i in range(len(buckets) - 1, 0, -1):
        result.extend(buckets[i])
        if len(result) >= k:
            return result[:k]
```

**Complexity:** O(n) time and space

---

## Pattern 3: K-Way Merge

### Merge K Sorted Lists (LC 23) ⭐⭐⭐⭐⭐

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def mergeKLists(lists: List[ListNode]) -> ListNode:
    # Heap to track smallest element from each list
    heap = []
    
    # Initialize heap with first node from each list
    for i, node in enumerate(lists):
        if node:
            # Use index as tiebreaker (nodes can't be compared)
            heapq.heappush(heap, (node.val, i, node))
    
    dummy = ListNode(0)
    current = dummy
    
    while heap:
        val, i, node = heapq.heappop(heap)
        
        current.next = node
        current = current.next
        
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    
    return dummy.next
```

**Complexity:** O(n log k) where n = total nodes, k = number of lists

**Space:** O(k) for heap

---

## Pattern 4: Running Median

### Find Median from Data Stream (LC 295) ⭐⭐⭐⭐⭐

**Two Heap Approach:**
```python
class MedianFinder:
    def __init__(self):
        # Max heap for smaller half (negate values)
        self.small = []
        # Min heap for larger half
        self.large = []
    
    def addNum(self, num: int) -> None:
        # Add to small (max heap)
        heapq.heappush(self.small, -num)
        
        # Balance: largest in small <= smallest in large
        if (self.small and self.large and
            -self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        
        # Keep sizes balanced (small can have 1 more)
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        elif len(self.large) > len(self.small):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)
    
    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return -self.small[0]
        
        return (-self.small[0] + self.large[0]) / 2
```

**Complexity:** O(log n) per add, O(1) per median query

---

## Pattern 5: Meeting Rooms / Timeline Problems

### Meeting Rooms II (LC 253) ⭐⭐⭐⭐⭐

**Heap Approach:**
```python
def minMeetingRooms(intervals: List[List[int]]) -> int:
    if not intervals:
        return 0
    
    # Sort by start time
    intervals.sort(key=lambda x: x[0])
    
    # Min heap to track end times of ongoing meetings
    rooms = []
    heapq.heappush(rooms, intervals[0][1])
    
    for i in range(1, len(intervals)):
        # If earliest meeting ended, reuse room
        if rooms[0] <= intervals[i][0]:
            heapq.heappop(rooms)
        
        # Add current meeting's end time
        heapq.heappush(rooms, intervals[i][1])
    
    return len(rooms)
```

**Complexity:** O(n log n) time, O(n) space

---

## Pattern 6: Distant Barcodes / Reorganization

### Reorganize String (LC 767) ⭐⭐⭐⭐

```python
def reorganizeString(s: str) -> str:
    from collections import Counter
    
    count = Counter(s)
    
    # Max heap by frequency
    max_heap = [(-freq, char) for char, freq in count.items()]
    heapq.heapify(max_heap)
    
    result = []
    prev_freq, prev_char = 0, ''
    
    while max_heap:
        freq, char = heapq.heappop(max_heap)
        result.append(char)
        
        # Add previous back if still has count
        if prev_freq < 0:
            heapq.heappush(max_heap, (prev_freq, prev_char))
        
        # Update previous
        prev_freq, prev_char = freq + 1, char
    
    result_str = ''.join(result)
    
    # Check if valid (length should match)
    return result_str if len(result_str) == len(s) else ""
```

**Complexity:** O(n log k) where k = unique characters

---

## Advanced Patterns

### Smallest Range Covering K Lists (LC 632)

```python
def smallestRange(nums: List[List[int]]) -> List[int]:
    # Heap: (value, list_index, element_index)
    heap = [(row[0], i, 0) for i, row in enumerate(nums)]
    heapq.heapify(heap)
    
    # Track current maximum
    curr_max = max(row[0] for row in nums)
    best_range = [float('-inf'), float('inf')]
    
    while heap:
        curr_min, list_idx, elem_idx = heapq.heappop(heap)
        
        # Update best range
        if curr_max - curr_min < best_range[1] - best_range[0]:
            best_range = [curr_min, curr_max]
        
        # Move to next element in this list
        if elem_idx + 1 < len(nums[list_idx]):
            next_val = nums[list_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))
            curr_max = max(curr_max, next_val)
        else:
            break  # Can't move forward
    
    return best_range
```

---

## Google Interview Tips

1. **Always clarify:** Min or max heap? K largest or smallest?

2. **Consider multiple approaches:**
   - Heap: O(n log k)
   - QuickSelect: O(n) average
   - Bucket sort: O(n) if range is small

3. **Watch for edge cases:**
   - Empty input
   - K = 1 or K = n
   - Duplicate elements

4. **Space optimization:**
   - Use heap of size k instead of size n

---

## Master Checklist

- [ ] Understand heap property and operations
- [ ] Implement max heap using negation
- [ ] Solve k-th element problems
- [ ] Master two-heap running median
- [ ] Handle k-way merge scenarios
- [ ] Reorganize/reorder with heap

---

## Practice Problems (Priority Order)

1. LC 215 - Kth Largest Element ⭐⭐⭐⭐⭐
2. LC 347 - Top K Frequent ⭐⭐⭐⭐⭐
3. LC 23 - Merge K Sorted Lists ⭐⭐⭐⭐⭐
4. LC 295 - Find Median ⭐⭐⭐⭐⭐
5. LC 253 - Meeting Rooms II ⭐⭐⭐⭐⭐
6. LC 767 - Reorganize String ⭐⭐⭐⭐
7. LC 973 - K Closest Points ⭐⭐⭐⭐
8. LC 1046 - Last Stone Weight ⭐⭐⭐
9. LC 632 - Smallest Range ⭐⭐⭐⭐
10. LC 239 - Sliding Window Maximum ⭐⭐⭐⭐

**Total Time:** 4-5 hours

---

## Common Mistakes

1. **Forgetting to heapify**
   ```python
   # ❌ Wrong
   heap = [3, 1, 4, 1, 5]
   smallest = heapq.heappop(heap)
   
   # ✅ Correct
   heap = [3, 1, 4, 1, 5]
   heapq.heapify(heap)
   smallest = heapq.heappop(heap)
   ```

2. **Confusing k largest vs k smallest**
   - K largest: Use min heap of size k
   - K smallest: Use max heap of size k

3. **Not using tuple comparison carefully**
   ```python
   # Python compares tuples element by element
   heapq.heappush(heap, (priority, data))
   ```

4. **Modifying heap directly**
   - Use heapq functions, don't modify list directly

---

**Time Complexity Reference:**

| Operation | Time |
|-----------|------|
| heapify | O(n) |
| heappush | O(log n) |
| heappop | O(log n) |
| peek (heap[0]) | O(1) |
| nsmallest(k) | O(n log k) |

**Master heaps, and you'll handle all Top-K problems with ease!**
