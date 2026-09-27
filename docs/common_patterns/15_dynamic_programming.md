# Dynamic Programming

The hardest algorithmic problems ask for the *best* of something: the cheapest, the longest, the fewest. For these optimization problems we've seen two approaches, each with a fatal flaw. **Exhaustive search** tries every possibility, so it's always correct — but it's usually exponential. **Greedy** algorithms commit to one locally best choice, so they're fast — but they're usually wrong.

**Dynamic programming** combines the best of both. Like exhaustive search, it considers every possibility, so it's correct. But it notices that a naive search solves the **same subproblems over and over**, and it solves each one just once, storing the answer in a table. When the number of distinct subproblems is small, an exponential search collapses into a polynomial algorithm.

Until you understand it, dynamic programming seems like magic. Once you do, it's perhaps the easiest design technique to apply — often easier to re-derive from scratch than to look up.

---

## Caching vs. Computation

The simplest illustration is the Fibonacci numbers, $F_n = F_{n-1} + F_{n-2}$ with $F_0 = 0$, $F_1 = 1$.

**Recursion.** Transcribe the definition directly:

```python
def fib_recursive(n: int) -> int:
    if n < 2:
        return n
    return fib_recursive(n - 1) + fib_recursive(n - 2)
```

It's correct, and it's catastrophically slow. The call tree for $F_n$ has $F_{n+1}$ leaves, and $F_n$ grows like $1.618^n$: computing $F_{45}$ this way makes over a billion calls. The waste is plain in the call tree: $F_{n-2}$ is computed twice, $F_{n-3}$ three times, $F_{n-4}$ five times...

**Caching.** There are only $n + 1$ distinct arguments. Store each result the first time it's computed, and look it up after that:

```python
from functools import cache


@cache
def fib_memo(n: int) -> int:
    if n < 2:
        return n
    return fib_memo(n - 1) + fib_memo(n - 2)
```

Now each value is computed once: $O(n)$ time. This is **memoization**, or top-down DP.

!!! tip "Take-Home Lesson"
    Explicitly caching the results of recursive calls gives most of the benefit of dynamic programming — usually the same running time. If you can write a correct recursive solution whose arguments take few distinct values, adding a cache is often all it takes.

**Computation in order.** Better still, notice that $F_i$ depends only on smaller values, so compute them from smallest to largest. No recursion at all:

```python
def fib_dp(n: int) -> int:
    back2, back1 = 0, 1                  # F(i-2), F(i-1)
    for _ in range(n):
        back2, back1 = back1, back1 + back2
    return back2
```

Since each value depends only on the previous two, we don't even need the table: $O(n)$ time, $O(1)$ space. This is **tabulation**, or bottom-up DP.

---

## The Recipe

Dynamic programming is a way of efficiently implementing a **recursive** algorithm. So the recurrence comes first, and the table second. Every DP solution goes through three steps:

1. **Formulate the answer as a recurrence** relating the problem to smaller instances of itself. This is where correctness lives.
2. **Show that the recurrence takes only polynomially many distinct parameter values.** Those values are the **states** — the cells of the table. This is where efficiency lives.
3. **Choose an evaluation order** so that every subproblem is solved before it's needed.

And, often, a fourth: **reconstruct the solution** itself (not just its cost) by recording which choice won at each state, then following those choices backward.

The running time is always

$$\text{(number of states)} \times \text{(work to evaluate one state)}.$$

### Top-down or bottom-up?

| | Memoization (top-down) | Tabulation (bottom-up) |
|---|---|---|
| How | Recursive function + `@cache` | Loops filling a table in dependency order |
| Evaluation order | Automatic | You must choose it |
| States computed | Only those reachable from the start | All of them |
| Space optimization | Hard | Easy: keep only the rows you still need |
| Pitfalls | Recursion depth; cache overhead | Getting the loop order right |

Write the memoized version first when the recurrence is new to you — it's the recurrence, transcribed. Convert to tabulation when you need to save space, avoid deep recursion, or squeeze out constant factors.

---

## One Sequence: "The Best Answer Ending Here"

The most common DP state for a sequence is an index $i$, meaning "the best answer for the first $i$ elements" or "the best answer that **ends at** element $i$."

### House Robber (LC 198)

