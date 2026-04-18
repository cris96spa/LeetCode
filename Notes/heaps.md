# Heaps & Priority Queues

## Python heapq Module

Python only provides a **min heap**.

```python
import heapq

nums = [3, 1, 4, 1, 5, 9, 2, 6]
heapq.heapify(nums)            # O(n) - in-place

heapq.heappush(nums, 7)        # O(log n)
smallest = heapq.heappop(nums) # O(log n)
smallest = nums[0]             # O(1) - peek

# Push and pop in one operation
result = heapq.heappushpop(nums, 8)  # O(log n)
result = heapq.heapreplace(nums, 8)  # O(log n) - pop then push

# Get n smallest/largest
heapq.nsmallest(3, nums)  # O(n log k)
heapq.nlargest(3, nums)   # O(n log k)
```

| Operation | Time |
|-----------|------|
| heapify | O(n) |
| heappush | O(log n) |
| heappop | O(log n) |
| peek (heap[0]) | O(1) |
| nsmallest(k) | O(n log k) |

## Max Heap Trick

Negate values to simulate a max heap:

```python
max_heap = []
heapq.heappush(max_heap, -5)
heapq.heappush(max_heap, -3)
heapq.heappush(max_heap, -7)

max_val = -heapq.heappop(max_heap)  # 7
```

## Custom Objects in Heap

```python
# Tuples compared element by element
heap = []
heapq.heappush(heap, (priority, item))

# Dataclass with ordering
from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any = field(compare=False)
```

---

## Pattern 1: K-th Largest/Smallest Element (LC 215)

**Approach 1: Min heap of size k** -- keep k largest elements, root is k-th largest.

```python
def findKthLargest(nums: List[int], k: int) -> int:
    heap = []
    
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    
    return heap[0]
```

**Time:** O(n log k) | **Space:** O(k)

**Approach 2: Heapify** -- faster when k is close to n.

```python
def findKthLargest(nums: List[int], k: int) -> int:
    nums = [-num for num in nums]
    heapq.heapify(nums)
    
    for _ in range(k - 1):
        heapq.heappop(nums)
    
    return -heapq.heappop(nums)
```

**Time:** O(n + k log n) | **Space:** O(1) if mutating input

**Approach 3: QuickSelect** -- optimal average case.

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

**Time:** O(n) average, O(n^2) worst | **Space:** O(1)

---

## Pattern 2: Top K Frequent Elements (LC 347)

**Heap approach:**
```python
def topKFrequent(nums: List[int], k: int) -> List[int]:
    from collections import Counter
    
    count = Counter(nums)
    
    heap = []
    for num, freq in count.items():
        heapq.heappush(heap, (freq, num))
        if len(heap) > k:
            heapq.heappop(heap)
    
    return [num for freq, num in heap]
```

**Time:** O(n log k) | **Space:** O(n)

**Bucket sort approach (optimal):**
```python
def topKFrequent(nums: List[int], k: int) -> List[int]:
    from collections import Counter
    
    count = Counter(nums)
    
    buckets = [[] for _ in range(len(nums) + 1)]
    for num, freq in count.items():
        buckets[freq].append(num)
    
    result = []
    for i in range(len(buckets) - 1, 0, -1):
        result.extend(buckets[i])
        if len(result) >= k:
            return result[:k]
```

**Time:** O(n) | **Space:** O(n)

---

## Pattern 3: K Closest Points to Origin (LC 973)

Use a max heap of size k. If a new point is closer than the farthest in the heap, swap it in.

```python
def kClosest(points: List[List[int]], k: int) -> List[List[int]]:
    # Max heap of size k (negate distance)
    heap = []
    
    for x, y in points:
        dist = -(x * x + y * y)  # Negate for max heap
        
        if len(heap) < k:
            heapq.heappush(heap, (dist, x, y))
        elif dist > heap[0][0]:
            heapq.heapreplace(heap, (dist, x, y))
    
    return [[x, y] for _, x, y in heap]
```

**Time:** O(n log k) | **Space:** O(k)

---

## Pattern 4: K-Way Merge / Merge K Sorted Lists (LC 23)

