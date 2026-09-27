# Backtracking

Some problems have no clever shortcut: to find all valid arrangements, or the best one, you must in principle consider every candidate. **Backtracking** is the systematic way to do that — to enumerate every configuration of a search space exactly once, while abandoning partial configurations the moment they can't possibly succeed.

Exhaustive search has a bad reputation, but surprisingly large problems yield to it, and it has one great virtue: it is *obviously correct*. If you've tried every possibility, you haven't missed the answer. The craft lies in two places: generating each candidate **exactly once** (no repeats, no omissions), and **pruning** the search so that you only look at candidates that matter.

---

## How Big Is Exhaustive?

It's important to have a feel for how big — and how small — the search spaces are. Python can explore on the order of a million simple search states per second:

| Search space | Size | Feasible up to about |
|---|---|---|
| All subsets of $n$ items | $2^n$ | $n \approx 20$ ($10^6$) |
| All permutations of $n$ items | $n!$ | $n \approx 10$ ($3.6 \times 10^6$) |
| All $k$-subsets | $\binom{n}{k}$ | depends; $\binom{30}{5} \approx 1.4 \times 10^5$ |
| All strings of length $n$ over $\Sigma$ | $\lvert\Sigma\rvert^n$ | $4^{10} \approx 10^6$ |

These limits are for *unpruned* search. Good pruning pushes them much further — sometimes by factors of thousands — because it cuts off whole subtrees at once. When a LeetCode problem has $n \le 15$ or so, it is usually telling you that exponential search is expected.

---

## The Backtracking Framework

Model a solution as a vector $a = (a_1, a_2, \ldots, a_n)$, built one position at a time. For subsets, $a_i$ might be "is item $i$ included?"; for permutations, $a_i$ is the item in position $i$; for a path in a graph, $a_i$ is the $i$-th vertex.

At each step, extend the partial solution $(a_1, \ldots, a_k)$ by one element. If it's complete, process it; otherwise, consider every legal candidate for position $k + 1$ in turn. The partial solutions form a **tree**, and backtracking is simply a **depth-first search** of that implicit tree. DFS (rather than BFS) is the right choice because it only needs to remember the current root-to-node path — space proportional to the *depth* of the tree, not its enormous width.

Every backtracking algorithm is the same skeleton with five problem-specific pieces:

```python
def backtrack(partial: list, state) -> None:
    if is_solution(partial, state):              # 1. is the partial solution complete?
        process_solution(partial, state)         # 2. record / count / print it
        return
    for candidate in candidates(partial, state): # 3. legal choices for the next position
        make_move(partial, candidate, state)     # 4. apply the choice
        backtrack(partial, state)
        unmake_move(partial, candidate, state)   # 5. undo it exactly
```

The `make_move` / `unmake_move` pair is what makes backtracking efficient. Rather than copying the whole state at each node, you mutate one shared state and **undo** each change on the way back up. The undo must restore the state *exactly*; most backtracking bugs are an incomplete undo.

!!! tip "Take-Home Lesson"
    Backtracking guarantees correctness by enumerating all possibilities, and efficiency by never visiting a state twice. For each new problem, you only need to decide what a partial solution looks like, what the candidates for the next position are, and how to apply and undo a move.

---

## Generating the Basic Objects

Almost every backtracking problem is a variation on generating subsets, permutations, or combinations. Learn these three cold.

### Subsets (LC 78)

**View 1 — include or exclude.** Position $i$ of the solution vector is a yes/no decision about item $i$. The search tree is a complete binary tree with $2^n$ leaves, one per subset.

```python
def subsets(nums: list[int]) -> list[list[int]]:
    result: list[list[int]] = []
    chosen: list[int] = []

    def decide(i: int) -> None:
        if i == len(nums):
            result.append(chosen[:])             # copy: chosen keeps changing
            return
        decide(i + 1)                            # exclude nums[i]
        chosen.append(nums[i])                   # include nums[i]
        decide(i + 1)
        chosen.pop()

    decide(0)
    return result
```

**View 2 — choose the next element.** Every node of the tree is itself a subset; its children add one element *later* than any already chosen. Starting each loop at `start` is what prevents generating `{2, 1}` after `{1, 2}`.

```python
def subsets_v2(nums: list[int]) -> list[list[int]]:
    result: list[list[int]] = []
    chosen: list[int] = []

    def extend(start: int) -> None:
        result.append(chosen[:])                 # every node is a valid subset
        for i in range(start, len(nums)):
            chosen.append(nums[i])
            extend(i + 1)
            chosen.pop()

    extend(0)
    return result
```