Maximize the sum of chosen houses with no two adjacent. For the first $i$ houses, either the $i$-th house is robbed (so house $i - 1$ isn't) or it isn't:

$$\text{best}(i) = \max\big(\text{best}(i-1),\ \text{best}(i-2) + a_i\big)$$

```python
def rob(nums: list[int]) -> int:
    skip = take = 0                     # best for the first i-2, i-1 houses
    for x in nums:
        skip, take = take, max(take, skip + x)
    return take
```

That "take it or leave it" split — the item is either in the solution or not — is the most common recurrence pattern in all of DP. **Climbing Stairs** (LC 70) is Fibonacci; **Maximum Subarray** (LC 53) uses "best ending here" (see [Kadane's algorithm](03_two_pointers_sliding_window.md#largest-subrange-three-algorithms-for-one-problem)).

### Word Break (LC 139)

Can the string be split into dictionary words? `ok[i]` is true if the prefix `s[:i]` can be split. It can be exactly when some split point $j < i$ has `ok[j]` true and `s[j:i]` is a word:

```python
def word_break(s: str, words: list[str]) -> bool:
    dictionary = set(words)
    longest = max(map(len, dictionary), default=0)
    ok = [True] + [False] * len(s)
    for i in range(1, len(s) + 1):
        for j in range(max(0, i - longest), i):
            if ok[j] and s[j:i] in dictionary:
                ok[i] = True
                break
    return ok[-1]
```

This is exactly what the backtracking solution computes, except that "can `s[j:]` be segmented?" is answered once per $j$ instead of once per path to $j$. **Decode Ways** (LC 91) has the same shape.

---

## Longest Increasing Subsequence (LC 300)

Given a sequence, find the longest subsequence (not necessarily contiguous) whose elements strictly increase. For $S = (2, 4, 3, 5, 1, 7, 6, 9, 8)$, one answer is $(2, 3, 5, 6, 8)$, of length 5.

Deriving the recurrence is instructive. Ask: *what would I need to know about the first $n - 1$ elements to finish the job?*

- The **length** $L$ of the longest increasing subsequence of the first $n - 1$ elements? Not enough. If $L = 5$ and $s_n = 8$, whether 8 extends it depends on whether *some* length-5 subsequence ends below 8.
- So we need, for each possible ending element, the longest subsequence ending there. Define $L_i$ = length of the longest increasing subsequence **ending at** $s_i$:

$$L_i = 1 + \max_{\substack{j < i \\ s_j < s_i}} L_j \qquad (\text{or } 1 \text{ if no such } j)$$

The answer is $\max_i L_i$ — the winning subsequence must end somewhere.

| $i$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| $s_i$ | 2 | 4 | 3 | 5 | 1 | 7 | 6 | 9 | 8 |
| $L_i$ | 1 | 2 | 2 | 3 | 1 | 4 | 4 | 5 | 5 |

Store each element's best predecessor, and the subsequence itself can be read backward from the element with the largest $L_i$:

```python
def longest_increasing_subsequence(nums: list[int]) -> list[int]:
    n = len(nums)
    length = [1] * n
    prev = [-1] * n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i] and length[j] + 1 > length[i]:
                length[i] = length[j] + 1
                prev[i] = j
    if not nums:
        return []
    i = max(range(n), key=length.__getitem__)
    seq = []
    while i != -1:
        seq.append(nums[i])
        i = prev[i]
    return seq[::-1]
```

$O(n^2)$ time. Notice the move we made — the obvious quantity wasn't enough, so we asked for more information about every prefix. It's the same "strengthen the hypothesis" move as in [tree recursion](10_trees.md#strengthening-the-hypothesis), and it's how most DP states are discovered.

### $O(n \log n)$ with patience sorting

Keep an array `tails`, where `tails[k]` is the **smallest possible last element** of an increasing subsequence of length $k + 1$ seen so far. `tails` is always strictly increasing, so for each new element, binary search finds the first tail $\ge x$ and replaces it (or appends $x$ if $x$ beats them all):

```python
import bisect


def length_of_lis(nums: list[int]) -> int:
    tails: list[int] = []
    for x in nums:
        k = bisect.bisect_left(tails, x)
        if k == len(tails):
            tails.append(x)              # x extends the longest subsequence so far
        else:
            tails[k] = x                 # a length-(k+1) subsequence can now end lower
    return len(tails)
```

Replacing a tail with a smaller value never hurts: a subsequence ending lower is at least as easy to extend later. (`tails` is *not* itself an increasing subsequence of the input — only its length is meaningful.) **Russian Doll Envelopes** (LC 354) is LIS after sorting by width ascending and height *descending*, so that envelopes of equal width can't nest.

---

## Two Sequences: Edit Distance (LC 72)

How many single-character **insertions, deletions, and substitutions** turn string $P$ into string $T$? This edit distance underlies spell checkers, `diff`, and DNA alignment.

Finding the best sequence of edits looks daunting: where should the insertions go? The trick is to think about the problem **in reverse**, and ask only what happens to the **last characters**. In an optimal alignment of $P[1..i]$ and $T[1..j]$, the last operation is one of:

- **Match or substitute** $P_i$ with $T_j$: cost 0 if they're equal, else 1, plus the cost of aligning $P[1..i-1]$ with $T[1..j-1]$.
- **Insert** $T_j$: cost 1, plus aligning $P[1..i]$ with $T[1..j-1]$.
- **Delete** $P_i$: cost 1, plus aligning $P[1..i-1]$ with $T[1..j]$.

There's no other possibility. So, with $D[i][j]$ the edit distance between the first $i$ characters of $P$ and the first $j$ of $T$:

$$D[i][j] = \min\begin{cases} D[i-1][j-1] + [P_i \ne T_j] \\ D[i][j-1] + 1 \\ D[i-1][j] + 1 \end{cases} \qquad D[i][0] = i,\ D[0][j] = j$$

The naive recursion branches three ways at every step — exponential. But there are only $(|P| + 1)(|T| + 1)$ distinct $(i, j)$ pairs, so the table has that many cells, each filled in $O(1)$:

```python
def min_distance(p: str, t: str) -> int:
    m, n = len(p), len(t)
    prev = list(range(n + 1))                     # row i-1 of the table
    for i in range(1, m + 1):
        curr = [i] + [0] * n
        for j in range(1, n + 1):
            curr[j] = min(
                prev[j - 1] + (p[i - 1] != t[j - 1]),   # match / substitute
                curr[j - 1] + 1,                        # insert t[j-1]
                prev[j] + 1,                            # delete p[i-1]
            )
        prev = curr
    return prev[n]
```

$O(mn)$ time. Each row depends only on the previous one, so two rows suffice: $O(n)$ space. (Reconstructing the actual edits needs the full table, or a cleverer divide-and-conquer.)

### One routine, many problems

Small changes to the costs, the base cases, or the goal cell turn edit distance into other classic problems:

- **Longest Common Subsequence** (LC 1143): forbid substitution. Then the only way to handle mismatched characters is to delete them, so the cheapest alignment keeps the most matches. Directly:

```python
def longest_common_subsequence(a: str, b: str) -> int:
    prev = [0] * (len(b) + 1)
    for i in range(1, len(a) + 1):
        curr = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev = curr
    return prev[-1]
```

- **Delete Operation for Two Strings** (LC 583): $|a| + |b| - 2 \cdot \text{LCS}$.
- **Longest increasing subsequence** is the LCS of the sequence with its own sorted, de-duplicated version.
- **Approximate substring matching**: to find where pattern $P$ best matches *anywhere* in text $T$, make skipping a prefix of $T$ free ($D[0][j] = 0$) and take the best cell in the last row. Without this change, the "best" match of a short pattern in a long text is dominated by the cost of deleting everything else.
- **Distinct Subsequences** (LC 115), **Interleaving String** (LC 97), **Regular Expression Matching** (LC 10), and **Wildcard Matching** (LC 44) are all two-index DPs with the same "what happens to the last characters?" derivation.

!!! tip "Take-Home Lesson"
    For optimization problems on objects with a natural **left-to-right order** — characters of a string, elements of a sequence, points along a line, leaves of a tree — dynamic programming very likely gives an efficient algorithm. The states are simply positions in the order.

---

## Subset Sum and Knapsack

**Subset sum:** is there a subset of $s_1, \ldots, s_n$ adding up to exactly $k$? Consider the items left to right. Either the last item $s_n$ is in the subset — so the first $n - 1$ items must make $k - s_n$ — or it isn't — so they must make $k$ on their own:

$$T[n][k] = T[n-1][k] \ \lor\ T[n-1][k - s_n]$$

That's $O(nk)$ time for $n$ items and target $k$. Note that this is polynomial in the *value* $k$, not in the number of bits needed to write $k$ down — it's fast when $k$ is modest, but with $k \approx 10^{18}$ the table is useless. (Subset sum is NP-complete; DP doesn't contradict that.)

In code, each row depends only on the previous one, so a single 1-D array suffices — **if the inner loop runs downward**, so that `reachable[j - x]` still refers to the previous row (a sum not yet using the current item):

```python
def can_partition(nums: list[int]) -> bool:
    """LC 416: split into two halves of equal sum = subset summing to total / 2."""
    total = sum(nums)
    if total % 2:
        return False
    target = total // 2
    reachable = [True] + [False] * target
    for x in nums:
        for j in range(target, x - 1, -1):          # downward: each item used at most once
            reachable[j] = reachable[j] or reachable[j - x]
    return reachable[target]
```

The **0/1 knapsack** problem is the same recurrence with values: `best[j] = max(best[j], best[j - w] + v)`, again iterating capacity downward.

### Unbounded items: coin change

If each item can be used **any number of times**, iterate the capacity **upward**: then `dp[j - c]` may already include coin $c$, which is exactly what reuse means.

```python
def coin_change(coins: list[int], amount: int) -> int:
    """LC 322: fewest coins summing to amount."""
    INF = amount + 1
    fewest = [0] + [INF] * amount
    for c in coins:
        for j in range(c, amount + 1):              # upward: coin c can be reused
            fewest[j] = min(fewest[j], fewest[j - c] + 1)
    return fewest[amount] if fewest[amount] != INF else -1
```

Here greedy fails (coins $\{1, 6, 10\}$, amount 12 — see [Greedy](14_greedy.md#when-greedy-fails)) but DP is always right, because it considers every last coin.

### Counting: combinations vs. permutations

When **counting** the ways to reach a total, the loop order decides what's being counted:

```python
def count_combinations(coins: list[int], amount: int) -> int:
    """LC 518: {1, 2} and {2, 1} are the same way. Coins in the OUTER loop."""
    ways = [1] + [0] * amount
    for c in coins:
        for j in range(c, amount + 1):
            ways[j] += ways[j - c]
    return ways[amount]


def count_sequences(nums: list[int], target: int) -> int:
    """LC 377: (1, 2) and (2, 1) are different. Totals in the OUTER loop."""
    ways = [1] + [0] * target
    for j in range(1, target + 1):
        for x in nums:
            if x <= j:
                ways[j] += ways[j - x]
    return ways[target]
```

With coins outer, each combination is built in one canonical order (all 1s, then all 2s, ...), so it's counted once. With totals outer, every choice of *last* element is counted separately at every step, so orderings are distinct.

| Variant | Loop structure | Inner direction |
|---|---|---|
| 0/1 (each item once) | items outer | capacity **downward** |
| Unbounded (reuse allowed) | items outer | capacity **upward** |
| Count unordered combinations | items outer | upward |
| Count ordered sequences | totals outer | items inner |

---

## Ordered Partition

Three workers must scan a shelf of books, each taking a **contiguous** section. How should the shelf be divided to minimize the largest section? For books with page counts $100, 200, \ldots, 900$, splitting into equal numbers of books gives sections of 600, 1500, and 2400 pages. The best split, $(100 \ldots 500 \mid 600, 700 \mid 800, 900)$, has a largest section of 1700.

Heuristics like "aim for the average" fail on some inputs. Instead, think recursively about the **last divider**. If the last section is books $i + 1 \ldots n$, the cost is the larger of that section's total and the best way to split the first $i$ books into $k - 1$ sections:

$$M[n][k] = \min_{i < n} \max\Big(M[i][k-1],\ \sum_{j=i+1}^{n} s_j\Big)$$

With prefix sums, each range sum is $O(1)$, and the table has $nk$ cells each taking $O(n)$: $O(kn^2)$ total.

```python
def linear_partition(s: list[int], k: int) -> int:
    n = len(s)
    prefix = [0]
    for x in s:
        prefix.append(prefix[-1] + x)
    INF = float("inf")
    # M[j][p]: best max-section for the first j items in p sections
    M = [[INF] * (k + 1) for _ in range(n + 1)]
    M[0][0] = 0
    for p in range(1, k + 1):
        for j in range(1, n + 1):
            for i in range(p - 1, j):                   # last section is s[i:j]
                M[j][p] = min(M[j][p], max(M[i][p - 1], prefix[j] - prefix[i]))
    return min(M[n][p] for p in range(1, k + 1))       # "k or fewer" sections
```

This is **Split Array Largest Sum** (LC 410). The [binary search on the answer](02_binary_search.md#split-array-largest-sum-lc-410) solution is faster, $O(n \log \sum s)$ — but the DP generalizes to costs where no greedy feasibility check exists.

---

## Interval DP

Some problems are naturally about **substrings or subarrays** $[i, j]$, and the answer for an interval combines answers for smaller intervals inside it. Evaluate in order of increasing **length**, so that every smaller interval is ready.

**Longest Palindromic Subsequence** (LC 516): if the end characters match, they wrap a palindrome inside; otherwise drop one end.

```python
def longest_palindrome_subseq(s: str) -> int:
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):                      # i descending: dp[i+1] is ready
        dp[i][i] = 1
        for j in range(i + 1, n):
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
    return dp[0][n - 1] if n else 0
```

**Burst Balloons** (LC 312) is the famous hard case, and it shows a key trick for interval DP: think about the **last** operation inside an interval, not the first. If balloon $k$ is the last one burst in the open interval $(i, j)$, then its neighbors at that moment are exactly $i$ and $j$, and the two sides are independent subproblems:

$$\text{dp}[i][j] = \max_{i < k < j} \big(\text{dp}[i][k] + a_i \cdot a_k \cdot a_j + \text{dp}[k][j]\big)$$

Choosing the *first* balloon instead would leave neighbors that depend on everything burst later — no clean subproblems. The same "last step" idea gives matrix-chain multiplication and optimal binary search trees, all $O(n^3)$.

---

## State Machine DP

When the decision at each step depends on a small amount of **mode** — holding a stock or not, in cooldown or not — make the mode part of the state. **Best Time to Buy and Sell Stock with Cooldown** (LC 309) has three modes per day:

```python
def max_profit_cooldown(prices: list[int]) -> int:
    hold, sold, rest = float("-inf"), 0, 0      # holding / just sold / free to buy
    for p in prices:
        hold, sold, rest = max(hold, rest - p), hold + p, max(rest, sold)
    return max(sold, rest)
```

Each line of the tuple assignment is a transition: you can hold by keeping your stock or buying from the "free" mode; you're "just sold" only by selling today; you're free if you were free or your cooldown just ended. The other stock problems (LC 123, 188, 714) add a transaction counter or a fee to the same machine.

---

## Beyond Sequences: Trees and Subsets

**On trees**, the natural order is bottom-up: a node's answer combines its children's. **House Robber III** (LC 337) returns a pair per node — the best total with the node robbed, and without it — which is DP with the state stored in the recursion's return value (see [Trees](10_trees.md#strengthening-the-hypothesis)).

**On subsets**, when there's no natural order, the state must remember *which* items have been used. Consider finding the shortest route visiting every city exactly once (the traveling salesman problem). A recurrence over "the path so far" is correct but has $n!$ states — it's just backtracking. But the future doesn't depend on the **order** of the cities visited, only on **which** cities were visited and **where you are now**. That gives $2^n \cdot n$ states:

$$\text{best}[S][v] = \min_{u \in S \setminus \{v\}} \big(\text{best}[S \setminus \{v\}][u] + d(u, v)\big)$$

```python
def shortest_tour(dist: list[list[int]]) -> int:
    """Held–Karp: shortest cycle through all cities, starting and ending at city 0."""
    n = len(dist)
    INF = float("inf")
    best = [[INF] * n for _ in range(1 << n)]
    best[1][0] = 0                                      # visited {0}, standing at 0
    for S in range(1 << n):
        if not S & 1:
            continue                                    # every path starts at city 0
        for v in range(n):
            if best[S][v] == INF:
                continue
            for w in range(n):
                if not S >> w & 1:
                    T = S | 1 << w
                    best[T][w] = min(best[T][w], best[S][v] + dist[v][w])
    full = (1 << n) - 1
    return min(best[full][v] + dist[v][0] for v in range(n)) if n > 1 else 0
```

$O(n^2 2^n)$ — feasible for $n \approx 20$, where $n!$ would be hopeless. Subsets as integers are covered in [Bit Manipulation](04_bit_manipulation.md#bit-vectors-integers-as-sets).

---

## When Does DP Work?

**When is it correct?** DP requires the **principle of optimality**: an optimal solution can be extended using only the *state* reached so far, not the specific decisions that led there. Edit distance satisfies it — the best way to finish aligning two strings doesn't depend on which edits were used to align their prefixes. A "longest simple path" recurrence that tracks only the current vertex violates it: whether the next step is legal depends on *which* vertices the path has already used. Fix it by enlarging the state (the subset of visited vertices), at exponential cost.

**When is it efficient?** When the number of states is small. Objects with an inherent **left-to-right order** — strings, sequences, rooted trees — have only $O(n)$ or $O(n^2)$ possible "stopping points," so they give polynomial DPs. Without such an order, the state must record an arbitrary subset, and the table is exponential.

!!! tip "Take-Home Lesson"
    Without an inherent left-to-right ordering on the objects, dynamic programming is usually doomed to require exponential space and time. When you're designing a DP, look first for the order that lets you describe a partial solution by a position (or a pair of positions).

---

## Recognizing a DP Problem

- The problem asks for an **optimum** (min, max, longest, fewest) or a **count** (number of ways) — rarely for the actual list of all solutions.
- A brute-force search would make a **sequence of decisions**, and the future depends only on a **small summary** of the decisions made so far.
- The recursive brute force **revisits** the same arguments.
- Greedy fails on small counterexamples.
- Constraints are modest in the dimensions that define the state: $n \le 5000$ for $O(n^2)$ states, $n \le 20$ for $O(2^n)$ subset states, sums up to about $10^4$–$10^5$ for knapsack.

---

## Common Mistakes

1. **Writing the table before the recurrence.** Get a correct recursive definition first; the table is just a way to evaluate it.

2. **Missing information in the state.** If the recurrence needs to know something the state doesn't record (like the last element in LIS, or the mode in the stock problems), it will be wrong. Add it to the state.

3. **Wrong evaluation order.** Every state must be computed after the states it depends on. Interval DP goes by increasing length; 1-D knapsack goes downward for 0/1, upward for unbounded.

4. **Off-by-one in table dimensions.** Tables indexed by prefix *length* have $n + 1$ rows, with row 0 for the empty prefix. Decide whether `dp[i]` means "first $i$ items" or "ending at item $i$", and write it down.

5. **Wrong base cases.** `dp[0] = 1` for counting (one way to make zero), `dp[0] = 0` for costs; unreachable states should be $\pm\infty$, not 0.

6. **Recursion depth in memoized solutions.** `@cache` recursion 10⁴ levels deep exceeds Python's limit. Tabulate, or raise the limit carefully.

7. **Confusing combinations and permutations** in counting problems — the loop order decides.

---

## Practice Problems

| Problem | State / idea |
|---|---|
| Climbing Stairs (LC 70) | Fibonacci |
| House Robber (LC 198) | Take or skip |
| House Robber II (LC 213) | Two linear runs (circle broken) |
| Decode Ways (LC 91) | Prefix length |
| Word Break (LC 139) | Prefix segmentable? |
| Unique Paths (LC 62) | Grid counting (Pascal's triangle) |
| Minimum Path Sum (LC 64) | Grid cost |
| Longest Increasing Subsequence (LC 300) | Best ending here; patience sorting |
| Russian Doll Envelopes (LC 354) | LIS after a clever sort |
| Longest Common Subsequence (LC 1143) | Two prefixes |
| Edit Distance (LC 72) | What happens to the last characters |
| Partition Equal Subset Sum (LC 416) | Subset sum, downward 1-D |
| Coin Change (LC 322) | Unbounded, upward |
| Coin Change II (LC 518) | Count combinations: items outer |
| Combination Sum IV (LC 377) | Count sequences: totals outer |
| Longest Palindromic Subsequence (LC 516) | Interval DP |
| Burst Balloons (LC 312) | Interval DP on the last operation |
| Best Time to Buy and Sell Stock with Cooldown (LC 309) | State machine |
| House Robber III (LC 337) | Tree DP returning a pair |
| Split Array Largest Sum (LC 410) | Ordered partition |
| Maximal Square (LC 221) | Largest square ending at each cell |
| Regular Expression Matching (LC 10) | Two indices, pattern cases |
