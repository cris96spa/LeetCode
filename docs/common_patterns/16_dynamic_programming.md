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

**Computation in order.** Better still, notice that $F_i$ depends only on smaller values, so fill a table from smallest to largest. No recursion at all:

```python
def fib_table(n: int) -> int:
    F = [0] * (n + 1)                    # F[i] = the i-th Fibonacci number
    if n > 0:
        F[1] = 1
    for i in range(2, n + 1):
        F[i] = F[i - 1] + F[i - 2]
    return F[n]
```

This is **tabulation**, or bottom-up DP. Now look at what the loop *reads*: only `F[i-1]` and `F[i-2]`. Everything older is dead, so two variables replace the table:

```python
def fib_dp(n: int) -> int:
    back2, back1 = 0, 1                  # F[i-2], F[i-1]
    for _ in range(n):
        back2, back1 = back1, back1 + back2
    return back2
```

$O(n)$ time, $O(1)$ space. Every space-optimized DP in this chapter is a full table compressed this way.

---

## The Recipe

Dynamic programming is a way of efficiently implementing a **recursive** algorithm. So the recurrence comes first, and the table second. Every DP solution goes through three steps:

1. **Formulate the answer as a recurrence** relating the problem to smaller instances of itself. This is where correctness lives.
2. **Show that the recurrence takes only polynomially many distinct parameter values.** Those values are the **states** — the cells of the table. Write down in one sentence what a cell means ("`T[i][j]` = can some subset of the first $i$ items sum to exactly $j$?"). If you can't, the recurrence isn't clear yet. This is where efficiency lives.
3. **Choose an evaluation order** so that every subproblem is solved before it's needed.

Then, optionally:

- **Compress the table.** Only after the full table is correct, check which cells the recurrence reads. If row $i$ needs only row $i - 1$, keep one or two rows.
- **Reconstruct the solution** itself (not just its cost) by recording which choice won at each state, then following those choices backward.

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
    n = len(nums)
    best = [0] * (n + 1)                # best[i] = max loot from the first i houses
    for i in range(1, n + 1):
        leave = best[i - 1]                                    # house i not robbed
        take = (best[i - 2] if i >= 2 else 0) + nums[i - 1]    # robbed: house i-1 must be skipped
        best[i] = max(leave, take)
    return best[n]
```

`best[i]` reads only the previous two entries, so, as with Fibonacci, two variables suffice:

```python
def rob(nums: list[int]) -> int:
    back2 = back1 = 0                   # best[i-2], best[i-1]
    for x in nums:
        back2, back1 = back1, max(back1, back2 + x)
    return back1
```

That "take it or leave it" split — the item is either in the solution or not — is the most common recurrence pattern in all of DP. **Climbing Stairs** (LC 70) is Fibonacci; **Maximum Subarray** (LC 53) uses "best ending here" (see [Kadane's algorithm](04_two_pointers_sliding_window.md#largest-subrange-three-algorithms-for-one-problem)).

### Word Break (LC 139)

Can the string be split into dictionary words? `ok[i]` is true if the prefix `s[:i]` can be split. It can be exactly when some split point $j < i$ has `ok[j]` true and `s[j:i]` is a word:

```python
def word_break(s: str, words: list[str]) -> bool:
    dictionary = set(words)
    longest = max(map(len, dictionary), default=0)
    ok = [True] + [False] * len(s)      # ok[i] = can s[:i] be split into words? (empty prefix: yes)
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
    length = [1] * n                    # length[i] = longest increasing subsequence ending at nums[i]
    prev = [-1] * n                     # prev[i] = index of the element before nums[i] in it
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

$O(n^2)$ time. Notice the move we made — the obvious quantity wasn't enough, so we asked for more information about every prefix. It's the same "strengthen the hypothesis" move as in [tree recursion](11_trees.md#strengthening-the-hypothesis), and it's how most DP states are discovered.

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
    # D[i][j] = edit distance between p[:i] and t[:j]
    D = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        D[i][0] = i                                   # delete all of p[:i]
    for j in range(n + 1):
        D[0][j] = j                                   # insert all of t[:j]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            D[i][j] = min(
                D[i - 1][j - 1] + (p[i - 1] != t[j - 1]),   # match / substitute
                D[i][j - 1] + 1,                            # insert t[j-1]
                D[i - 1][j] + 1,                            # delete p[i-1]
            )
    return D[m][n]
