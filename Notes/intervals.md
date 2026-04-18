# Intervals

## Core Concepts

### Interval Representation

An interval is a range `[start, end]`. Always clarify in interviews:
- Inclusive vs exclusive endpoints (`[1, 3]` vs `[1, 3)`)
- Can intervals be empty? (`[3, 3]`)
- Is input already sorted?

### Overlap Condition

Two intervals `[a, b]` and `[c, d]` overlap if:
```python
max(a, c) <= min(b, d)
```

Equivalent: `a <= d and c <= b`. They do NOT overlap if `b < c or d < a`.

```
Overlapping:     [a----b]
                    [c----d]

Non-overlapping: [a----b]  [c----d]
```

### Sorting Strategies

| Strategy | Code | Use Case |
|----------|------|----------|
| By start time | `intervals.sort(key=lambda x: x[0])` | Merging, inserting, most problems |
| By end time | `intervals.sort(key=lambda x: x[1])` | Greedy scheduling (non-overlapping, arrows) |
| By start, then end descending | `intervals.sort(key=lambda x: (x[0], -x[1]))` | Covered intervals (longer first) |

Sorting reduces O(n^2) pairwise comparison to O(n) single pass after O(n log n) sort.

---

## Techniques

### Merge Intervals (LC 56)

Sort by start. Walk through, extending the last merged interval on overlap or appending on no overlap.

```python
def merge(intervals):
    if not intervals:
        return []

    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]

    for current in intervals[1:]:
        last = merged[-1]
        if current[0] <= last[1]:
            last[1] = max(last[1], current[1])
        else:
            merged.append(current)

    return merged
```

**Time:** O(n log n) -- **Space:** O(n)

**Edge cases:** empty input, single interval, all overlapping, none overlapping, duplicates.

---

### Insert Interval (LC 57)

Input is already sorted and non-overlapping. Three phases: before, merge, after.

```python
def insert(intervals, newInterval):
    result = []
    i = 0
    n = len(intervals)

    # Phase 1: intervals entirely before newInterval
    while i < n and intervals[i][1] < newInterval[0]:
        result.append(intervals[i])
        i += 1

    # Phase 2: merge overlapping intervals
    while i < n and intervals[i][0] <= newInterval[1]:
        newInterval[0] = min(newInterval[0], intervals[i][0])
        newInterval[1] = max(newInterval[1], intervals[i][1])
        i += 1
    result.append(newInterval)

    # Phase 3: intervals entirely after
    while i < n:
        result.append(intervals[i])
        i += 1

    return result
```

**Time:** O(n) (no sort needed) -- **Space:** O(n)

---

### Meeting Rooms (LC 252)

Can a person attend all meetings? Sort by start, check for any overlap with previous.

```python
def canAttendMeetings(intervals):
    intervals.sort(key=lambda x: x[0])

    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i-1][1]:
            return False

    return True
```

**Time:** O(n log n) -- **Space:** O(1)

---

### Meeting Rooms II (LC 253)

Minimum conference rooms needed.

**Approach 1: Min Heap**

Sort by start. Use a min-heap of end times to track ongoing meetings. If the earliest-ending meeting finishes before the current one starts, reuse that room.

```python
import heapq

def minMeetingRooms(intervals):
    if not intervals:
        return 0

    intervals.sort(key=lambda x: x[0])
    rooms = []

    for interval in intervals:
        if rooms and rooms[0] <= interval[0]:
            heapq.heappop(rooms)
        heapq.heappush(rooms, interval[1])

    return len(rooms)
```

**Time:** O(n log n) -- **Space:** O(n)

**Approach 2: Line Sweep**

Break each interval into two events: +1 at start, -1 at end. Sort events and sweep to find the maximum concurrent meetings.

```python
def minMeetingRooms(intervals):
    events = []
    for start, end in intervals:
        events.append((start, 1))   # meeting starts
        events.append((end, -1))    # meeting ends

    events.sort()  # ties broken by -1 before +1 (end before start)

    max_rooms = current = 0
    for _, delta in events:
        current += delta
        max_rooms = max(max_rooms, current)

    return max_rooms
```

**Time:** O(n log n) -- **Space:** O(n)

