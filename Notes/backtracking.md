# Backtracking Cheatsheet for LeetCode Problems

Backtracking is a systematic way to explore all possible configurations of a solution space. This cheat sheet outlines the general approach to solve backtracking problems, common templates, and key points to remember.

---

## General Steps to Solve Backtracking Problems

1. **Understand the Problem**:

   - Identify if the problem involves generating all solutions or finding an optimal/valid solution (e.g., subsets, permutations, combinations, or a path).

2. **Define the Decision Space**:

   - Determine what choices are available at each step.

3. **Choose/Explore/Unchoose Pattern**:

   - Choose a potential solution element.
   - Recursively explore further.
   - Unchoose (backtrack) to reset the state.

4. **Base Case**:

   - Define when a solution is complete.

5. **Prune**:
   - Add constraints to skip invalid paths (early termination).

---

## Backtracking Template

```python
# General Backtracking Template

def backtrack(path, options):
    if is_valid(path):         # Base case: stop when path is valid/complete
        result.append(path[:]) # Save a deep copy of the path if needed
        return

    for choice in options:     # Iterate through choices
        if is_valid_choice(choice):  # Skip invalid choices
            path.append(choice)      # Make a choice
            backtrack(path, options) # Explore further
            path.pop()               # Undo the choice (backtrack)
```

---

## Common Problem Types and Patterns

### 1. Subsets

- **Example**: Generate all subsets of a given set.
- **Key Idea**: Either include or exclude each element.

```python
def subsets(nums):
    result = []

    def backtrack(start, path):
        result.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])  # Include nums[i]
            backtrack(i + 1, path)  # Explore
            path.pop()  # Exclude nums[i]

    backtrack(0, [])
    return result
```

### 2. Permutations

- **Example**: Generate all permutations of a set.
- **Key Idea**: Use a visited array to track used elements.

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
                visited[i] = True  # Mark as used
                path.append(nums[i])
                backtrack(path)
                path.pop()  # Backtrack
                visited[i] = False  # Reset state

    backtrack([])
    return result
```

### 3. Combinations

- **Example**: Generate all combinations of size k.
- **Key Idea**: Combine elements without reusing.

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

### 4. N-Queens

- **Example**: Place n queens on an n×n chessboard.
- **Key Idea**: Check for conflicts before placing a queen.

```python
def solveNQueens(n):
    result = []
    board = ["." * n for _ in range(n)]

    def is_safe(row, col):
        for i in range(row):
            if board[i][col] == "Q" or \
               (col - (row - i) >= 0 and board[i][col - (row - i)] == "Q") or \
               (col + (row - i) < n and board[i][col + (row - i)] == "Q"):
                return False
        return True

    def backtrack(row):
        if row == n:
            result.append([row for row in board])
            return

        for col in range(n):
            if is_safe(row, col):
                board[row] = board[row][:col] + "Q" + board[row][col+1:]
                backtrack(row + 1)
                board[row] = board[row][:col] + "." + board[row][col+1:]

    backtrack(0)
    return result
```

### 5. Word Search

- **Example**: Find if a word exists in a grid.
- **Key Idea**: Mark cells as visited.

```python
def exist(board, word):
    rows, cols = len(board), len(board[0])

    def backtrack(row, col, index):
        if index == len(word):
            return True

        if row < 0 or row >= rows or col < 0 or col >= cols or board[row][col] != word[index]:
            return False

        temp, board[row][col] = board[row][col], "#"  # Mark visited
        found = any(
            backtrack(row + dr, col + dc, index + 1)
            for dr, dc in [(1, 0), (0, 1), (-1, 0), (0, -1)]
        )
        board[row][col] = temp  # Unmark visited
        return found

    for r in range(rows):
        for c in range(cols):
            if backtrack(r, c, 0):
                return True

    return False
```

---

## Tips and Tricks

1. **Avoid Recomputing States**:

   - Use memoization or pruning where applicable.

2. **Track State Changes Clearly**:

   - Always reset any modified state (e.g., visited arrays or temporary markings).

3. **Early Pruning**:

   - Add conditions to skip unnecessary paths early in the recursion.

4. **Iterative vs. Recursive**:

   - Most backtracking problems are recursive, but some (like subsets) can also be solved iteratively.

5. **Understand Constraints**:
   - If constraints are tight, focus on pruning and optimizing the recursion.

---

By following this structured approach and leveraging these patterns, you can tackle a wide variety of backtracking problems efficiently on LeetCode.