```

$O(mn)$ time and space. To reconstruct the actual edits, start at `D[m][n]` and step back to whichever of the three neighbors produced its value.

**Compressing.** Row `i` reads only row `i - 1` (`D[i-1][j-1]`, `D[i-1][j]`) and the cell to its left in row `i` itself. So keep two rows, `prev` for row `i - 1` and `curr` for row `i`, giving $O(n)$ space (but no reconstruction):

```python
def min_distance(p: str, t: str) -> int:
    m, n = len(p), len(t)
    prev = list(range(n + 1))                     # row 0: D[0][j] = j
    for i in range(1, m + 1):
        curr = [i] + [0] * n                      # D[i][0] = i
        for j in range(1, n + 1):
            curr[j] = min(
                prev[j - 1] + (p[i - 1] != t[j - 1]),
                curr[j - 1] + 1,
                prev[j] + 1,
            )
        prev = curr
    return prev[n]
```

### One routine, many problems

Small changes to the costs, the base cases, or the goal cell turn edit distance into other classic problems:

- **Longest Common Subsequence** (LC 1143): forbid substitution. Then the only way to handle mismatched characters is to delete them, so the cheapest alignment keeps the most matches. Directly:

```python
def longest_common_subsequence(a: str, b: str) -> int:
    m, n = len(a), len(b)
    # L[i][j] = length of the LCS of a[:i] and b[:j]; row/column 0 = empty prefix, LCS 0
    L = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1           # both last characters join the LCS
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1]) # drop a's last or b's last
    return L[m][n]
```

The same two-row compression as edit distance brings the space down to $O(n)$.

- **Delete Operation for Two Strings** (LC 583): $|a| + |b| - 2 \cdot \text{LCS}$.
- **Longest increasing subsequence** is the LCS of the sequence with its own sorted, de-duplicated version.
- **Approximate substring matching**: to find where pattern $P$ best matches *anywhere* in text $T$, make skipping a prefix of $T$ free ($D[0][j] = 0$) and take the best cell in the last row. Without this change, the "best" match of a short pattern in a long text is dominated by the cost of deleting everything else.
- **Distinct Subsequences** (LC 115), **Interleaving String** (LC 97), **Regular Expression Matching** (LC 10), and **Wildcard Matching** (LC 44) are all two-index DPs with the same "what happens to the last characters?" derivation.

!!! tip "Take-Home Lesson"
    For optimization problems on objects with a natural **left-to-right order** — characters of a string, elements of a sequence, points along a line, leaves of a tree — dynamic programming very likely gives an efficient algorithm. The states are simply positions in the order.

---

## Subset Sum and Knapsack

All of these problems have the same structure: go through the items one at a time and decide, for each one, **take it or leave it**. So the state needs two indices:

- **how many items have been decided**: a prefix, as in every sequence DP;
- **how much of the budget is left**: the sum still to make, or the capacity still free.

The second index is a *value*, not a position. That's what's new here.

### Subset sum: the full table

**Problem.** Given positive integers $s_1, \ldots, s_n$ and a target $k$, is there a subset summing to exactly $k$?

**State.** $T[i][j]$ = *can some subset of the first $i$ items sum to exactly $j$?* We need it for every $0 \le i \le n$ and every $0 \le j \le k$, and the answer is $T[n][k]$.

Why every $j$, and not just $k$? Taking an item changes the target. If we take $s_i$, the other items must make $j - s_i$, so we need answers for smaller targets too. As with LIS, the obvious question isn't enough, so we ask a more general one.

**Recurrence.** Look at the last item, $s_i$. A subset of the first $i$ items that sums to $j$ either:

- **leaves** $s_i$: then it's a subset of the first $i - 1$ items summing to $j$, so $T[i-1][j]$;
- **takes** $s_i$: then the rest of it is a subset of the first $i - 1$ items summing to $j - s_i$, so $T[i-1][j - s_i]$ (possible only if $s_i \le j$).

$$T[i][j] = T[i-1][j] \ \lor\ T[i-1][j - s_i]$$

**Base case.** With no items, the only subset is the empty one, which sums to 0: $T[0][0] = \text{true}$, and $T[0][j] = \text{false}$ for $j > 0$.

**Example.** Items $(2, 3, 5)$, $k = 8$ (T = reachable):

| | $j$=0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| $i = 0$: no items | T | | | | | | | | |
| $i = 1$: + 2 | T | | T | | | | | | |
| $i = 2$: + 3 | T | | T | T | | T | | | |
| $i = 3$: + 5 | T | | T | T | | T | | T | T |

Each row is the row above, plus the row above shifted right by $s_i$. $T[3][8]$ is true because $T[2][3]$ is true: take the 5, and $\{2, 3\}$ can make the remaining 3.

```python
def subset_sum(nums: list[int], k: int) -> bool:
    n = len(nums)
    # T[i][j] = can some subset of nums[:i] sum to exactly j?
    T = [[False] * (k + 1) for _ in range(n + 1)]
    T[0][0] = True                                      # empty subset makes 0
    for i in range(1, n + 1):
        x = nums[i - 1]                                 # the i-th item
        for j in range(k + 1):
            T[i][j] = T[i - 1][j]                       # leave x
            if j >= x and T[i - 1][j - x]:
                T[i][j] = True                          # take x
    return T[n][k]