The line sweep approach generalizes well to "maximum overlap at any point" problems.

---

### Interval Intersections (LC 986)

Two sorted interval lists. Use two pointers; the interval that ends first advances.

```python
def intervalIntersection(A, B):
    i = j = 0
    result = []

    while i < len(A) and j < len(B):
        start = max(A[i][0], B[j][0])
        end = min(A[i][1], B[j][1])

        if start <= end:
            result.append([start, end])

        if A[i][1] < B[j][1]:
            i += 1
        else:
            j += 1

    return result
```

**Time:** O(m + n) -- **Space:** O(1) (excluding result)

---

### Non-overlapping Intervals (LC 435)

Minimum removals to make all intervals non-overlapping. Greedy: sort by end time, keep intervals with earliest end.

```python
def eraseOverlapIntervals(intervals):
    if not intervals:
        return 0

    intervals.sort(key=lambda x: x[1])

    removals = 0
    prev_end = intervals[0][1]

    for i in range(1, len(intervals)):
        if intervals[i][0] < prev_end:
            removals += 1
        else:
            prev_end = intervals[i][1]

    return removals
```

**Time:** O(n log n) -- **Space:** O(1)

---

### Remove Covered Intervals (LC 1288)

Sort by start ascending, then end descending. An interval is covered if its end is <= the running max end.

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

**Time:** O(n log n) -- **Space:** O(1)

---

### Minimum Arrows to Burst Balloons (LC 452)

Each balloon is an interval. An arrow at position x bursts all balloons where `start <= x <= end`. Find minimum arrows.

This is the complement of non-overlapping intervals: count the number of non-overlapping groups. Sort by end, greedily shoot at each group's earliest end point.

```python
def findMinArrowShots(points):
    if not points:
        return 0

    points.sort(key=lambda x: x[1])

    arrows = 1
    arrow_pos = points[0][1]

    for start, end in points[1:]:
        if start > arrow_pos:  # new group, need new arrow
            arrows += 1
            arrow_pos = end

    return arrows
```

**Time:** O(n log n) -- **Space:** O(1)

---

## Line Sweep Technique

General template for event-based interval processing. Useful for counting maximum overlap, resource usage over time, etc.

```python
def line_sweep(intervals):
    events = []
    for start, end in intervals:
        events.append((start, 1))
        events.append((end, -1))

    events.sort()

    max_val = current = 0
    for _, delta in events:
        current += delta
        max_val = max(max_val, current)

    return max_val
```

**Time:** O(n log n) -- **Space:** O(n)

**When to use:** any problem asking about the maximum (or minimum) number of overlapping intervals at any point in time.

---

## Complexity Reference Table

| Problem | Time | Space |
|---------|------|-------|
| Merge Intervals | O(n log n) | O(n) |
| Insert Interval (sorted input) | O(n) | O(n) |
| Meeting Rooms | O(n log n) | O(1) |
| Meeting Rooms II (heap) | O(n log n) | O(n) |
| Meeting Rooms II (line sweep) | O(n log n) | O(n) |
| Interval Intersections | O(m + n) | O(1) |
| Non-overlapping Intervals | O(n log n) | O(1) |
| Remove Covered Intervals | O(n log n) | O(1) |
| Min Arrows to Burst Balloons | O(n log n) | O(1) |

## Common Mistakes

1. **Sorting by wrong key.** Merging needs sort-by-start. Greedy scheduling (non-overlapping, arrows) needs sort-by-end.
2. **Using `<` vs `<=` for overlap.** `[1,2]` and `[2,3]` -- do they overlap? Depends on problem semantics. Meeting rooms: `<` (meetings `[1,2]` and `[2,3]` don't conflict). Merge intervals: `<=`.
3. **Forgetting to extend with `max`.** When merging, the new end is `max(last[1], current[1])`, not just `current[1]` -- the current interval could be contained within the last.
4. **Modifying input unintentionally.** `newInterval[0] = min(...)` mutates the input list. Be aware of whether the caller expects the input preserved.
5. **Off-by-one with line sweep event ordering.** When a meeting ends and another starts at the same time, the end event should process first. The tuple `(time, -1)` sorts before `(time, +1)` naturally.
