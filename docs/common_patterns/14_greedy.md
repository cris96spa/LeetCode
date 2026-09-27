# Greedy Algorithms

A greedy algorithm builds a solution one decision at a time, always taking the choice that looks best **right now**, and never reconsidering. It is the most natural way to attack an optimization problem, and when it works it is hard to beat: usually a sort followed by a single pass.

The difficulty is that it often doesn't work. Greedy algorithms are easy to invent, easy to code, and — very frequently — wrong in ways that simple test cases won't reveal. So this chapter is only partly about greedy *techniques*. It is mostly about the discipline that makes them safe: **proving a greedy choice correct, or finding the counterexample that shows it isn't**.

!!! tip "Take-Home Lesson"
    There is a fundamental difference between an **algorithm**, which always produces a correct result, and a **heuristic**, which usually does a good job but offers no guarantee. A greedy procedure is a heuristic until you have proved it is an algorithm.

---

## Where Greedy Sits

Every optimization problem can be attacked in three ways:

| Approach | Correct? | Fast? |
|---|---|---|
| **Exhaustive search** (backtracking) | Always — it tries everything | Usually exponential |
| **Greedy** | Only with proof — it commits to one choice | Usually $O(n \log n)$ |
| **Dynamic programming** | Always — it tries everything *systematically* | Polynomial when there are few distinct subproblems |

Greedy and DP both build a solution from decisions. The difference is that DP keeps the consequences of **every** option for each decision, while greedy keeps only **one**. So greedy is correct precisely when you can prove that the locally best choice is always *part of some* optimal solution — that you never need the options you threw away.

---

## When Greedy Fails

Before learning to prove greedy algorithms right, it helps to see how easily they go wrong.

**Making change.** Pay $n$ units with as few coins as possible. Greedy: repeatedly take the largest coin that fits. With US coins $\{1, 5, 10, 25\}$ this is optimal. But with coins $\{1, 6, 10\}$ and $n = 12$, greedy takes $10 + 1 + 1$ (three coins), while $6 + 6$ uses two. Nothing in the greedy rule changed; the *problem instance* did. Coin Change (LC 322) therefore needs DP.

**0/1 knapsack.** Pack items into a bag of capacity $W$ to maximize total value. Greedy by value-per-weight fails with capacity 10 and items (weight 6, value 7), (weight 5, value 5), (weight 5, value 5): greedy takes the densest item first and has room for nothing else (value 7), while the two lighter items give 10. But if items can be **cut** (the *fractional* knapsack), greedy by density is optimal — the troublesome leftover space can always be filled with a fraction of the next item.

