# Intervals - Complete Guide

**Interview Frequency:** ⭐⭐⭐⭐ (50% of FAANG interviews)
**Google Frequency:** ⭐⭐⭐⭐ (Highly favored in Google phone screens)

## Why Intervals Matter at Google

Interval problems test multiple skills simultaneously:
- **Sorting intuition** - recognizing when to sort saves complexity
- **Greedy thinking** - local optimal choices leading to global optimum
- **Edge case handling** - boundary conditions are critical
- **Time/space tradeoffs** - often multiple valid approaches

Google loves intervals because they mirror real-world scheduling, resource allocation, and timeline management problems.

---

## **Key Concepts**

### **1. What is an Interval?**

An interval is a range represented as `[start, end]` where:

- `start`: The beginning of the interval (inclusive)
- `end`: The endpoint of the interval (can be inclusive or exclusive - **always clarify in interview**)

**Critical Clarifications to Ask:**
- Are endpoints inclusive? `[1, 3]` vs `[1, 3)`
- Can intervals be empty? `[3, 3]`
- Can `start > end`? (Usually no)
- Are intervals sorted? (Changes approach dramatically)

### **2. Types of Interval Problems**

- **Merging intervals**: Combine overlapping intervals into a single interval
- **Inserting intervals**: Add a new interval and merge if necessary
- **Checking overlap**: Determine if two intervals overlap
- **Interval intersections**: Find common ranges between two sets of intervals
- **Removing intervals**: Remove specific intervals or ranges
- **Scheduling problems**: Meeting rooms, minimum resources needed
- **Timeline sweeping**: Events happening at points in time

---

## **Core Techniques**

### **1. Sorting Strategies**

**A. Sort by Start Time (Most Common)**
```python
intervals.sort(key=lambda x: x[0])
# Time: O(n log n), Space: O(1) if in-place
```
**When to use:** Merging, inserting, most general problems

**B. Sort by Start, Then by End (Descending)**
```python
intervals.sort(key=lambda x: (x[0], -x[1]))
```
**When to use:** Finding covered intervals (longer intervals first)

**C. Sort by End Time**
```python
intervals.sort(key=lambda x: x[1])
```
**When to use:** Interval scheduling (greedy selection)

**Why Sort?** 
- Reduces O(n²) comparison to O(n) after O(n log n) sort
- Enables greedy approaches
- Simplifies overlap detection

### **2. Overlap Conditions**

Two intervals `[a, b]` and `[c, d]` overlap if:
```python
max(a, c) <= min(b, d)
```

**Alternative formulation** (often clearer):
```python
a <= d and c <= b  # They DON'T overlap if: b < c or d < a
```

**Visual:**
```
Overlapping:     [a----b]
                    [c----d]

Non-overlapping: [a----b]  [c----d]
```

### **3. Merging Intervals**

**Algorithm:**
1. Sort intervals by start time - O(n log n)
2. Traverse intervals, comparing current with last merged - O(n)
3. If overlap: extend the last interval's end
4. If no overlap: add current interval to result

**Complexity:** O(n log n) time, O(n) space for result

---

## **Common Problems and Patterns**

### **1. Merge Intervals** (LC 56)

**Problem:** Given intervals, merge all overlapping ones.

**Approach:**
```python
def merge(intervals):
    if not intervals:
        return []
    
    # Sort by start time
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    
    for current in intervals[1:]:
        last = merged[-1]
        
        # Check overlap: current starts before last ends
        if current[0] <= last[1]:
            # Merge: extend last interval
            last[1] = max(last[1], current[1])
        else:
            # No overlap: add current
            merged.append(current)
    
    return merged
```

**Complexity:**
- Time: O(n log n) - dominated by sorting
- Space: O(n) - for result (can be O(1) if modifying input)

**Edge Cases:**
- Empty input: `[]`
- Single interval: `[[1,3]]`
- All overlapping: `[[1,4], [2,5], [3,6]]` → `[[1,6]]`
- None overlapping: `[[1,2], [3,4]]` → `[[1,2], [3,4]]`
- Duplicate intervals: `[[1,3], [1,3]]` → `[[1,3]]`

**Google Follow-up:** "What if intervals are streaming in real-time?"

### **2. Insert Interval** (LC 57)

**Problem:** Insert new interval into sorted, non-overlapping intervals.

**Key Insight:** Three distinct phases - before, merge, after

