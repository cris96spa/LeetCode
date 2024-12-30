## **Key Concepts**

### **1. What is an Interval?**

An interval is a range represented as `[start, end]` where:

- `start`: The beginning of the interval.
- `end`: The endpoint of the interval.

### **2. Types of Interval Problems**

- **Merging intervals**: Combine overlapping intervals into a single interval.
- **Inserting intervals**: Add a new interval and merge if necessary.
- **Checking overlap**: Determine if two intervals overlap.
- **Interval intersections**: Find common ranges between two sets of intervals.
- **Removing intervals**: Remove specific intervals or ranges.

---

## **Core Techniques**

### **1. Sorting by Start Time**

- **Why?** Many interval problems benefit from sorting intervals by their `start` values to simplify merging and overlap detection.
- **How?**
  ```python
  intervals.sort(key=lambda x: x[0])
  ```

### **2. Overlap Conditions**

- Two intervals `[a, b]` and `[c, d]` overlap if:
  ```
  max(a, c) <= min(b, d)
  ```
  - This means the start of one interval is before the end of the other.

### **3. Merging Intervals**

- Merge intervals if they overlap.
- **Steps:**
  1. Sort intervals by start time.
  2. Traverse the intervals and check for overlap.
  3. Merge overlapping intervals.

---

## **Common Problems and Patterns**

### **1. Merge Intervals**

- **Problem:** Merge overlapping intervals.
- **Approach:**
  ```python
  def merge(intervals):
      intervals.sort(key=lambda x: x[0])
      merged = []
      for interval in intervals:
          if not merged or merged[-1][1] < interval[0]:
              merged.append(interval)
          else:
              merged[-1][1] = max(merged[-1][1], interval[1])
      return merged
  ```

### **2. Insert Interval**

- **Problem:** Insert a new interval and merge if necessary.
- **Approach:**

  ```python
  def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        results = []
        n, i = len(intervals), 0

        while i < n and intervals[i][1] < newInterval[0]:
            results.append(intervals[i])
            i+=1

        while i < n and intervals[i][0] <= newInterval[1]:
            newInterval = [
                min(newInterval[0], intervals[i][0]),
                max(newInterval[1], intervals[i][1])
            ]
            i+=1
        results.append(newInterval)

        while i < n:
            results.append(intervals[i])
            i+=1
        return results
  ```

### **3. Check for Overlap**

- **Problem:** Determine if two intervals overlap.
- **Approach:**
  ```python
  def isOverlap(interval1, interval2):
      return max(interval1[0], interval2[0]) <= min(interval1[1], interval2[1])
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

---

## **Key Tips for Interval Problems**

1. **Always Sort First:** Sorting intervals by their start times simplifies most problems.
2. **Draw Diagrams:** Visualize the intervals to understand the overlaps and gaps.
3. **Use Overlap Conditions:** Memorize the overlap formula `max(a, c) <= min(b, d)`.
4. **Test Edge Cases:** Consider scenarios with:
   - Single intervals.
   - Fully overlapping intervals.
   - Disjoint intervals.
   - Boundary conditions (e.g., empty lists, intervals at edges).
5. **Optimize for Large Inputs:** Use efficient data structures like heaps or binary search trees for advanced problems.
