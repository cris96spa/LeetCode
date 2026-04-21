# Greedy Algorithms

## When Greedy Works

- The problem has **optimal substructure**: optimal solution contains optimal solutions to subproblems.
- **Greedy choice property**: making the locally optimal choice at each step leads to a globally optimal solution.
- Often involves sorting + picking the "best" available option at each step.
- Key question: "Can I prove that being greedy never makes things worse?"

## Greedy vs DP

| Aspect | Greedy | DP |
|--------|--------|----|
| Approach | Make best local choice, never revisit | Try all choices, combine subproblem results |
| When | Local optimal = global optimal | Need all possibilities or exact count |
| Typical complexity | O(n log n) from sorting | O(n^2) or O(n * W) |
| Proof needed | Yes (exchange argument) | Correctness follows from recurrence |

If you think greedy works but can't prove it, consider DP.

---

## Key Patterns

### Interval Scheduling

Sort by end time, greedily pick non-overlapping intervals. See `intervals.md` for full coverage of interval problems (merge, insert, non-overlapping count, meeting rooms).

### Jump Game (LC 55)

Can you reach the last index? Track the farthest reachable position.

O(n) time, O(1) space:
```python
def canJump(nums):
    farthest = 0
    for i in range(len(nums)):
        if i > farthest:
            return False
        farthest = max(farthest, i + nums[i])
    return True
```

### Jump Game II (LC 45)

Minimum jumps to reach the last index. BFS-like level expansion.

O(n) time, O(1) space:
```python
def jump(nums):
    jumps = 0
    curr_end = 0      # end of current jump range
    farthest = 0      # farthest we can reach
    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])
        if i == curr_end:
            jumps += 1
            curr_end = farthest
    return jumps
```

### Gas Station (LC 134)

Circular route with gas stations. Find the starting station index (or -1 if impossible).

O(n) time, O(1) space:
```python
def canCompleteCircuit(gas, cost):
    if sum(gas) < sum(cost):
        return -1
    
    start = 0
    tank = 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:
            start = i + 1
            tank = 0
    return start
```

**Key insight:** If total gas >= total cost, a solution always exists. If the running sum goes negative at station `i`, the start must be after `i` (because any start between the current start and `i` would also fail).

### Candy (LC 135)

Each child gets at least 1 candy. A child with a higher rating than a neighbor gets more candy than that neighbor.

O(n) time, O(n) space:
```python
def candy(ratings):
    n = len(ratings)
    candies = [1] * n
    
    # Left to right: if rating increases, give more than left neighbor
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            candies[i] = candies[i - 1] + 1
    
    # Right to left: if rating increases (looking right), give more than right neighbor
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            candies[i] = max(candies[i], candies[i + 1] + 1)
    
    return sum(candies)
```

### Task Scheduler (LC 621)

Given tasks and cooldown `n`, find minimum intervals needed.

O(n) time, O(1) space (26 letters):
```python
def leastInterval(tasks, n):
    from collections import Counter
    counts = Counter(tasks)
    max_freq = max(counts.values())
    num_max = sum(1 for v in counts.values() if v == max_freq)
    
    # (max_freq - 1) full groups of (n + 1) slots, plus num_max tasks in last group
    result = (max_freq - 1) * (n + 1) + num_max
    return max(result, len(tasks))
```

**Key insight:** The most frequent task forces `(max_freq - 1)` gaps of size `n`. Other tasks fill in the gaps. If there are enough tasks to fill all gaps, the answer is just `len(tasks)`.

### Partition Labels (LC 763)

Partition string so each letter appears in at most one part. Maximize number of parts.

O(n) time, O(1) space (26 letters):
```python
def partitionLabels(s):
    last = {c: i for i, c in enumerate(s)}
    result = []
    start = end = 0
    for i, c in enumerate(s):
        end = max(end, last[c])
        if i == end:
            result.append(end - start + 1)
            start = i + 1
    return result
```

### Best Time to Buy and Sell Stock II (LC 122)

Unlimited transactions allowed. Collect every upswing.

O(n) time, O(1) space:
```python
def maxProfit(prices):
    profit = 0
    for i in range(1, len(prices)):
        if prices[i] > prices[i - 1]:
            profit += prices[i] - prices[i - 1]
    return profit
```

### Assign Cookies (LC 455)