Both are $O(n \cdot 2^n)$: $2^n$ subsets, each copied in $O(n)$. (Subsets can also be generated without recursion by binary counting; see [Bit Manipulation](04_bit_manipulation.md#generating-subsets).) View 2 generalizes more easily, so it's the one to reach for when constraints are added.

### Permutations (LC 46)

Position $k$ can hold any element not already used. A `used` array makes "not already used" an $O(1)$ check:

```python
def permutations(nums: list[int]) -> list[list[int]]:
    result: list[list[int]] = []
    perm: list[int] = []
    used = [False] * len(nums)

    def place() -> None:
        if len(perm) == len(nums):
            result.append(perm[:])
            return
        for i, x in enumerate(nums):
            if not used[i]:
                used[i] = True                   # make move
                perm.append(x)
                place()
                perm.pop()                       # unmake move
                used[i] = False

    place()
    return result
```

$O(n \cdot n!)$. There are $n!$ leaves, and the tree has fewer than $e \cdot n!$ nodes in total, so the internal nodes don't change the bound.

### Combinations: $k$-subsets (LC 77)

Choose $k$ of the numbers $1 \dots n$. It's View 2 of subsets, recording only nodes at depth $k$ — plus a cheap but valuable **prune**: if there aren't enough numbers left to reach size $k$, stop.

```python
def combine(n: int, k: int) -> list[list[int]]:
    result: list[list[int]] = []
    chosen: list[int] = []

    def extend(start: int) -> None:
        if len(chosen) == k:
            result.append(chosen[:])
            return
        need = k - len(chosen)
        for x in range(start, n - need + 2):     # leave room for the remaining picks
            chosen.append(x)
            extend(x + 1)
            chosen.pop()

    extend(1)
    return result
```

### Paths in a graph (LC 797)

A path is a vector of vertices where each $a_{k+1}$ is a neighbor of $a_k$ not already on the path. In a DAG, "not already on the path" is automatic:

```python
def all_paths_source_target(graph: list[list[int]]) -> list[list[int]]:
    target = len(graph) - 1
    result: list[list[int]] = []
    path = [0]

    def walk(u: int) -> None:
        if u == target:
            result.append(path[:])
            return
        for v in graph[u]:
            path.append(v)
            walk(v)
            path.pop()

    walk(0)
    return result
```

The number of paths can be exponential in the size of the graph, so the running time is too — output size alone forces it.

---

## Each Configuration Exactly Once: Handling Duplicates

When the input contains duplicates, the generators above produce duplicate outputs: `[1, 2a]` and `[1, 2b]` look identical. Generating everything and deduplicating with a set works but wastes time. It's better to never generate the duplicates at all.

**The rule:** sort the input so equal values are adjacent. At any single node of the search tree, try each **distinct value** as the next choice only once.

**Subsets with duplicates** (LC 90) — in the choose-next-element tree, siblings are the choices at the same node; skip a value equal to the previous sibling:

```python
def subsets_with_dup(nums: list[int]) -> list[list[int]]:
    nums = sorted(nums)
    result: list[list[int]] = []
    chosen: list[int] = []

    def extend(start: int) -> None:
        result.append(chosen[:])
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:
                continue                         # same value already tried at this node
            chosen.append(nums[i])
            extend(i + 1)
            chosen.pop()

    extend(0)
    return result
```

Note the condition `i > start`, not `i > 0`. Taking a second copy of a value **deeper** in the tree (as a child of the first copy) is fine — that's how `[2, 2]` gets generated. Only sibling repeats are redundant.

**Permutations with duplicates** (LC 47) — among equal values, insist that they are used in their original left-to-right order. A copy may be placed only if the previous equal copy has already been placed:

```python
def permute_unique(nums: list[int]) -> list[list[int]]:
    nums = sorted(nums)
    result: list[list[int]] = []
    perm: list[int] = []
    used = [False] * len(nums)

    def place() -> None:
        if len(perm) == len(nums):
            result.append(perm[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                continue                         # use equal copies left to right only
            used[i] = True
            perm.append(nums[i])
            place()
            perm.pop()
            used[i] = False

    place()
    return result
```

**Combination Sum II** (LC 40) combines both ideas: sibling-skip for duplicates, and each element used at most once.

---

## Pruning: Cutting the Tree Early

Generating all $n!$ tours of a traveling salesman instance and then evaluating each one is wasteful. If the tour so far is already more expensive than the best complete tour found, **no extension can help** — so stop exploring this branch. Checking constraints on *partial* solutions, rather than waiting for complete ones, is the single most important technique in exhaustive search.

!!! tip "Take-Home Lesson"
    Clever pruning can make short work of surprisingly hard search problems. Proper pruning has a far greater effect on search time than any other factor — the data structures, the language, or the speed of the machine.

There are three main kinds of pruning.

**1. Feasibility pruning:** abandon a partial solution as soon as it violates a constraint or can no longer be completed. In **Combination Sum** (LC 39), sort the candidates; once a candidate overshoots the remaining target, every later (larger) candidate will too, so `break` rather than `continue`:

```python
def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    candidates = sorted(candidates)
    result: list[list[int]] = []
    chosen: list[int] = []

    def extend(start: int, remaining: int) -> None:
        if remaining == 0:
            result.append(chosen[:])
            return
        for i in range(start, len(candidates)):
            c = candidates[i]
            if c > remaining:
                break                            # sorted: everything after is too big as well
            chosen.append(c)
            extend(i, remaining - c)             # i, not i + 1: reuse allowed
            chosen.pop()

    extend(0, target)
    return result
```

**Generate Parentheses** (LC 22) is pure feasibility pruning: never place more than $n$ opening brackets, and never close more than you've opened. Every leaf reached is valid, so no work is wasted on invalid strings at all.

**2. Bounding (branch and bound):** in optimization problems, abandon a partial solution when even an optimistic estimate of its best completion can't beat the best solution found so far.

**3. Symmetry:** if two branches are guaranteed to lead to equivalent results, explore only one. For a TSP tour, rotations of the same cycle are the same tour, so fix the starting city: a factor of $n$ saved for free.

### A worked example: Partition to K Equal Sum Subsets (LC 698)

Can the numbers be split into $k$ groups with equal sums? Each group must sum to `target = total / k`. The naive search assigns each number to one of $k$ buckets — $k^n$ possibilities. Three prunings make it fast:

```python
def can_partition_k_subsets(nums: list[int], k: int) -> bool:
    total = sum(nums)
    if total % k:
        return False
    target = total // k
    nums = sorted(nums, reverse=True)            # (a) big items first: fail fast
    if nums[0] > target:
        return False
    buckets = [0] * k

    def place(i: int) -> bool:
        if i == len(nums):
            return True                          # all placed; every bucket must equal target
        seen: set[int] = set()
        for b in range(k):
            if buckets[b] + nums[i] > target or buckets[b] in seen:
                continue                         # (b) infeasible, or (c) symmetric to a tried bucket
            seen.add(buckets[b])
            buckets[b] += nums[i]
            if place(i + 1):
                return True
            buckets[b] -= nums[i]
        return False

    return place(0)
```

- **(a) Order the choices**: placing large numbers first makes buckets overflow early, near the root of the tree, where pruning saves the most.
- **(b) Feasibility**: never overfill a bucket.
- **(c) Symmetry**: two buckets with the same current sum are interchangeable — putting `nums[i]` into either leads to equivalent searches. Try only one. In particular, all the empty buckets are the same bucket.

---

## Constraint Satisfaction

In constraint satisfaction problems, every position has a domain of values and the constraints forbid certain combinations. Backtracking assigns positions one at a time and checks constraints incrementally — the `make_move` step also updates whatever data structure answers "is this value still allowed?" in $O(1)$.

### N-Queens (LC 51)

Place $n$ queens so that none attack each other. One queen per row, so the solution vector gives each row's column. A queen at $(r, c)$ occupies column $c$, "diagonal" $r - c$, and "anti-diagonal" $r + c$; three sets make each safety check $O(1)$:

```python
def solve_n_queens(n: int) -> list[list[str]]:
    result: list[list[str]] = []
    cols: set[int] = set()
    diag: set[int] = set()
    anti: set[int] = set()
    queens: list[int] = []                       # queens[r] = column of the queen in row r

    def place(r: int) -> None:
        if r == n:
            result.append(["." * c + "Q" + "." * (n - c - 1) for c in queens])
            return
        for c in range(n):
            if c in cols or r - c in diag or r + c in anti:
                continue
            cols.add(c); diag.add(r - c); anti.add(r + c); queens.append(c)
            place(r + 1)
            cols.remove(c); diag.remove(r - c); anti.remove(r + c); queens.pop()

    place(0)
    return result
```

### Sudoku (LC 37): choose the most constrained cell

A natural Sudoku solver fills empty cells in reading order, trying each digit not already in the cell's row, column, or box. It works — but experiments show that for hard puzzles it can take an extremely long time. Two changes make it orders of magnitude faster:

- **Most constrained first.** Instead of the next cell in reading order, fill the empty cell with the **fewest** remaining candidates. A cell with one candidate is a forced move and costs nothing; a cell with two candidates is a coin flip rather than a 1-in-9 guess. Since the branching factors multiply down the tree, reducing the average branching from 3 to 2 over 20 cells cuts the search from $3^{20} \approx 3.5 \times 10^9$ to $2^{20} \approx 10^6$ — a factor of over 3,000.
- **Look ahead.** If any empty cell has **zero** candidates left, the current partial solution is dead — backtrack now, instead of discovering it many moves later. Most-constrained selection gets this for free: the cell with zero candidates is the one it picks.

```python
def solve_sudoku(board: list[list[str]]) -> None:
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    empty = []
    for r in range(9):
        for c in range(9):
            if board[r][c] == ".":
                empty.append((r, c))
            else:
                d = board[r][c]
                rows[r].add(d); cols[c].add(d); boxes[r // 3 * 3 + c // 3].add(d)

    def candidates(r: int, c: int) -> set[str]:
        return set("123456789") - rows[r] - cols[c] - boxes[r // 3 * 3 + c // 3]

    def solve() -> bool:
        if not empty:
            return True
        # most constrained cell: fewest candidates (0 candidates => dead end immediately)
        i = min(range(len(empty)), key=lambda j: len(candidates(*empty[j])))
        r, c = empty[i]
        options = candidates(r, c)
        empty[i] = empty[-1]
        empty.pop()
        for d in options:
            board[r][c] = d
            rows[r].add(d); cols[c].add(d); boxes[r // 3 * 3 + c // 3].add(d)
            if solve():
                return True
            rows[r].remove(d); cols[c].remove(d); boxes[r // 3 * 3 + c // 3].remove(d)
        board[r][c] = "."
        empty.append((r, c))                     # restore the list of empty cells
        empty[i], empty[-1] = empty[-1], empty[i]
        return False

    solve()
```

Choosing the most constrained cell looks like it only *reorders* the work, but it changes the shape of the search tree: fixing constrained positions first adds constraints that shrink the branching everywhere below. The same heuristic — **fail first** — applies to any constraint problem: graph coloring, scheduling, crossword filling.

!!! tip "Take-Home Lesson"
    The order in which you make decisions matters enormously. Make the most constrained decision first, and check for dead ends as early as possible. Both reduce the branching factor, and the branching factor is exponentiated by the depth of the search.

---

## Searching Grids and Strings

### Word Search (LC 79)

Trace a word through adjacent cells without reusing a cell. The partial solution is the path so far; the candidates are unvisited neighbors holding the next letter. Marking the cell in place and restoring it afterward is the make/unmake pair:

```python
def exist(board: list[list[str]], word: str) -> bool:
    rows, cols = len(board), len(board[0])

    def match(r: int, c: int, i: int) -> bool:
        if board[r][c] != word[i]:
            return False
        if i == len(word) - 1:
            return True
        board[r][c] = "#"                        # make move: mark used
        found = any(
            match(nr, nc, i + 1)
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1))
            if 0 <= nr < rows and 0 <= nc < cols
        )
        board[r][c] = word[i]                    # unmake move
        return found

    return any(match(r, c, 0) for r in range(rows) for c in range(cols))
```

A cheap global prune before searching: if the board doesn't contain enough copies of each letter in the word, return `False` immediately. For many words at once, drive the search with a trie (Word Search II; see [Trie & Union Find](12_trie_union_find.md#word-search-ii-lc-212-walking-a-trie-and-a-grid-together)).

### Partitioning a string (LC 131)

Split a string into palindromes, returning all ways. The solution vector is the list of pieces; the candidates for the next piece are the palindromic prefixes of what remains.

```python
def partition(s: str) -> list[list[str]]:
    n = len(s)
    # is_pal[i][j]: s[i..j] is a palindrome — precomputed so each check is O(1)
    is_pal = [[False] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            is_pal[i][j] = s[i] == s[j] and (j - i < 2 or is_pal[i + 1][j - 1])

    result: list[list[str]] = []
    pieces: list[str] = []

    def cut(start: int) -> None:
        if start == n:
            result.append(pieces[:])
            return
        for end in range(start, n):
            if is_pal[start][end]:
                pieces.append(s[start:end + 1])
                cut(end + 1)
                pieces.pop()

    cut(0)
    return result
```

Precomputing the palindrome table is itself a small dynamic program; it turns an $O(n)$ check at each node into $O(1)$. Restore IP Addresses (LC 93) and Word Break II (LC 140) have the same shape.

---

## Beyond Depth-First: Best-First Search

Backtracking explores the tree depth-first, in whatever order the candidates happen to come. For optimization problems, it can pay to always expand the **most promising** partial solution next, keeping partial solutions in a priority queue ordered by an estimate of their final cost. That's **best-first search**.

Its most famous form, **A\***, orders partial solutions by *cost so far + an estimate of the remaining cost*. If the estimate never overestimates (it is a lower bound), the first complete solution popped is optimal — and a tight estimate lets the search ignore most of the tree. Dijkstra's algorithm is A\* with an estimate of zero. The price is memory: best-first search stores the whole frontier, while depth-first backtracking stores only one path.

---

## When Backtracking Should Become DP

If the same sub-search is reached by different paths — for example, "can the rest of the string starting at position $i$ be segmented into words?" in Word Break — backtracking recomputes it every time. When the answer to a sub-search depends only on a small **state** (here, just $i$), cache it. That's memoization, and it turns exponential backtracking into polynomial dynamic programming. The signal: the subproblem's answer doesn't depend on the choices that led to it. See [Dynamic Programming](15_dynamic_programming.md).

---

## Complexity Summary

| Problem | Search space | Time |
|---|---|---|
| Subsets | $2^n$ leaves | $O(n \cdot 2^n)$ |
| Permutations | $n!$ leaves | $O(n \cdot n!)$ |
| $k$-combinations | $\binom{n}{k}$ leaves | $O(k \binom{n}{k})$ |
| N-Queens | $\le n!$ | $O(n!)$, much less in practice |
| Word Search | $m n \cdot 3^{L}$ paths | $O(mn \cdot 3^{L})$ for word length $L$ |
| Palindrome partitioning | $2^{n-1}$ ways to cut | $O(n \cdot 2^n)$ |

---

## Common Mistakes

1. **Appending the shared list instead of a copy.** `result.append(chosen)` stores a reference to the list you keep mutating; at the end every entry is empty. Use `chosen[:]`.

2. **Incomplete undo.** Every change made before the recursive call must be reversed after it — the path, the `used` flags, the constraint sets, the board cell.

3. **Wrong duplicate-skipping condition.** `i > start` (skip repeated *siblings*), not `i > 0` (which also forbids legitimate repeats deeper in the tree).

4. **Checking constraints only at the leaves.** Test partial solutions as early as possible; that is where pruning gets its power.

5. **Passing `i + 1` vs. `i`.** Reuse allowed (LC 39): recurse with `i`. No reuse (LC 40, LC 78): recurse with `i + 1`.

6. **Building strings by concatenation in deep recursions.** Use a list and `"".join` when recording a solution.

7. **Using backtracking where the subproblems overlap.** If the future depends only on a small state, memoize it.

---

## Practice Problems

| Problem | Idea |
|---|---|
| Subsets (LC 78) | Include / exclude, or choose-next |
| Subsets II (LC 90) | Sort + skip repeated siblings |
| Permutations (LC 46) | `used` flags |
| Permutations II (LC 47) | Equal values in original order |
| Combinations (LC 77) | Choose-next with room-left pruning |
| Combination Sum (LC 39) | Reuse allowed; sorted `break` pruning |
| Combination Sum II (LC 40) | No reuse; sibling skip |
| Generate Parentheses (LC 22) | Feasibility pruning on counts |
| Letter Combinations of a Phone Number (LC 17) | Product of candidate sets |
| All Paths From Source to Target (LC 797) | Paths in a DAG |
| Word Search (LC 79) | Grid DFS with mark / unmark |
| Palindrome Partitioning (LC 131) | Cut at palindromic prefixes |
| N-Queens (LC 51) | Column / diagonal sets |
| Sudoku Solver (LC 37) | Most constrained cell first |
| Partition to K Equal Sum Subsets (LC 698) | Ordering + symmetry pruning |
| Matchsticks to Square (LC 473) | Same as LC 698 with $k = 4$ |
