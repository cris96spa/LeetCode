class Solution:
    """♛ N-Queens.

    Problem:
    --------
    Place `n` queens on an `n x n` chessboard so that no two attack each other, and return
    every distinct solution. Each solution is a board of `n` strings, where "Q" is a queen
    and "." an empty square. Constraint: 1 <= n <= 9.

    Key Insight:
    ------------
    Two queens attack each other along a row, a column, or a diagonal. So every row holds
    exactly one queen, and a solution is fully described by `queens[r]`, the column of the
    queen in row `r`. The search fills one row at a time, which rules out row attacks by
    construction. The other three are each identified by one number:
    - column: `c`;
    - diagonal (top-left to bottom-right): `r - c`, constant along it;
    - anti-diagonal (top-right to bottom-left): `r + c`, constant along it.
    Keeping the occupied ones in three sets makes every safety check O(1).

    Approach:
    ---------
    Backtracking, row by row:
    - Complete: `row == n` means every row holds a queen, so record the board.
    - Candidates: every column `col` whose column, diagonal and anti-diagonal are free.
    - Make move: set `queens[row] = col` and mark its column and both diagonals.
    - Unmake move: reset `queens[row]` to -1 and unmark them.
    Boards are rendered only for complete solutions, never for dead-end partial ones.

    Complexity:
    -----------
    - Time: O(n * n!). Row `r` has at most `n - r` free columns, so there are at most n!
      complete placements, each column check is O(1), and each of the S solutions costs
      O(n^2) to render (S is far below n!).
    - Space: O(n) auxiliary for `queens`, the sets and the recursion stack;
      O(S * n^2) for the output.

    Example:
    --------
    Input: n = 4
    Output: [[".Q..", "...Q", "Q...", "..Q."], ["..Q.", "Q...", "...Q", ".Q.."]]
    """

    def solveNQueens(self, n: int) -> list[list[str]]:
        results: list[list[str]] = []
        queens = [-1] * n  # queens[row] = column of the queen in that row, -1 if empty
        cols: set[int] = set()
        diag: set[int] = set()
        anti_diag: set[int] = set()

        def build_board() -> list[str]:
            return ["." * col + "Q" + "." * (n - col - 1) for col in queens]

        def is_free(row: int, col: int) -> bool:
            return col not in cols and row - col not in diag and row + col not in anti_diag

        def make_move(row: int, col: int) -> None:
            queens[row] = col
            cols.add(col)
            diag.add(row - col)
            anti_diag.add(row + col)

        def unmake_move(row: int, col: int) -> None:
            queens[row] = -1
            cols.remove(col)
            diag.remove(row - col)
            anti_diag.remove(row + col)

        def place(row: int) -> None:
            if row == n:
                results.append(build_board())
                return

            for col in range(n):
                if not is_free(row, col):
                    continue

                make_move(row, col)
                place(row + 1)
                unmake_move(row, col)

        place(0)
        return results
