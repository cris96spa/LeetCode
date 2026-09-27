# Intervals

Intervals are everywhere: meetings on a calendar, jobs on a machine, reservations for a room, the lifetime of a process, the span of a gene on a chromosome. Interval problems look varied — merge these, schedule those, count how many overlap — but almost all of them are solved by the same two moves:

1. **Sort** the intervals by an endpoint (and choosing *which* endpoint is the real decision).
2. **Sweep** from left to right, maintaining a small amount of state.

This chapter is also the right place to confront one of the central lessons of algorithm design. Interval problems invite **greedy** algorithms, and greedy algorithms invite *plausible-looking wrong answers*. We will see several of those, learn how to break them with counterexamples, and learn how to prove the correct one right.

---

## Foundations

### Representation

An interval is a pair `[start, end]`. Before writing any code, decide whether endpoints are **inclusive** or not, because it changes the overlap test:

- **Closed** $[s, e]$: `[1, 3]` and `[3, 5]` share the point 3, so they overlap. (LC 56 uses this convention.)
- **Half-open** $[s, e)$: `[1, 3)` and `[3, 5)` don't overlap — a meeting ending at 3 doesn't conflict with one starting at 3. (Meeting rooms use this convention.)

Half-open intervals are usually the better model for time: the length is `e - s`, and adjacent intervals tile without overlapping.

### When do two intervals overlap?

The positive condition is easy to get wrong, so derive it from the negative. Two intervals are **disjoint** exactly when one ends before the other starts: $a_e \le b_s$ or $b_e \le a_s$ (half-open). Negating:

$$\text{overlap}(a, b) \iff a_s < b_e \ \text{ and } \ b_s < a_e$$

For closed intervals, use $\le$ in both places. The overlapping region, when it exists, is $[\max(a_s, b_s),\ \min(a_e, b_e)]$.

### Only three ways for two intervals to meet

Up to symmetry, two intervals are either **disjoint**, **partially overlapping**, or **nested** (one contains the other). That short list is useful when testing an idea: any claim about pairs of intervals can be checked against all three cases, and any counterexample to an interval algorithm can be built by adding a third interval to one of these three pictures.

### Which endpoint to sort by?

| Goal | Sort by | Why |
|---|---|---|
| Merge overlapping intervals, compute a union | **start** | Anything that could merge with the current block starts before it ends |
| Select the most non-overlapping intervals | **end** | Finishing early leaves the most room for the rest |
| Count simultaneous overlaps | **both endpoints as events** | Only the moments where something starts or ends matter |

---

## Merging Intervals (LC 56)

Sort by start. Walk through the intervals, maintaining the current merged block. An interval either overlaps the block (extend it) or starts after it ends (the block is finished; start a new one).

```python
def merge(intervals: list[list[int]]) -> list[list[int]]:
    intervals.sort(key=lambda iv: iv[0])
    merged: list[list[int]] = []
    for start, end in intervals:
        if merged and start <= merged[-1][1]:            # overlaps the current block
            merged[-1][1] = max(merged[-1][1], end)      # nested intervals: keep the larger end
        else:
            merged.append([start, end])
    return merged
```

**Why is sorting by start enough?** Invariant: `merged` holds disjoint blocks covering exactly the intervals seen so far, and nothing unseen starts before the last block's start. If the next interval starts after the last block ends, then *every* later interval starts even later — none of them can reach back to touch the finished block. So only the last block ever needs checking.

The `max` handles the **nested** case: `[1, 10]` followed by `[2, 3]` must not shrink the block to end at 3.

**Time:** $O(n \log n)$ for the sort; the sweep is $O(n)$.

### Insert into a sorted list (LC 57)

When the intervals are already sorted and disjoint, inserting a new one needs no sort. Three phases in one pass: copy the intervals that end before the new one starts, absorb every interval that overlaps it, copy the rest.

```python
def insert(intervals: list[list[int]], new: list[int]) -> list[list[int]]:
    result = []
    i, n = 0, len(intervals)
    start, end = new
    while i < n and intervals[i][1] < start:          # entirely before
        result.append(intervals[i])
        i += 1
    while i < n and intervals[i][0] <= end:           # overlaps: absorb
        start = min(start, intervals[i][0])
        end = max(end, intervals[i][1])
        i += 1
    result.append([start, end])
    result.extend(intervals[i:])                      # entirely after
    return result
```