```

That's $O(nk)$ time for $n$ items and target $k$. This is polynomial in the *value* $k$, not in the number of bits needed to write $k$ down. It's fast when $k$ is modest, but with $k \approx 10^{18}$ the table is useless. (Subset sum is NP-complete; DP doesn't contradict that.)

### Partition Equal Subset Sum (LC 416)

**Problem.** Can `nums` be split into two groups with equal sums?

This is subset sum with $k = \text{total} / 2$. Why is finding *one* group of that sum enough? Because every element goes into exactly one of the two groups. If group $A$ sums to $a$, the other group is everything else, and it sums to $\text{total} - a$. So:

- If the two groups are equal, then $a = \text{total} - a$, so $a = \text{total}/2$. A valid split always contains a subset summing to $\text{total}/2$.
- If some subset $A$ sums to $\text{total}/2$, put every other element in $B$. Then $B$ sums to $\text{total} - \text{total}/2 = \text{total}/2$ with no extra work.

Finding one half is enough, because its complement is the other half. If the total is odd, no integer half exists.

```python
def can_partition(nums: list[int]) -> bool:
    total = sum(nums)
    if total % 2:
        return False                    # odd total: two equal integer halves are impossible
    return subset_sum(nums, total // 2) # the complement of that subset is the other half
```

### Compressing to one array: why downward

Row $i$ reads only row $i - 1$, so we can keep a single array, `reachable[j]` = *can some subset of the items seen so far sum to $j$?*, and overwrite it in place, one item at a time.

There's a catch. The take branch reads `T[i-1][j - x]`, a cell **to the left** in the **previous** row. If `j` goes upward, then by the time we reach `j`, the cell `j - x` has already been overwritten with row $i$. It may already include $x$, so $x$ gets used twice.

Take `nums = [3]`, `k = 6`. Going upward, `reachable[3]` becomes true (0 + 3). Then `reachable[6]` reads `reachable[3]` and becomes true, meaning "6 = 3 + 3", which uses the single 3 twice. Going **downward**, `j = 6` is computed while `reachable[3]` still holds the previous row (false), and only then does `j = 3` become true. That's correct.

```python
def can_partition(nums: list[int]) -> bool:
    total = sum(nums)
    if total % 2:
        return False
    target = total // 2
    reachable = [True] + [False] * target       # reachable[j] = some subset of the items so far sums to j
    for x in nums:
        for j in range(target, x - 1, -1):      # downward: reachable[j - x] is still the previous row
            reachable[j] = reachable[j] or reachable[j - x]
    return reachable[target]
```

The loop stops at `x`: for `j < x` only "leave" is possible, so `T[i][j] = T[i-1][j]`, and the cell is left unchanged.

### 0/1 knapsack

Items have weights $w_i$ and values $v_i$. Each can be used **at most once**. Maximize the total value with total weight at most $C$.

**State.** $\text{best}[i][c]$ = the largest value from a subset of the first $i$ items with total weight $\le c$.

**Recurrence.** It's the same take-or-leave split, but now we compare values (max) instead of asking "is it possible?" (or):

$$\text{best}[i][c] = \max\big(\text{best}[i-1][c],\ \text{best}[i-1][c - w_i] + v_i\big) \qquad (\text{take only if } w_i \le c)$$

**Base case.** $\text{best}[0][c] = 0$ for every $c$: no items, no value. (Because the state says weight $\le c$, not $= c$, every capacity is achievable with the empty set.)

```python
def knapsack(weights: list[int], values: list[int], C: int) -> int:
    n = len(weights)
    # best[i][c] = max value from a subset of the first i items with total weight <= c
    best = [[0] * (C + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        w, v = weights[i - 1], values[i - 1]
        for c in range(C + 1):
            best[i][c] = best[i - 1][c]                                 # leave item i
            if c >= w:
                best[i][c] = max(best[i][c], best[i - 1][c - w] + v)    # take item i
    return best[n][C]
```

The take branch reads row $i - 1$, exactly as in subset sum, so the one-array version also goes **downward**: `for c in range(C, w - 1, -1): best[c] = max(best[c], best[c - w] + v)`. Subset sum is the special case where each item's value equals its weight, and we ask whether $\text{best}[n][k] = k$.

### Unbounded items: coin change (LC 322)

Now each coin can be used **any number of times**. We want the fewest coins summing to exactly `amount`.

**State.** $\text{fewest}[i][s]$ = the fewest coins summing to exactly $s$, using only the first $i$ coin types ($\infty$ if impossible).

**Recurrence.** Take or leave coin type $i$, with value $c_i$:

- **leave**: we never use $c_i$ again, so $\text{fewest}[i-1][s]$;
- **take one copy**: and $c_i$ is *still available* for the rest, so $\text{fewest}[\mathbf{i}][s - c_i] + 1$.

$$\text{fewest}[i][s] = \min\big(\text{fewest}[i-1][s],\ \text{fewest}[i][s - c_i] + 1\big)$$

The only difference from 0/1 is the row index in the take branch: **$i$ instead of $i - 1$**. Taking a coin doesn't remove it from the menu.

**Base case.** $\text{fewest}[0][0] = 0$ and $\text{fewest}[0][s] = \infty$ for $s > 0$. Here the sum must be *exact*, so unreachable states are $\infty$, not 0.

```python
def coin_change(coins: list[int], amount: int) -> int:
    INF = float("inf")
    n = len(coins)
    # fewest[i][s] = fewest coins summing to exactly s, using only the first i coin types
    fewest = [[INF] * (amount + 1) for _ in range(n + 1)]
    fewest[0][0] = 0
    for i in range(1, n + 1):
        c = coins[i - 1]
        for s in range(amount + 1):
            fewest[i][s] = fewest[i - 1][s]                             # never use c
            if s >= c:
                fewest[i][s] = min(fewest[i][s], fewest[i][s - c] + 1)  # one more c; row i: c still allowed
    return fewest[n][amount] if fewest[n][amount] != INF else -1
```

**Compressing.** The take branch now reads the **current** row at `s - c`. In a single array, iterating **upward** gives exactly that, because `fewest[s - c]` has already been updated for coin `c`. So the loop direction isn't a trick to memorize. It follows from which row the recurrence reads:

```python
def coin_change(coins: list[int], amount: int) -> int:
    INF = amount + 1                            # more coins than any real answer needs
    fewest = [0] + [INF] * amount               # fewest[s] = fewest coins (types so far) making s
    for c in coins:
        for s in range(c, amount + 1):          # upward: fewest[s - c] is already row i
            fewest[s] = min(fewest[s], fewest[s - c] + 1)
    return fewest[amount] if fewest[amount] != INF else -1
```

Here greedy fails (coins $\{1, 6, 10\}$, amount 12; see [Greedy](15_greedy.md#when-greedy-fails)), but DP is always right, because it considers every possibility for each coin.

### Counting: combinations vs. permutations

When **counting** the ways to reach a total, the right state depends on whether order matters.

**Combinations (LC 518)**, where $\{1, 2\}$ and $\{2, 1\}$ are the same way. Use the coin-change state: $\text{ways}[i][s]$ = the number of ways to make $s$ using only the first $i$ coin types. Every way either uses no $c_i$ at all, or uses at least one $c_i$ (remove one copy, and the rest still uses types $1..i$):

$$\text{ways}[i][s] = \text{ways}[i-1][s] + \text{ways}[i][s - c_i]$$

Coin types are decided in a fixed order ($c_1$ first, then $c_2$, ...), so each multiset of coins is counted exactly once. In one array this becomes coins outer, sums upward, as in coin change.

**Permutations (LC 377)**, where $(1, 2)$ and $(2, 1)$ are different. Now there is no "first $i$ items" index, because any item can come at any position. The state is just $\text{ways}[s]$ = the number of ordered sequences summing to $s$. Split on the **last element** $x$: the sequence is some sequence summing to $s - x$, followed by $x$.

$$\text{ways}[s] = \sum_{x \le s} \text{ways}[s - x], \qquad \text{ways}[0] = 1 \text{ (the empty sequence)}$$

To compute $\text{ways}[s]$ we need every smaller total, with every item allowed, so totals go in the outer loop. This is Climbing Stairs with arbitrary step sizes. It's a genuinely 1-D state, not a compressed table.

```python
def count_combinations(coins: list[int], amount: int) -> int:
    """LC 518. ways[s] = ways to make s with the coin types seen so far."""
    ways = [1] + [0] * amount
    for c in coins:                             # coin types outer: the table's row index
        for s in range(c, amount + 1):          # upward: c may be reused
            ways[s] += ways[s - c]
    return ways[amount]


def count_sequences(nums: list[int], target: int) -> int:
    """LC 377. ways[s] = ordered sequences summing to s."""
    ways = [1] + [0] * target
    for s in range(1, target + 1):              # totals outer
        for x in nums:                          # every choice of last element
            if x <= s:
                ways[s] += ways[s - x]
    return ways[target]
```

| Variant | State | Take branch reads | One-array loops |
|---|---|---|---|
| 0/1: subset sum, knapsack | first $i$ items, sum/capacity | row $i - 1$ | items outer, capacity **downward** |
| Unbounded: coin change | first $i$ item types, sum | row $i$ | items outer, capacity **upward** |
| Count combinations | first $i$ item types, sum | row $i$ | items outer, upward |
| Count sequences | sum only; split on the last element | — | totals outer, items inner |

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

This is **Split Array Largest Sum** (LC 410). The [binary search on the answer](03_binary_search.md#split-array-largest-sum-lc-410) solution is faster, $O(n \log \sum s)$ — but the DP generalizes to costs where no greedy feasibility check exists.

---

## Interval DP

Some problems are naturally about **substrings or subarrays** $[i, j]$, and the answer for an interval combines answers for smaller intervals inside it. Evaluate in order of increasing **length**, so that every smaller interval is ready.

**Longest Palindromic Subsequence** (LC 516): if the end characters match, they wrap a palindrome inside; otherwise drop one end.

```python
def longest_palindrome_subseq(s: str) -> int:
    n = len(s)
    dp = [[0] * n for _ in range(n)]                    # dp[i][j] = longest palindromic subsequence of s[i..j]
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

When the decision at each step depends on a small amount of **mode** — holding a stock or not, in cooldown or not — make the mode part of the state. **Best Time to Buy and Sell Stock with Cooldown** (LC 309) has three modes, so the state is (day $d$, mode), and each cell is the best profit at the end of day $d$ in that mode:

- $\text{hold}[d]$: holding a stock. Either we already held it, or we bought today, which needs the "free" mode yesterday:
  $\text{hold}[d] = \max(\text{hold}[d-1],\ \text{rest}[d-1] - p_d)$
- $\text{sold}[d]$: sold today, so tomorrow is cooldown. We must have held yesterday:
  $\text{sold}[d] = \text{hold}[d-1] + p_d$
- $\text{rest}[d]$: not holding and free to buy tomorrow. Either we were already free, or yesterday's sale finished its cooldown:
  $\text{rest}[d] = \max(\text{rest}[d-1],\ \text{sold}[d-1])$

Before day 1, holding is impossible ($-\infty$) and the other two modes have profit 0. Day $d$ reads only day $d - 1$, so three variables replace the three columns:

```python
def max_profit_cooldown(prices: list[int]) -> int:
    hold, sold, rest = float("-inf"), 0, 0      # hold[d-1], sold[d-1], rest[d-1]
    for p in prices:
        hold, sold, rest = max(hold, rest - p), hold + p, max(rest, sold)
    return max(sold, rest)
```

The tuple assignment matters: every right-hand side must read *yesterday's* values. The other stock problems (LC 123, 188, 714) add a transaction counter or a fee to the same machine.

---

## Beyond Sequences: Trees and Subsets

**On trees**, the natural order is bottom-up: a node's answer combines its children's. **House Robber III** (LC 337) returns a pair per node — the best total with the node robbed, and without it — which is DP with the state stored in the recursion's return value (see [Trees](11_trees.md#strengthening-the-hypothesis)).

**On subsets**, when there's no natural order, the state must remember *which* items have been used. Consider finding the shortest route visiting every city exactly once (the traveling salesman problem). A recurrence over "the path so far" is correct but has $n!$ states — it's just backtracking. But the future doesn't depend on the **order** of the cities visited, only on **which** cities were visited and **where you are now**. That gives $2^n \cdot n$ states:

$$\text{best}[S][v] = \min_{u \in S \setminus \{v\}} \big(\text{best}[S \setminus \{v\}][u] + d(u, v)\big)$$

```python
def shortest_tour(dist: list[list[int]]) -> int:
    """Held–Karp: shortest cycle through all cities, starting and ending at city 0."""
    n = len(dist)
    INF = float("inf")
    best = [[INF] * n for _ in range(1 << n)]           # best[S][v] = shortest path from 0 visiting exactly S, ending at v
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

$O(n^2 2^n)$ — feasible for $n \approx 20$, where $n!$ would be hopeless. Subsets as integers are covered in [Bit Manipulation](05_bit_manipulation.md#bit-vectors-integers-as-sets).

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
