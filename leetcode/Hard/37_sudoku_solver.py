class Solution:
    """🔢 Sudoku Solver.

    Problem:
    --------
    Fill the empty cells (marked ".") of a 9 x 9 Sudoku board in place, so that every row,
    every column and every 3 x 3 block contains each digit 1-9 exactly once. The input is
    guaranteed to have exactly one solution.

    Key Insight:
    ------------
    Plain backtracking in reading order is correct but can be very slow on hard puzzles.
    The order in which cells are filled matters: always fill the empty cell with the
    fewest candidates first (most constrained first, or "fail first").
    - A cell with 1 candidate is a forced move: no branching at all.
    - A cell with 0 candidates means the current partial board is dead, and picking it
      first detects this immediately instead of many moves later.
    - Each placed digit removes candidates from its row, column and block, which keeps
      the branching small further down the tree.

    Approach:
    ---------
    State:
    - `rows[r]`, `cols[c]`, `blocks[b]`: digits already used in each row, column and
      block, where block `b = row // 3 * 3 + col // 3` numbers blocks left to right, top
      to bottom.
    - `empty`: the set of cells still to fill.
    - Candidates of a cell: "123456789" minus its row, column and block digits.

    Backtracking:
    - Complete: `empty` is empty, so every cell holds a valid digit.
    - Choose: the empty cell with the fewest candidates.
    - Make move: write the digit and add it to its row, column and block.
    - Unmake move: reset the cell to "." and remove the digit from all three.
    The given digits are registered with the same `make_move` before the search starts.

    Complexity:
    -----------
    With m empty cells (m <= 81):
    - Time: O(9^m * m) in the worst case: at most 9 choices per cell, and choosing the
      next cell scans all empty cells. In practice the heuristic keeps the tree tiny.
    - Space: O(m) for `empty` and the recursion stack; the row, column and block sets
      hold at most 81 digits each in total.
    """

    def solveSudoku(self, board: list[list[str]]) -> None:  # noqa: C901 (each nested helper adds 1)
        """Do not return anything, modify board in-place instead."""
        rows: list[set[str]] = [set() for _ in range(9)]
        cols: list[set[str]] = [set() for _ in range(9)]
        blocks: list[set[str]] = [set() for _ in range(9)]
        empty: set[tuple[int, int]] = set()

        def block_idx(row: int, col: int) -> int:
            return row // 3 * 3 + col // 3

        def candidates(row: int, col: int) -> set[str]:
            return set("123456789") - rows[row] - cols[col] - blocks[block_idx(row, col)]

        def num_candidates(cell: tuple[int, int]) -> int:
            row, col = cell
            return len(candidates(row, col))

        def make_move(row: int, col: int, digit: str) -> None:
            board[row][col] = digit
            rows[row].add(digit)
            cols[col].add(digit)
            blocks[block_idx(row, col)].add(digit)

        def unmake_move(row: int, col: int, digit: str) -> None:
            board[row][col] = "."
            rows[row].remove(digit)
            cols[col].remove(digit)
            blocks[block_idx(row, col)].remove(digit)

        for row in range(9):
            for col in range(9):
                if board[row][col] == ".":
                    empty.add((row, col))
                else:
                    make_move(row, col, board[row][col])  # register the given digit

        def solve() -> bool:
            if not empty:
                return True

            row, col = min(empty, key=num_candidates)  # most constrained; 0 candidates = dead end
            empty.remove((row, col))
            for digit in candidates(row, col):
                make_move(row, col, digit)
                if solve():
                    return True
                unmake_move(row, col, digit)

            empty.add((row, col))
            return False

        solve()