```python
def mergeKLists(lists: List[ListNode]) -> ListNode:
    heap = []
    
    for i, node in enumerate(lists):
        if node:
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

**Time:** O(n log k) where n = total nodes, k = number of lists | **Space:** O(k)

The index `i` serves as a tiebreaker since ListNode objects are not comparable.

---

## Pattern 5: Running Median (LC 295)

Two heaps: max heap for the smaller half, min heap for the larger half.

```python
class MedianFinder:
    def __init__(self):
        self.small = []  # Max heap (negated)
        self.large = []  # Min heap
    
    def addNum(self, num: int) -> None:
        heapq.heappush(self.small, -num)
        
        # Ensure max of small <= min of large
        if (self.small and self.large and
            -self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        
        # Balance sizes (small can have 1 more)
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

**Time:** O(log n) per add, O(1) per findMedian | **Space:** O(n)

---

## Pattern 6: Reorganize / Rearrange (LC 767)

Place most frequent characters first, ensuring no two adjacent characters are the same.

```python
def reorganizeString(s: str) -> str:
    from collections import Counter
    
    count = Counter(s)
    
    max_heap = [(-freq, char) for char, freq in count.items()]
    heapq.heapify(max_heap)
    
    result = []
    prev_freq, prev_char = 0, ''
    
    while max_heap:
        freq, char = heapq.heappop(max_heap)
        result.append(char)
        
        if prev_freq < 0:
            heapq.heappush(max_heap, (prev_freq, prev_char))
        
        prev_freq, prev_char = freq + 1, char  # freq is negative
    
    result_str = ''.join(result)
    return result_str if len(result_str) == len(s) else ""
```

**Time:** O(n log k) where k = unique characters | **Space:** O(k)

---

## Pattern 7: Task Scheduler (LC 621)

Schedule tasks with cooldown period n between same tasks. Greedy: always pick the task with the highest remaining count.

```python
def leastInterval(tasks: List[str], n: int) -> int:
    from collections import Counter
    
    count = Counter(tasks)
    max_heap = [-freq for freq in count.values()]
    heapq.heapify(max_heap)
    
    time = 0
    cooldown = deque()  # (available_time, neg_count)
    
    while max_heap or cooldown:
        time += 1
        
        if max_heap:
            freq = heapq.heappop(max_heap) + 1  # Execute one (freq is negative)
            if freq < 0:
                cooldown.append((time + n, freq))
        
        if cooldown and cooldown[0][0] == time:
            heapq.heappush(max_heap, cooldown.popleft()[1])
    
    return time
```

**Time:** O(n * k) where k = unique tasks | **Space:** O(k)

For the heap-free formula approach: `result = max(len(tasks), (max_freq - 1) * (n + 1) + count_of_max_freq)`.

---

## Advanced

### Smallest Range Covering K Lists (LC 632)

```python
def smallestRange(nums: List[List[int]]) -> List[int]:
    heap = [(row[0], i, 0) for i, row in enumerate(nums)]
    heapq.heapify(heap)
    
    curr_max = max(row[0] for row in nums)
    best_range = [float('-inf'), float('inf')]
    
    while heap:
        curr_min, list_idx, elem_idx = heapq.heappop(heap)
        
        if curr_max - curr_min < best_range[1] - best_range[0]:
            best_range = [curr_min, curr_max]
        
        if elem_idx + 1 < len(nums[list_idx]):
            next_val = nums[list_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))
            curr_max = max(curr_max, next_val)
        else:
            break  # One list exhausted, can't cover all
    
    return best_range
```

**Time:** O(n log k) where n = total elements, k = number of lists | **Space:** O(k)

### Lazy Deletion Pattern

When you cannot efficiently update entries already in the heap (e.g., changing priorities), use lazy deletion: mark entries as invalid and skip them when popped.

```python
class LazyHeap:
    def __init__(self):
        self.heap = []
        self.deleted = set()
    
    def push(self, item):
        heapq.heappush(self.heap, item)
    
    def remove(self, item):
        self.deleted.add(item)
    
    def pop(self):
        while self.heap:
            item = heapq.heappop(self.heap)
            if item not in self.deleted:
                return item
            self.deleted.discard(item)
        return None
    
    def peek(self):
        while self.heap and self.heap[0] in self.deleted:
            self.deleted.discard(heapq.heappop(self.heap))
        return self.heap[0] if self.heap else None
```

This is useful for problems like Sliding Window Median where you need to remove arbitrary elements from a heap.

**Note:** For interval scheduling problems using heaps (e.g., Meeting Rooms II / LC 253), see [intervals.md](intervals.md).

---

## Complexity Reference

| Pattern | Time | Space |
|---------|------|-------|
| K-th element (heap of size k) | O(n log k) | O(k) |
| K-th element (quickselect) | O(n) avg | O(1) |
| Top K frequent (heap) | O(n log k) | O(n) |
| Top K frequent (bucket sort) | O(n) | O(n) |
| K-way merge | O(n log k) | O(k) |
| Running median | O(log n) per add | O(n) |
| Task scheduler | O(n) | O(k) |

## Common Mistakes

1. **Forgetting to heapify** -- pushing to an unsorted list and then popping gives wrong results. Always `heapify` first or build via `heappush`.

2. **Confusing k largest vs k smallest** -- K largest: use min heap of size k. K smallest: use max heap of size k.

3. **Tuple comparison issues** -- Python compares tuples element by element. If priorities tie and the second element is not comparable (e.g., ListNode), add a tiebreaker index.

4. **Modifying heap directly** -- never insert/remove from the list directly. Always use `heapq` functions.

5. **Using max heap without negation** -- Python has no built-in max heap. Always negate values.