**Movie scheduling.** Choosing the largest set of non-overlapping intervals by earliest start or by shortest length both fail, on instances with just two or three intervals (see [Intervals](08_intervals.md#three-plausible-ideas-three-failures)).

The pattern in all three: greedy fails when an early choice **blocks** better combinations later. A proof of correctness must show that this can't happen.

---

## How to Prove a Greedy Algorithm Correct

### 1. The exchange argument

Take any optimal solution that *disagrees* with the greedy choice, and show you can **exchange** part of it for the greedy choice without making it worse. Then some optimal solution agrees with greedy's first choice; repeat the argument for the rest.

**Example: minimizing total completion time.** One machine, $n$ jobs with processing times $t_i$. In what order should they run to minimize the sum of their completion times?

Claim: **shortest job first**. Suppose an optimal order has two adjacent jobs $a$ then $b$ with $t_a > t_b$. Swap them. Jobs before and after the pair are unaffected. Before the swap, the pair contributes $(T + t_a) + (T + t_a + t_b)$ to the sum; after, $(T + t_b) + (T + t_b + t_a)$. The swap saves $t_a - t_b > 0$. So an optimal order has no such "inversions" — it's sorted by processing time.

```python
def min_total_completion_time(times: list[int]) -> int:
    total = elapsed = 0
    for t in sorted(times):                  # shortest processing time first
        elapsed += t
        total += elapsed
    return total
```

The same adjacent-swap argument proves many "sort by the right key" algorithms: sort by the key under which swapping any out-of-order adjacent pair never hurts.

### 2. Greedy stays ahead

Show by induction that after each step, greedy's partial solution is **at least as good** as any other algorithm's partial solution after the same number of steps — so at the end, greedy can't be behind. The proof that earliest-finish-first maximizes the number of non-overlapping intervals has this form: greedy's $k$-th interval always ends no later than any other solution's $k$-th interval.

### 3. Match a lower bound

Find a simple reason why **no** solution can do better than some value $L$, then show greedy achieves $L$. For meeting rooms, $L$ is the maximum number of meetings overlapping at one instant; greedy room assignment never opens more rooms than that (see [Intervals](08_intervals.md#partitioning-how-many-rooms-lc-253)). This is often the quickest proof when it applies.

### ... and always hunt for counterexamples

Before investing in a proof, spend two minutes trying to break the greedy rule: **think small** (two or three items), **seek extremes** (one huge item among tiny ones), and **go for ties** (make everything look equally attractive so the rule has nothing to go on). If a small counterexample exists, you'll usually find it quickly; if you can't find one, the attempt often shows you why the proof works.

---

## Classic Greedy Algorithms

### Earliest deadline first

$n$ jobs each have a processing time and a deadline. Is there an order in which every job finishes by its deadline? **Sort by deadline.** If any feasible order exists, this one is feasible: by the exchange argument, if a job with a later deadline runs immediately before one with an earlier deadline, swapping them doesn't make either one late — the earlier-deadline job finishes sooner, and the later-deadline job now finishes when the first one used to, which met an even earlier deadline.

```python
def all_deadlines_met(jobs: list[tuple[int, int]]) -> bool:
    """jobs[i] = (processing_time, deadline)."""
    elapsed = 0
    for duration, deadline in sorted(jobs, key=lambda j: j[1]):
        elapsed += duration
        if elapsed > deadline:
            return False
    return True
```

If jobs can be *dropped* to fit as many as possible (Course Schedule III, LC 630), process by deadline and keep a max-heap of the durations taken; whenever the total exceeds the current deadline, drop the longest job so far. Dropping the longest job frees the most time while losing only one job.

### Huffman coding

To compress text, give frequent symbols short codes and rare symbols long ones, with no code a prefix of another. **Huffman's algorithm**: repeatedly merge the two **least frequent** symbols into a combined symbol whose frequency is their sum, until one remains. The merges form a binary tree; each symbol's code is its root-to-leaf path. The greedy choice is right because the two rarest symbols can always be placed as siblings at the deepest level of some optimal tree (an exchange argument).

With a heap, this is $O(n \log n)$. The same algorithm solves **Minimum Cost to Connect Sticks** (LC 1167), where merging two sticks costs their total length:

```python
import heapq


def connect_sticks(sticks: list[int]) -> int:
    heap = sticks[:]
    heapq.heapify(heap)
    cost = 0
    while len(heap) > 1:
        merged = heapq.heappop(heap) + heapq.heappop(heap)   # the two cheapest
        cost += merged
        heapq.heappush(heap, merged)
    return cost
```

### Graph algorithms

Several of the most important graph algorithms are greedy, each with an exchange-argument proof: **Prim's** and **Kruskal's** minimum spanning tree algorithms (always take the lightest edge that crosses a cut) and **Dijkstra's** shortest paths (always finalize the closest unfinished vertex). See [Graphs](11_graphs.md#minimum-spanning-trees).

---

## Interview Patterns

Each of these comes with the argument that makes it correct. The argument is the part to remember.

### Reachability: Jump Game (LC 55)

`nums[i]` is the maximum jump from index $i$. Can you reach the end?

Track the **farthest index reachable** so far. If the scan ever reaches an index beyond it, that index — and everything after it — is unreachable.

```python
def can_jump(nums: list[int]) -> bool:
    reach = 0
    for i, jump in enumerate(nums):
        if i > reach:
            return False
        reach = max(reach, i + jump)
    return True
```

**Why:** the reachable indices always form a prefix $[0, \text{reach}]$ — if you can reach index $j$, you can reach every index before it (by stopping short on the jump that passed it).

### Jump Game II (LC 45): BFS in disguise

Minimum number of jumps to reach the end. Think of it as **BFS by levels**: level $k$ is the range of indices reachable in exactly $k$ jumps, and the next level extends to the farthest point reachable from anywhere in the current one.

```python
def jump(nums: list[int]) -> int:
    jumps = 0
    level_end = farthest = 0
    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])
        if i == level_end:              # finished scanning this level
            jumps += 1
            level_end = farthest
    return jumps
```

It's greedy in the sense of never tracking individual paths, but its correctness is BFS's: levels are explored in order, so the first level containing the last index gives the fewest jumps.

### Gas Station (LC 134)

A circular route of stations; `gas[i]` is available at station $i$ and `cost[i]` is needed to reach the next. Find a start from which the full loop is possible.

```python
def can_complete_circuit(gas: list[int], cost: list[int]) -> int:
    if sum(gas) < sum(cost):
        return -1
    start = tank = 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:                     # can't reach i + 1 from start
            start, tank = i + 1, 0
    return start
```

Two facts make this correct. **(1)** If starting at $s$ you first run dry before reaching $j + 1$, then no start between $s$ and $j$ works either: you arrived at each of them with a non-negative tank, so starting there fresh (with an empty tank) can only be worse. That's why the start jumps straight to $j + 1$. **(2)** If the total gas covers the total cost, the start that survives the scan works for the whole loop: the deficit accumulated before it is exactly covered by the surplus gathered after it.

### Partition Labels (LC 763)

Split a string into as many parts as possible so that each letter appears in only one part. Each part must extend at least to the **last occurrence** of every letter inside it; greedily close a part the moment the scan reaches the farthest last-occurrence seen so far.

```python
def partition_labels(s: str) -> list[int]:
    last = {ch: i for i, ch in enumerate(s)}
    sizes = []
    start = end = 0
    for i, ch in enumerate(s):
        end = max(end, last[ch])
        if i == end:
            sizes.append(end - start + 1)
            start = i + 1
    return sizes
```

Closing as early as possible is safe because any valid partition must include the whole range $[\text{start}, \text{end}]$ in one part; closing there leaves the rest free to be split as finely as possible.

### Constraints from both sides: Candy (LC 135)

Children in a row with ratings; each gets at least one candy, and a child with a higher rating than a neighbor gets more than that neighbor. Minimize total candy.

Each child faces two independent constraints — from the left neighbor and from the right. Satisfy each with a greedy pass, then take the maximum:

```python
def candy(ratings: list[int]) -> int:
    n = len(ratings)
    left = [1] * n
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            left[i] = left[i - 1] + 1
    right = [1] * n
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            right[i] = right[i + 1] + 1
    return sum(max(l, r) for l, r in zip(left, right))
```

**Why minimal:** `left[i]` is the smallest value satisfying all left-side constraints, and `right[i]` all right-side ones — each is forced by the length of the increasing run leading to $i$. So every valid assignment gives child $i$ at least `max(left[i], right[i])`, and that assignment is itself valid.

### Pairing after sorting

**Boats to Save People** (LC 881): each boat holds two people, with a weight limit. Sort; pair the heaviest remaining person with the lightest if they fit, otherwise send the heaviest alone.

```python
def num_rescue_boats(people: list[int], limit: int) -> int:
    people = sorted(people)
    lo, hi = 0, len(people) - 1
    boats = 0
    while lo <= hi:
        if people[lo] + people[hi] <= limit:
            lo += 1                      # the lightest rides along
        hi -= 1                          # the heaviest always leaves
        boats += 1
    return boats
```

**Exchange argument:** if the heaviest person can share with anyone, they can share with the lightest. In any optimal solution, swapping the lightest person into the heaviest's boat (and moving whoever was there into the lightest's old spot) keeps every boat within the limit. If the heaviest can't share even with the lightest, they must go alone.

**Assign Cookies** (LC 455) and **Two City Scheduling** (LC 1029, sort by the *difference* in the two costs) follow the same "sort, then match" shape, each justified by an exchange.

### Structure forced by the smallest element: Hand of Straights (LC 846)

Can the cards be split into groups of $W$ consecutive values? The **smallest** remaining card can't be the middle or end of a group — nothing smaller is left — so it must start one. That forced choice is the greedy step:

```python
from collections import Counter


def is_n_straight_hand(hand: list[int], w: int) -> bool:
    count = Counter(hand)
    for x in sorted(count):
        need = count[x]
        if need:
            for y in range(x, x + w):
                if count[y] < need:
                    return False
                count[y] -= need
    return True
```

When a greedy choice is **forced** — every valid solution must make it — no exchange argument is needed at all.

### Counting the slack: Task Scheduler (LC 621)

Tasks with a cooldown of $n$ between identical tasks; find the minimum total time. Let the most frequent task appear $f$ times, and $m$ tasks tie for that frequency. The most frequent task alone forces $f - 1$ full cycles of length $n + 1$, plus a final partial cycle containing the $m$ tied tasks — a **lower bound** of $(f - 1)(n + 1) + m$. Other tasks fill the idle slots; if there are more tasks than slots, there's no idle time at all and the answer is simply the number of tasks.

```python
def least_interval(tasks: list[str], n: int) -> int:
    freq = Counter(tasks).values()
    f = max(freq)
    m = sum(1 for v in freq if v == f)
    return max(len(tasks), (f - 1) * (n + 1) + m)
```

### Local gains: Best Time to Buy and Sell Stock II (LC 122)

With unlimited transactions, every price increase between consecutive days can be captured. The total profit is the sum of all positive day-to-day differences — any longer transaction's profit decomposes into exactly those steps.

```python
def max_profit(prices: list[int]) -> int:
    return sum(max(0, b - a) for a, b in zip(prices, prices[1:]))
```

---

## Greedy as Approximation

For some problems, no efficient exact algorithm is known at all (they are NP-complete), and greedy is used as a heuristic with a **provable quality guarantee**.

**Set cover:** choose as few of the given subsets as possible to cover every element. Greedy repeatedly picks the subset covering the **most still-uncovered** elements. It isn't always optimal — but it is never worse than about $\ln n$ times optimal. The argument: the number of uncovered elements halves at most $\log_2 n$ times; between consecutive halvings, greedy uses some number $w$ of subsets, and since each of them was the best available, the optimal solution also needs at least $w$ subsets to cover those same elements. So greedy uses at most $w \log_2 n \le \text{OPT} \cdot \log_2 n$ subsets.

!!! tip "Take-Home Lesson"
    When a problem is too hard to solve exactly, a greedy heuristic with a proven approximation ratio is a principled compromise: fast, simple, and guaranteed to be close. "Guaranteed close" is a far stronger statement than "usually works."

---

## Common Mistakes

1. **Trusting a greedy rule without proof.** Passing the examples proves nothing. Try small counterexamples; if none turns up, sketch the exchange argument.

2. **Sorting by the wrong key.** Earliest start vs. earliest end, value vs. value per weight, cost vs. cost *difference*. The right key is the one under which an adjacent swap never helps.

3. **Using greedy on problems that need DP.** Coin change with arbitrary denominations, 0/1 knapsack, longest increasing subsequence: any time an early choice can block a better combination later.

4. **Forgetting the global feasibility check.** Gas Station first checks that total gas covers total cost; without it, the scan's answer is meaningless.

5. **Confusing "optimal for these examples" with "optimal."** US coin denominations make greedy change-making correct; most denomination systems don't.

---

## Practice Problems

| Problem | Greedy idea | Justification |
|---|---|---|
| Assign Cookies (LC 455) | Sort both, match smallest adequate | Exchange |
| Best Time to Buy and Sell Stock II (LC 122) | Sum positive differences | Decomposition |
| Jump Game (LC 55) | Track max reach | Reachable set is a prefix |
| Jump Game II (LC 45) | Level-by-level reach | BFS |
| Gas Station (LC 134) | Reset start on deficit | Skipped starts are no better |
| Partition Labels (LC 763) | Close at farthest last occurrence | Forced range |
| Candy (LC 135) | Two passes, take max | Each pass is the minimum for its side |
| Boats to Save People (LC 881) | Heaviest with lightest | Exchange |
| Two City Scheduling (LC 1029) | Sort by cost difference | Exchange |
| Hand of Straights (LC 846) | Smallest card starts a group | Forced choice |
| Task Scheduler (LC 621) | Frequency formula | Lower bound achieved |
| Non-overlapping Intervals (LC 435) | Earliest finish first | Stays ahead |
| Minimum Cost to Connect Sticks (LC 1167) | Merge two smallest | Huffman exchange |
| Course Schedule III (LC 630) | By deadline, drop longest | Exchange |
| Queue Reconstruction by Height (LC 406) | Tallest first, insert at index $k$ | Shorter people don't affect taller ones' counts |
