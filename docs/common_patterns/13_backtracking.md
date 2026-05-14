# Backtracking

## Core Template

```python
def backtrack(path, options):
    if is_complete(path):
        result.append(path[:])  # save a copy
        return

    for choice in options:
        if is_valid(choice):
            path.append(choice)       # choose
            backtrack(path, options)   # explore
            path.pop()                # unchoose
```

Every backtracking problem follows choose/explore/unchoose. The variations come from how you generate `options` and define `is_complete`.

---

## Decision Framework

**When to use a `start` index (combinations/subsets):**
- Order does not matter -- `[1,2]` and `[2,1]` are the same result.
- Each element is used at most once.
- Pass `start` to the recursive call so you only consider elements after the current one.

**When to use a `visited` array (permutations):**
- Order matters -- `[1,2]` and `[2,1]` are different results.
- Each element is used exactly once.
- On every recursive call, loop through all elements but skip those already marked visited.

**When to use neither (allow reuse):**
- Elements can be reused (e.g., Combination Sum I).
- Pass the same `start` (not `start + 1`) to allow picking the same element again.

---

## Pattern 1: Subsets

### Basic Subsets (LC 78)

Every node in the recursion tree is a valid subset, so append at every call.

```python
def subsets(nums):
    result = []

    def backtrack(start, path):
        result.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()

    backtrack(0, [])
    return result
```

**Time:** O(n * 2^n) -- 2^n subsets, each up to length n to copy.
**Space:** O(n) recursion depth (excluding output).

### Subsets with Duplicates (LC 90)

Sort first. Skip an element if it equals the previous one at the same recursion level.

```python
def subsetsWithDup(nums):
    nums.sort()
    result = []

    def backtrack(start, path):
        result.append(path[:])
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:
                continue  # skip duplicate at same level
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()

    backtrack(0, [])
    return result
```

**Time:** O(n * 2^n). **Space:** O(n).

---

## Pattern 2: Permutations

### Basic Permutations (LC 46)

Use a `visited` array. Every element can appear at every position.

```python
def permute(nums):
    result = []
    visited = [False] * len(nums)

    def backtrack(path):
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i in range(len(nums)):
            if not visited[i]:
                visited[i] = True
                path.append(nums[i])
                backtrack(path)
                path.pop()
                visited[i] = False

    backtrack([])
    return result
```

**Time:** O(n * n!) -- n! permutations, O(n) to copy each.
**Space:** O(n).

### Permutations with Duplicates (LC 47)

Sort first. Skip if the same value was already placed at this position in the current level. The key condition: skip `nums[i]` if `nums[i] == nums[i-1]` and `nums[i-1]` was not used (meaning it was already explored and backtracked at this level).

```python
def permuteUnique(nums):
    nums.sort()
    result = []
    visited = [False] * len(nums)

    def backtrack(path):
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i in range(len(nums)):
            if visited[i]:
                continue
            if i > 0 and nums[i] == nums[i - 1] and not visited[i - 1]:
                continue  # skip duplicate at same tree level
            visited[i] = True
            path.append(nums[i])
            backtrack(path)
            path.pop()
            visited[i] = False

    backtrack([])
    return result
```

**Time:** O(n * n!) worst case. **Space:** O(n).

---

## Pattern 3: Combinations

### Basic Combinations (LC 77)

Choose r elements from 1..n without regard to order.

```python
def combine(n, k):
    result = []

    def backtrack(start, path):
        if len(path) == k:
            result.append(path[:])
            return
        for i in range(start, n + 1):
            path.append(i)
            backtrack(i + 1, path)
            path.pop()

    backtrack(1, [])
    return result
```

**Time:** O(k * C(n, k)). **Space:** O(k).

**Pruning optimization:** replace the loop bound with `n - (k - len(path)) + 1` to avoid exploring branches that can never reach length k.

### Combination Sum -- With Reuse (LC 39)

Candidates can be reused unlimited times. Pass `i` (not `i + 1`) to allow reuse.

```python
def combinationSum(candidates, target):
    result = []

    def backtrack(start, path, remaining):
        if remaining == 0:
            result.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break  # pruning (requires sorted input)
            path.append(candidates[i])
            backtrack(i, path, remaining - candidates[i])  # i, not i+1
            path.pop()

    candidates.sort()
    backtrack(0, [], target)
    return result
```

