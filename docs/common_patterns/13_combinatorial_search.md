# Combinatorial Search

Some problems have no clever shortcut: to find all valid arrangements, or the best one, you must in principle consider every candidate. **Combinatorial search** is the art of doing that efficiently. Its workhorse is **backtracking**, which enumerates every configuration of a search space exactly once while abandoning partial configurations the moment they can't possibly succeed.

Exhaustive search has a bad reputation, but surprisingly large problems yield to it, and it has one great virtue: it is *obviously correct*. If you've tried every possibility, you haven't missed the answer. The craft lies in four places:

- **Generating** each candidate exactly once, with no repeats and no omissions.
- **Pruning** the search so that you only look at candidates that matter.
- **Ordering** the search so that the best candidates are examined first.
- **Splitting** the search space when it is too big to enumerate as a whole.

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

Every node of the search tree is itself a subset; its children add one element *later* than any already chosen. Starting each loop at `start` is what prevents generating `{2, 1}` after `{1, 2}`.

```python
def subsets(nums: list[int]) -> list[list[int]]:
    result: list[list[int]] = []
    chosen: list[int] = []

    def extend(start: int) -> None:
        result.append(chosen[:])                 # every node is a valid subset; copy, chosen keeps changing
        for i in range(start, len(nums)):
            chosen.append(nums[i])
            extend(i + 1)
            chosen.pop()

    extend(0)
    return result
```