$O(n)$. (Binary search could locate the overlap region in $O(\log n)$, but building the output list is $O(n)$ anyway.)

### Intersecting two interval lists (LC 986)

Given two sorted lists of disjoint intervals, report all pairwise intersections. Two pointers, one per list: the intersection of the current pair is `[max(starts), min(ends)]` if non-empty. Then advance whichever interval **ends first** — it can't intersect anything further in the other list.

```python
def interval_intersection(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    i = j = 0
    result = []
    while i < len(a) and j < len(b):
        lo = max(a[i][0], b[j][0])
        hi = min(a[i][1], b[j][1])
        if lo <= hi:
            result.append([lo, hi])
        if a[i][1] < b[j][1]:
            i += 1
        else:
            j += 1
    return result
```

---

## Interval Scheduling: The Movie Star Problem

Here is a problem worth thinking about slowly.

> You are a movie star with offers for $n$ film projects. Each project occupies a fixed interval of days, and you can't be on two sets at once. Every film pays the same. Which projects should you accept to star in **as many films as possible**?

In other words: given $n$ intervals, find the largest subset of mutually non-overlapping ones. Before reading on, try to find an algorithm.

### Three plausible ideas, three failures

**Idea 1: earliest start first.** Take the job that starts first, discard everything that conflicts with it, repeat. After all, no other job can use those early days.

It fails when the earliest job is very long. One epic that starts first and runs all year blocks every other offer:

```text
[====================== epic ======================]
  [a]   [b]   [c]   [d]   [e]
earliest-start picks 1 film; the optimum is 5
```

**Idea 2: shortest job first.** The problem with the epic was its length, so prefer short jobs.

It fails when a short job straddles two longer ones:

```text
[=== x ===]   [=== y ===]
        [ s ]
shortest-first picks s (1 film); the optimum is x and y (2 films)
```

The loss here is at most half the optimum — but "at most half as good" is still wrong.

**Idea 3: fewest conflicts first.** Take the interval that overlaps the fewest others; surely that sacrifices the least. This one is harder to break, which is exactly why it's dangerous.

??? question "Stop and Think: Break the fewest-conflicts heuristic"
    **Problem:** Find an instance where repeatedly choosing the interval with the fewest overlaps gives a suboptimal answer.

    **Solution:** Start from four disjoint intervals in a row — the optimal answer, $T_1 \dots T_4$. Add a short interval $M$ that bridges $T_2$ and $T_3$; it conflicts with just those two. Now make $T_2$ and $T_3$ look *worse* than $M$ by piling three identical intervals across the $T_1$/$T_2$ boundary and three across the $T_3$/$T_4$ boundary:

    ```text
    T1 [0,2]   T2 [3,5]   T3 [6,8]   T4 [9,11]
            3 x [1.5,3.5]      3 x [7.5,9.5]
                    M [4.5,6.5]
    ```

    Conflict counts: $M$ has 2, $T_1$ and $T_4$ have 3, $T_2$ and $T_3$ have 4, each stacked interval has 4. The heuristic grabs $M$, which eliminates $T_2$ and $T_3$, and can then get at most one interval from each side: 3 films. The optimum, $T_1 \dots T_4$, is 4.

    Notice the recipe: find the weakness ("a low-conflict interval can still block good ones"), then use **ties and piles of identical items** to steer the heuristic into it.

!!! tip "Take-Home Lesson"
    Reasonable-looking algorithms are easily wrong. Correctness must be demonstrated, not assumed — and the fastest way to demolish a wrong idea is a **small counterexample**. Think small (two or three intervals), think exhaustively (try all three pairwise configurations), seek extremes (very long vs. very short), and go for ties.

### The algorithm that works: earliest finish first