Greedily assign smallest sufficient cookie to each child (sorted).

O(n log n + m log m) time, O(1) space (ignoring sort):
```python
def findContentChildren(g, s):
    g.sort()
    s.sort()
    child = cookie = 0
    while child < len(g) and cookie < len(s):
        if s[cookie] >= g[child]:
            child += 1
        cookie += 1
    return child
```

### Maximum Subarray (LC 53) - Kadane's Algorithm

O(n) time, O(1) space:
```python
def maxSubArray(nums):
    max_sum = curr_sum = nums[0]
    for num in nums[1:]:
        curr_sum = max(num, curr_sum + num)
        max_sum = max(max_sum, curr_sum)
    return max_sum
```

**Greedy insight:** if the running sum goes negative, it can only hurt future sums, so reset. See also `dynamic_programming.md` for the DP perspective.

### Reorganize String (LC 767)

Rearrange so no two adjacent chars are the same (or return "" if impossible).

O(n log n) time, O(n) space:
```python
def reorganizeString(s):
    from collections import Counter
    import heapq
    
    counts = Counter(s)
    max_count = max(counts.values())
    if max_count > (len(s) + 1) // 2:
        return ""
    
    # Max heap (negate for Python's min heap)
    heap = [(-cnt, ch) for ch, cnt in counts.items()]
    heapq.heapify(heap)
    
    result = []
    while len(heap) >= 2:
        cnt1, ch1 = heapq.heappop(heap)
        cnt2, ch2 = heapq.heappop(heap)
        result.append(ch1)
        result.append(ch2)
        if cnt1 + 1 < 0:
            heapq.heappush(heap, (cnt1 + 1, ch1))
        if cnt2 + 1 < 0:
            heapq.heappush(heap, (cnt2 + 1, ch2))
    
    if heap:
        result.append(heap[0][1])
    
    return "".join(result)
```

See `heaps.md` for more heap-based patterns.

### Boats to Save People (LC 881)

Each boat holds at most 2 people and has weight limit. Minimize boats.

O(n log n) time, O(1) space:
```python
def numRescueBoats(people, limit):
    people.sort()
    lo, hi = 0, len(people) - 1
    boats = 0
    while lo <= hi:
        if people[lo] + people[hi] <= limit:
            lo += 1
        hi -= 1
        boats += 1
    return boats
```

**Greedy insight:** pair the heaviest with the lightest. If they don't fit together, the heaviest rides alone.

### Minimum Number of Platforms / Meeting Rooms II Pattern

Sort start and end times separately. Sweep through events.

O(n log n) time, O(n) space:
```python
def minMeetingRooms(intervals):
    starts = sorted(i[0] for i in intervals)
    ends = sorted(i[1] for i in intervals)
    rooms = max_rooms = 0
    s = e = 0
    while s < len(starts):
        if starts[s] < ends[e]:
            rooms += 1
            max_rooms = max(max_rooms, rooms)
            s += 1
        else:
            rooms -= 1
            e += 1
    return max_rooms
```

See also: `intervals.md`.

---

## How to Verify Greedy is Correct

### Exchange Argument
1. Assume an optimal solution that differs from the greedy solution at some step.
2. Show that swapping the non-greedy choice for the greedy choice doesn't make the solution worse.
3. Repeat until the optimal solution matches the greedy solution.

### Structural Argument
Show that the greedy choice is part of *some* optimal solution, and the remaining subproblem is smaller.

### Counterexample to Disprove
Find one input where greedy fails. Example: coin change with denominations {1, 3, 4} and target 6. Greedy picks 4+1+1=3 coins, but optimal is 3+3=2 coins. This problem needs DP.

---

## Common Mistakes

- **Assuming greedy works without proof:** always look for a counterexample or sketch an exchange argument. Classic trap: coin change with arbitrary denominations requires DP.
- **Not sorting when needed:** most greedy solutions require sorted input. Think about what to sort by (start time? end time? ratio?).
- **Not handling ties correctly:** when two items have equal priority, the tie-breaking rule matters (e.g., intervals with same end time).
- **Confusing "greedy works for this variant" with "greedy works for all variants":** e.g., greedy works for Buy/Sell Stock II (unlimited transactions) but not for Buy/Sell Stock III (at most 2 transactions).
- **Off-by-one in boundary conditions:** especially in jump game, gas station (circular), and interval endpoints.