**Approach:**
```python
def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
    result = []
    i = 0
    n = len(intervals)
    
    # Phase 1: Add all intervals that come before newInterval (no overlap)
    while i < n and intervals[i][1] < newInterval[0]:
        result.append(intervals[i])
        i += 1
    
    # Phase 2: Merge all overlapping intervals with newInterval
    while i < n and intervals[i][0] <= newInterval[1]:
        newInterval[0] = min(newInterval[0], intervals[i][0])
        newInterval[1] = max(newInterval[1], intervals[i][1])
        i += 1
    result.append(newInterval)
    
    # Phase 3: Add all intervals that come after newInterval
    while i < n:
        result.append(intervals[i])
        i += 1
    
    return result
```

**Complexity:**
- Time: O(n) - single pass through array (intervals already sorted!)
- Space: O(n) - result array

**Why No Sorting?** Input is already sorted and non-overlapping.

**Edge Cases:**
- Insert at beginning: `intervals=[[2,5]], new=[1,3]`
- Insert at end: `intervals=[[1,2]], new=[4,6]`
- Merge all: `intervals=[[1,2],[3,4]], new=[1,5]`

### **3. Meeting Rooms** (LC 252)

**Problem:** Can person attend all meetings (no overlaps)?

**Approach:**
```python
def canAttendMeetings(intervals):
    intervals.sort(key=lambda x: x[0])
    
    for i in range(1, len(intervals)):
        # If current starts before previous ends
        if intervals[i][0] < intervals[i-1][1]:
            return False
    
    return True
```

**Complexity:** O(n log n) time, O(1) space

**Overlap Check Helper:**
```python
def isOverlap(interval1, interval2):
    # Two intervals overlap if:
    return max(interval1[0], interval2[0]) < min(interval1[1], interval2[1])
    # Note: Use < for exclusive, <= for inclusive endpoints
```

### **4. Interval Intersection**

- **Problem:** Find the intersection of two lists of intervals.
- **Approach:**
  ```python
  def intervalIntersection(firstList, secondList):
      i, j = 0, 0
      result = []
      while i < len(firstList) and j < len(secondList):
          start = max(firstList[i][0], secondList[j][0])
          end = min(firstList[i][1], secondList[j][1])
          if start <= end:
              result.append([start, end])
          if firstList[i][1] < secondList[j][1]:
              i += 1
          else:
              j += 1
      return result
  ```

### **5. Remove Covered Intervals**

- **Problem:** Remove intervals that are completely covered by another interval.
- **Approach:**
  ```python
  def removeCoveredIntervals(intervals):
      intervals.sort(key=lambda x: (x[0], -x[1]))
      count = 0
      prev_end = 0
      for _, end in intervals:
          if end > prev_end:
              count += 1
              prev_end = end
      return count
  ```

### **6. Meeting Rooms II** (LC 253) - **Google Favorite**

**Problem:** Minimum conference rooms needed.

**Approach 1: Min Heap (Optimal)**
```python
import heapq

def minMeetingRooms(intervals):
    if not intervals:
        return 0
    
    # Sort by start time
    intervals.sort(key=lambda x: x[0])
    
    # Min heap to track end times of ongoing meetings
    rooms = []
    
    for interval in intervals:
        # If earliest ending meeting finished, reuse room
        if rooms and rooms[0] <= interval[0]:
            heapq.heappop(rooms)
        
        # Add current meeting's end time
        heapq.heappush(rooms, interval[1])
    
    return len(rooms)
```

**Complexity:** O(n log n) time, O(n) space

**Approach 2: Timeline/Sweep (Space Optimized)**
```python
def minMeetingRooms(intervals):
    starts = sorted([i[0] for i in intervals])
    ends = sorted([i[1] for i in intervals])
    
    rooms = max_rooms = 0
    s = e = 0
    
    while s < len(starts):
        if starts[s] < ends[e]:
            rooms += 1  # Meeting starting
            max_rooms = max(max_rooms, rooms)
            s += 1
        else:
            rooms -= 1  # Meeting ending
            e += 1
    
    return max_rooms
```

**Complexity:** O(n log n) time, O(n) space

**Google Follow-up:** "How would you handle recurring meetings?"

---

## **Advanced Patterns**

### **7. Non-overlapping Intervals** (LC 435)

**Problem:** Minimum removals to make intervals non-overlapping.

**Key Insight:** Greedy - keep intervals with earliest end time.