### Combination Sum II -- No Reuse, With Duplicates (LC 40)

Each number used at most once, but input has duplicates. Sort + skip pattern.

```python
def combinationSum2(candidates, target):
    candidates.sort()
    result = []

    def backtrack(start, path, remaining):
        if remaining == 0:
            result.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break
            if i > start and candidates[i] == candidates[i - 1]:
                continue  # skip duplicates
            path.append(candidates[i])
            backtrack(i + 1, path, remaining - candidates[i])
            path.pop()

    backtrack(0, [], target)
    return result
```

---

## Pattern 4: Constraint Satisfaction (N-Queens, Sudoku)

Place items under constraints. Use sets or arrays to track what's already taken.

### N-Queens (LC 51)

```python
def solveNQueens(n):
    result = []
    cols = set()
    diag1 = set()  # row - col
    diag2 = set()  # row + col

    def backtrack(row, board):
        if row == n:
            result.append(["".join(r) for r in board])
            return
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            board[row][col] = "Q"
            backtrack(row + 1, board)
            board[row][col] = "."
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)

    board = [["." for _ in range(n)] for _ in range(n)]
    backtrack(0, board)
    return result
```

**Time:** O(n!) -- at most n choices for row 0, n-1 for row 1, etc.
**Space:** O(n^2) for the board.

---

## Pattern 5: Grid Search (Word Search)

### Word Search (LC 79)

Mark cells visited in-place. Explore 4 directions. Restore on backtrack.

```python
def exist(board, word):
    rows, cols = len(board), len(board[0])

    def backtrack(r, c, idx):
        if idx == len(word):
            return True
        if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != word[idx]:
            return False

        temp = board[r][c]
        board[r][c] = "#"  # mark visited
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if backtrack(r + dr, c + dc, idx + 1):
                return True
        board[r][c] = temp  # restore
        return False

    for r in range(rows):
        for c in range(cols):
            if backtrack(r, c, 0):
                return True
    return False
```

**Time:** O(m * n * 3^L) where L = word length (3 directions after first step since we don't revisit).
**Space:** O(L) recursion depth.

---

## Pattern 6: Partitioning

### Palindrome Partitioning (LC 131)

Partition a string so every substring is a palindrome. At each step, try every prefix -- if it's a palindrome, recurse on the remainder.

```python
def partition(s):
    result = []

    def is_palindrome(sub):
        return sub == sub[::-1]

    def backtrack(start, path):
        if start == len(s):
            result.append(path[:])
            return
        for end in range(start + 1, len(s) + 1):
            substring = s[start:end]
            if is_palindrome(substring):
                path.append(substring)
                backtrack(end, path)
                path.pop()

    backtrack(0, [])
    return result
```

**Time:** O(n * 2^n) -- up to 2^n ways to partition, O(n) palindrome check each.
**Space:** O(n).

---

## Complexity Summary Table

| Pattern | Time | Space |
|---|---|---|
| Subsets | O(n * 2^n) | O(n) |
| Subsets w/ duplicates | O(n * 2^n) | O(n) |
| Permutations | O(n * n!) | O(n) |
| Permutations w/ duplicates | O(n * n!) | O(n) |
| Combinations C(n,k) | O(k * C(n,k)) | O(k) |
| Combination Sum (with reuse) | O(n^(T/M)) | O(T/M) |
| N-Queens | O(n!) | O(n^2) |
| Word Search | O(m * n * 3^L) | O(L) |
| Palindrome Partition | O(n * 2^n) | O(n) |

T = target, M = smallest candidate, L = word length. Space excludes output storage.

---

## Common Mistakes

1. **Forgetting to copy the path.** `result.append(path)` stores a reference that gets mutated. Always use `path[:]` or `list(path)`.
2. **Not sorting before duplicate skipping.** The `if nums[i] == nums[i-1]: continue` trick only works on sorted input.
3. **Wrong loop variable after recursion.** In combination/subset problems, recurse with `i + 1`, not `start + 1`.
4. **Not restoring state.** Every modification (visited flags, board marks, set additions) must be undone after recursion returns.
5. **Using `start` index for permutations.** Permutations need a `visited` array since every element can appear at every position. Using `start` would only generate combinations.
6. **Passing `i + 1` when reuse is allowed.** Combination Sum I allows reuse -- pass `i`, not `i + 1`.