$O(n \cdot 2^n)$: $2^n$ subsets, each copied in $O(n)$. (Subsets can also be generated without recursion by binary counting; see [Bit Manipulation](04_bit_manipulation.md#generating-subsets).) The combination, duplicate-handling, and Combination Sum generators below are all this same tree with an extra rule.

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

Choose $k$ of the numbers $1 \dots n$. It's the subsets tree, recording only nodes at depth $k$ — plus a cheap but valuable **prune**: if there aren't enough numbers left to reach size $k$, stop.

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

**Subsets with duplicates** (LC 90) — in the subsets tree, siblings are the choices at the same node; skip a value equal to the previous sibling:

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

**2. Bounding (branch and bound):** in optimization problems, abandon a partial solution when even an optimistic estimate of its best completion can't beat the best solution found so far. See the [worked example](#branch-and-bound-find-minimum-time-to-finish-all-jobs-lc-1723) below.

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

### Branch and bound: Find Minimum Time to Finish All Jobs (LC 1723)

LC 698 asks a yes/no question. Turn it into an optimization: assign every job to one of $k$ workers so that the **largest** total is as small as possible. Backtracking still tries every assignment, but now it also remembers `best`, the cost of the best complete assignment found so far. Branch and bound needs two things:

- **A lower bound on every completion.** The largest load so far, `current_max`, can only grow as more jobs are assigned. So no completion of the current branch can cost less than it.
- **A good solution to compare against.** As soon as `current_max >= best`, the branch can't produce anything better than what's already known, so abandon it.

```python
def minimum_time_required(jobs: list[int], k: int) -> int:
    jobs = sorted(jobs, reverse=True)            # big jobs first: high loads show up early
    loads = [0] * k
    best = sum(jobs)                             # a valid answer to start from: one worker does it all

    def assign(i: int, current_max: int) -> None:
        nonlocal best
        if current_max >= best:
            return                               # bound: no completion of this branch can win
        if i == len(jobs):
            best = current_max                   # a strictly better complete solution
            return
        tried: set[int] = set()
        for w in range(k):
            if loads[w] in tried:
                continue                         # symmetry: equal loads give equivalent subtrees
            tried.add(loads[w])
            loads[w] += jobs[i]
            assign(i + 1, max(current_max, loads[w]))
            loads[w] -= jobs[i]

    assign(0, 0)
    return best
```

The bound and the search help each other. Every improvement to `best` makes the bound prune more, and sorting the jobs largest first finds good solutions early, while the tree is still small. Two refinements tighten it further: start `best` from a greedy solution instead of the trivial one, and use a stronger lower bound, such as $\max(\text{current\_max}, \lceil \text{remaining work} / k \rceil)$. The stronger the bound, the earlier branches die.

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

## Best-First Search and A\*

Backtracking explores the tree depth-first, in whatever order the candidates happen to come. For optimization problems, it can pay to always expand the **most promising** partial solution next. **Best-first search** keeps all the partial solutions generated so far in a priority queue, ordered by a cost, and repeatedly expands the cheapest one.

**When can it stop?** Not necessarily at the first complete solution it pops. That solution was the cheapest *partial* solution when it was chosen, but a more expensive partial solution might still finish more cheaply. The search can stop once the cheapest entry left in the queue costs at least as much as the best complete solution found. That rule is only correct if a partial solution's cost is a **lower bound** on the cost of every completion of it. Otherwise something deeper in the queue could still turn into a better answer.

**A\*** sharpens the cost. Ordering by *cost so far* alone favors short partial solutions: in a traveling-salesman search, half a tour is almost always cheaper than any full tour, so every half-tour gets expanded before the search finishes anything. A\* orders by *cost so far + an estimate of the remaining cost*. If the estimate never overestimates, the total is still a lower bound, the stopping rule stays correct, and partial solutions near completion are no longer penalized. With a consistent estimate, like the one below, the first complete solution popped is optimal. Dijkstra's algorithm is A\* with an estimate of zero.

**Sliding Puzzle** (LC 773) asks for the fewest moves that turn a $2 \times 3$ board into `[[1, 2, 3], [4, 5, 0]]`, where each move slides a tile into the blank. Each move shifts one tile by one cell, so every tile needs at least as many moves as its Manhattan distance from its goal cell. The sum of those distances is therefore a lower bound on the moves remaining:

```python
def sliding_puzzle(board: list[list[int]]) -> int:
    goal = (1, 2, 3, 4, 5, 0)
    moves_from = {0: (1, 3), 1: (0, 2, 4), 2: (1, 5), 3: (0, 4), 4: (1, 3, 5), 5: (2, 4)}

    def estimate(state: tuple[int, ...]) -> int:
        """Sum of each tile's Manhattan distance to its goal cell: never overestimates."""
        return sum(
            abs(i // 3 - (tile - 1) // 3) + abs(i % 3 - (tile - 1) % 3)
            for i, tile in enumerate(state)
            if tile
        )

    start = tuple(tile for row in board for tile in row)
    fewest = {start: 0}                          # fewest moves found so far to each state
    heap = [(estimate(start), 0, start)]         # (moves + estimate, moves, state)
    while heap:
        _, moves, state = heapq.heappop(heap)
        if state == goal:
            return moves
        if moves > fewest[state]:
            continue                             # stale entry
        blank = state.index(0)
        for j in moves_from[blank]:
            nxt = list(state)
            nxt[blank], nxt[j] = nxt[j], nxt[blank]
            nxt = tuple(nxt)
            if moves + 1 < fewest.get(nxt, moves + 2):
                fewest[nxt] = moves + 1
                heapq.heappush(heap, (moves + 1 + estimate(nxt), moves + 1, nxt))
    return -1                                    # the goal is unreachable from this board
```

This board has only 360 reachable states, so plain BFS also works. A\* matters when the state space is large: the tighter the estimate, the more of the space it never touches.

**The price is memory.** Depth-first backtracking stores only the current path, while best-first search stores the whole frontier. In Skiena's traveling-salesman experiments with 11 cities, the priority queue grew to 202,063 entries; the backtracking stack needed 11. A slow program eventually gives an answer, but one that runs out of memory never does.

!!! tip "Take-Home Lesson"
    The promise of a partial solution is not just its cost so far, but also the cost of the rest of the solution. An estimate of the remaining cost that is tight, yet still a lower bound, makes best-first search far more efficient.

---

## Meet in the Middle

At $n = 40$, enumerating all $2^{40} \approx 10^{12}$ subsets is hopeless, but $2^{20} \approx 10^6$ is easy. **Meet in the middle** gets from one to the other by splitting the items into two halves, enumerating all subsets of each half separately, and combining the two lists cleverly instead of trying every pair.

**Closest Subsequence Sum** (LC 1755): find the subset sum closest to `goal`, with $n \le 40$. Every subset is a subset of the left half plus a subset of the right half, so its sum is $s_L + s_R$. For each left sum $s_L$, the best partner is the right sum closest to $\text{goal} - s_L$. After sorting the right sums, binary search finds it:

```python
def subset_sums(nums: list[int]) -> list[int]:
    sums = [0]
    for x in nums:
        sums += [s + x for s in sums]            # every old subset, with and without x
    return sums


def min_abs_difference(nums: list[int], goal: int) -> int:
    half = len(nums) // 2
    left = subset_sums(nums[:half])
    right = sorted(subset_sums(nums[half:]))
    best = abs(goal)                             # the empty subset
    for s in left:
        i = bisect.bisect_left(right, goal - s)  # the best partner is right[i - 1] or right[i]
        for j in (i - 1, i):
            if 0 <= j < len(right):
                best = min(best, abs(s + right[j] - goal))
    return best
```

**Time:** $O(2^{n/2} \cdot n)$, dominated by sorting the right half's $2^{n/2}$ sums: well under a second in Python at $n = 40$, compared with hours for brute force. The idea works whenever a solution splits into two independent halves whose combination can be checked quickly: by sorting and binary search, a hash map, or two pointers. **Partition Array Into Two Arrays to Minimize Sum Difference** (LC 2035) is the same trick, with the left and right sums grouped by how many elements they use.

---

## Heuristic Search (Briefly)

When the search space is too large even for pruning, and an exact answer isn't required, **heuristic search** trades the guarantee of optimality for speed. **Random sampling** tries random solutions and keeps the best. **Local search** starts from some solution and repeatedly makes small changes, such as swapping two cities in a tour, as long as they improve it. It stops at a *local* optimum, which may be far from the best. **Simulated annealing** also accepts some changes that make the solution worse, with a probability that shrinks over time. That lets it escape local optima early, then settle down. These methods power real-world scheduling and layout tools, but they don't appear in interview problems, which always have exact answers.

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
| Meet in the middle on subsets | $2 \cdot 2^{n/2}$ half-subsets | $O(n \cdot 2^{n/2})$ |

---

## Common Mistakes

1. **Appending the shared list instead of a copy.** `result.append(chosen)` stores a reference to the list you keep mutating; at the end every entry is empty. Use `chosen[:]`.

2. **Incomplete undo.** Every change made before the recursive call must be reversed after it — the path, the `used` flags, the constraint sets, the board cell.

3. **Wrong duplicate-skipping condition.** `i > start` (skip repeated *siblings*), not `i > 0` (which also forbids legitimate repeats deeper in the tree).

4. **Checking constraints only at the leaves.** Test partial solutions as early as possible; that is where pruning gets its power.

5. **Passing `i + 1` vs. `i`.** Reuse allowed (LC 39): recurse with `i`. No reuse (LC 40, LC 78): recurse with `i + 1`.

6. **Building strings by concatenation in deep recursions.** Use a list and `"".join` when recording a solution.

7. **Using backtracking where the subproblems overlap.** If the future depends only on a small state, memoize it.

8. **Stopping best-first search too early.** The first complete solution popped is optimal only when the queue's costs are lower bounds on every completion (and, for A\*, the estimate never overestimates). Otherwise keep searching until the cheapest queue entry can't beat the best solution found.

---

## Practice Problems

| Problem | Idea |
|---|---|
| Subsets (LC 78) | Choose the next element |
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
| Find Minimum Time to Finish All Jobs (LC 1723) | Branch and bound |
| Sliding Puzzle (LC 773) | A\* with Manhattan distance (or BFS) |
| Closest Subsequence Sum (LC 1755) | Meet in the middle |
| Partition Array Into Two Arrays to Minimize Sum Difference (LC 2035) | Meet in the middle, grouped by size |