```python
def eraseOverlapIntervals(intervals):
    if not intervals:
        return 0
    
    # Sort by END time (greedy choice)
    intervals.sort(key=lambda x: x[1])
    
    removals = 0
    prev_end = intervals[0][1]
    
    for i in range(1, len(intervals)):
        if intervals[i][0] < prev_end:  # Overlap
            removals += 1
        else:
            prev_end = intervals[i][1]
    
    return removals
```

**Complexity:** O(n log n) time, O(1) space

### **8. Interval List Intersections** (LC 986)

**Problem:** Find intersections of two sorted interval lists.

**Two Pointer Approach:**
```python
def intervalIntersection(A, B):
    i = j = 0
    result = []
    
    while i < len(A) and j < len(B):
        # Find intersection
        start = max(A[i][0], B[j][0])
        end = min(A[i][1], B[j][1])
        
        if start <= end:  # Valid intersection
            result.append([start, end])
        
        # Move pointer for interval that ends first
        if A[i][1] < B[j][1]:
            i += 1
        else:
            j += 1
    
    return result
```

**Complexity:** O(m + n) time, O(1) space (excluding result)

---

## **Master Checklist**

- [ ] Can identify when to sort by start vs end time
- [ ] Know overlap condition by heart
- [ ] Can implement merge intervals in <10 minutes
- [ ] Understand heap approach for meeting rooms
- [ ] Can explain greedy choice for scheduling problems
- [ ] Comfortable with two-pointer technique
- [ ] Can handle edge cases without prompting

---

## **Key Tips for Interval Problems**

### **1. Sorting Strategy**
- Default: sort by start time
- Greedy scheduling: sort by end time
- Covered intervals: sort by start, then end descending

### **2. Common Patterns Recognition**
- "Merge" → Sort by start, track end
- "Minimum resources" → Heap or timeline sweep
- "Remove minimum" → Greedy by end time
- "Find intersections" → Two pointers

### **3. Implementation Tips**
- Always clarify: inclusive vs exclusive endpoints
- Use `max(start1, start2)` and `min(end1, end2)` for overlap
- Consider: can you modify input? (saves space)
- Edge case: empty input, single interval

### **4. Google Interview Specifics**
- Be ready to optimize space (in-place modifications)
- Explain tradeoffs: heap vs timeline sweep
- Discuss streaming data scenarios
- Consider follow-ups: recurring events, priority levels

### **5. Testing Strategy**
```python
# Test with these patterns:
test_cases = [
    [],                           # Empty
    [[1,3]],                      # Single
    [[1,3],[2,4]],               # Overlap
    [[1,2],[3,4]],               # No overlap
    [[1,4],[1,4]],               # Duplicate
    [[1,4],[2,3]],               # Contained
    [[1,2],[2,3]],               # Touch at boundary
]
```

### **6. Time Complexity Quick Reference**
| Operation | Time | Why |
|-----------|------|-----|
| Merge | O(n log n) | Sorting dominates |
| Insert (sorted) | O(n) | No sort needed |
| Min rooms (heap) | O(n log n) | n insertions/deletions |
| Intersections | O(m + n) | Two pointers |

---

## **Interview Template**

```python
def solve_interval_problem(intervals):
    # Step 1: Handle edge cases
    if not intervals:
        return []
    
    # Step 2: Sort (by start usually)
    intervals.sort(key=lambda x: x[0])
    
    # Step 3: Initialize result
    result = [intervals[0]]  # or other structure
    
    # Step 4: Iterate and apply logic
    for i in range(1, len(intervals)):
        current = intervals[i]
        last = result[-1]
        
        # Check relationship (overlap, contain, etc.)
        if condition:
            # Merge/update
            pass
        else:
            # Add separately
            result.append(current)
    
    return result
```

**Practice Problems (Priority Order):**
1. LC 56 - Merge Intervals ⭐⭐⭐⭐⭐
2. LC 57 - Insert Interval ⭐⭐⭐⭐⭐
3. LC 253 - Meeting Rooms II ⭐⭐⭐⭐⭐ (Google favorite)
4. LC 435 - Non-overlapping Intervals ⭐⭐⭐⭐
5. LC 986 - Interval List Intersections ⭐⭐⭐⭐
6. LC 252 - Meeting Rooms ⭐⭐⭐
7. LC 1272 - Remove Interval ⭐⭐⭐

**Time Investment:** 4-5 hours to master all patterns

---

*Master these patterns and you'll handle any interval problem Google throws at you.*
5. **Optimize for Large Inputs:** Use efficient data structures like heaps or binary search trees for advanced problems.