Consider the interval $x$ that **ends first**. Every other interval that conflicts with $x$ must still be running just before $x$ ends (it can't end earlier, by the choice of $x$), so all of them overlap each other at that moment — at most one of them can be in *any* solution. And among them, $x$ is the one that frees up the timeline earliest. So choosing $x$ can never hurt.

```python
def max_non_overlapping(intervals: list[list[int]]) -> int:
    """Largest number of pairwise non-overlapping half-open intervals."""
    count = 0
    last_end = float("-inf")
    for start, end in sorted(intervals, key=lambda iv: iv[1]):
        if start >= last_end:              # compatible with everything chosen
            count += 1
            last_end = end
    return count
```

**Proof by exchange.** Let $G = g_1, g_2, \ldots$ be the greedy picks and $O = o_1, o_2, \ldots$ any optimal solution, both sorted by end time. Greedy picked $g_1$ as the earliest-ending interval of all, so $\text{end}(g_1) \le \text{end}(o_1)$. Replace $o_1$ with $g_1$ in $O$: it still doesn't conflict with $o_2$, since $g_1$ ends no later than $o_1$ did. Repeating the argument, greedy "stays ahead" at every step — its $k$-th pick ends no later than the optimum's $k$-th — so if the optimum had a $(k+1)$-th interval, it would also have been available to greedy. Hence $|G| \ge |O|$.

**Time:** $O(n \log n)$.

This exchange argument is *the* template for proving greedy algorithms correct: show that the greedy choice can be swapped into any optimal solution without making it worse. See [Greedy](14_greedy.md) for more.

### Problems that are secretly interval scheduling

| Problem | Reduction |
|---|---|
| Non-overlapping Intervals (LC 435): fewest removals to eliminate overlaps | `n - max_non_overlapping(intervals)` |
| Minimum Arrows to Burst Balloons (LC 452) | Same greedy (closed intervals, so compare with `>`). Each chosen interval's end is where an arrow goes; the number of disjoint intervals equals the number of arrows needed |
| Maximum Length of Pair Chain (LC 646) | Exactly interval scheduling |

The arrows problem is a nice duality: the maximum number of pairwise-disjoint intervals equals the minimum number of points that **stab** every interval. Greedy finds both at once.

---

## Partitioning: How Many Rooms? (LC 253)

Now keep *all* the intervals, and ask for the minimum number of rooms (machines, colors) so that no two overlapping meetings share a room.

**Lower bound:** if some moment has $d$ meetings in progress, you need at least $d$ rooms. Call the maximum such $d$ over all moments the **depth**.

**Upper bound:** the depth is always enough. Process meetings by start time, and reuse any room whose meeting has ended. A new room is opened only when all current rooms are busy — that is, at a moment when that many meetings overlap. So the number of rooms never exceeds the depth.

So the answer is simply **the maximum number of simultaneous intervals**, which a sweep over endpoints computes directly:

```python
def min_meeting_rooms(intervals: list[list[int]]) -> int:
    events = []
    for start, end in intervals:
        events.append((start, 1))      # a meeting begins
        events.append((end, -1))       # a meeting ends
    events.sort()                      # at equal times, -1 sorts before +1
    rooms = best = 0
    for _, delta in events:
        rooms += delta
        best = max(best, rooms)
    return best
```

The tuple sort puts an end event `(t, -1)` before a start event `(t, 1)` at the same time — exactly right for half-open intervals, where a room freed at time $t$ can be reused at time $t$. For closed intervals, you'd want the opposite order.

If you need to know **which** room each meeting gets, simulate the greedy assignment with a min-heap of end times:

```python
import heapq


def min_meeting_rooms_heap(intervals: list[list[int]]) -> int:
    ends: list[int] = []                         # end times of rooms in use
    for start, end in sorted(intervals):
        if ends and ends[0] <= start:
            heapq.heapreplace(ends, end)         # reuse the room that frees up first
        else:
            heapq.heappush(ends, end)            # open a new room
    return len(ends)
```

!!! tip "Take-Home Lesson"
    For many optimization problems, the smartest first step is to find a simple **lower bound** on the answer, then look for an algorithm that meets it. When a greedy algorithm matches the lower bound, it's optimal — no exchange argument needed.

---

## The Sweep Line

The events technique generalizes: turn each interval into a "+1 at start, −1 at end" pair of events, sort the events, and sweep while maintaining a running state. It answers questions like:

- Maximum overlap, and *when* it occurs.
- Total length covered by the union of intervals (add up the stretches where the count is positive).
- Whether any point is covered by more than $k$ intervals (LC 731, 732).
- The skyline of a set of buildings (LC 218), with a max-heap of active heights as the state.

### Difference arrays: sweep lines on integer grids

When coordinates are small integers, skip the sort: record `+x` at the start and `-x` just past the end in an array, then take a prefix sum. Each prefix sum value is the total active at that position.

```python
def car_pooling(trips: list[list[int]], capacity: int) -> bool:
    """LC 1094: trips[i] = [passengers, from, to]; can one car carry them all?"""
    delta = [0] * 1001
    for passengers, start, end in trips:
        delta[start] += passengers
        delta[end] -= passengers           # they get off at `end`
    load = 0
    for change in delta:
        load += change
        if load > capacity:
            return False
    return True
```

$O(n + C)$ for coordinate range $C$ — a counting-sort version of the sweep. Corporate Flight Bookings (LC 1109) is the same trick.

---

## When Greedy Fails: Weighted Scheduling

Change the movie problem slightly: each film now pays a **different** fee, and you want to maximize total earnings (LC 1235, Maximum Profit in Job Scheduling). Earliest-finish-first breaks immediately — it would happily take a 1-dollar job that blocks a million-dollar one.

The fix is **dynamic programming** over the jobs sorted by end time. For job $i$, either skip it, or take it and add the best total over jobs that end by the time $i$ starts. That "latest compatible job" is found by binary search.

```python
import bisect


def job_scheduling(start: list[int], end: list[int], profit: list[int]) -> int:
    jobs = sorted(zip(end, start, profit))
    ends = [e for e, _, _ in jobs]
    best = [0] * (len(jobs) + 1)          # best[i] = max profit using the first i jobs
    for i, (e, s, p) in enumerate(jobs):
        k = bisect.bisect_right(ends, s, 0, i)    # jobs[:k] all end by time s
        best[i + 1] = max(best[i], best[k] + p)
    return best[-1]
```

**Time:** $O(n \log n)$. The pattern — sort, then DP where each item looks back to its last compatible predecessor — recurs throughout scheduling problems. See [Dynamic Programming](15_dynamic_programming.md).

!!! note "Narrowing the problem"
    Scheduling is extremely sensitive to the exact problem statement. Unweighted intervals: greedy, $O(n \log n)$. Weighted intervals: DP, $O(n \log n)$. But allow each job to occupy *several* disjoint intervals (a film that shoots in March and again in June), and the problem becomes NP-complete — no efficient algorithm is known at all. When a problem seems hard, check whether the instances you actually need to handle belong to a simpler special case. Restricting the input until an efficient algorithm exists is a legitimate and powerful design technique.

---

## Common Mistakes

1. **Closed vs. half-open confusion.** `start <= prev_end` merges `[1, 3]` and `[3, 5]`; `start < prev_end` doesn't. Decide which the problem intends before writing the comparison — including in event sorting.

2. **Forgetting nested intervals when merging.** `merged[-1][1] = end` instead of `max(merged[-1][1], end)` shrinks a block when a short interval sits inside a long one.

3. **Sorting by the wrong endpoint.** Merging wants start order; selecting the most disjoint intervals wants end order. Earliest-*start*-first selection is a classic wrong answer.

4. **Wrong tie-breaking in sweeps.** Whether an end and a start at the same instant overlap is decided by event order. Encode it deliberately.

5. **Trusting a greedy rule without proof.** Before coding a greedy interval algorithm, spend a minute hunting for a counterexample with two or three intervals. If you can't find one, try to sketch the exchange argument.

6. **Mutating the input.** `intervals.sort()` and editing `merged[-1]` in place modify lists the caller may still use. Copy if that matters.

---

## Practice Problems

| Problem | Technique |
|---|---|
| Merge Intervals (LC 56) | Sort by start, extend block |
| Insert Interval (LC 57) | Three-phase linear scan |
| Interval List Intersections (LC 986) | Two pointers, advance the earlier end |
| Meeting Rooms (LC 252) | Sort, check adjacent pairs |
| Meeting Rooms II (LC 253) | Sweep line or heap of end times |
| Non-overlapping Intervals (LC 435) | Earliest finish first |
| Minimum Number of Arrows (LC 452) | Earliest finish first (stabbing) |
| Maximum Length of Pair Chain (LC 646) | Earliest finish first |
| Remove Covered Intervals (LC 1288) | Sort by start asc, end desc |
| Car Pooling (LC 1094) | Difference array |
| My Calendar II (LC 731) | Sweep / overlap counting |
| Employee Free Time (LC 759) | Merge, then report gaps |
| The Skyline Problem (LC 218) | Sweep line + max-heap |
| Maximum Profit in Job Scheduling (LC 1235) | Sort by end + DP + binary search |
