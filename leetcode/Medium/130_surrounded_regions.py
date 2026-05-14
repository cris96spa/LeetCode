from collections import deque
from typing import List


class Solution:
    """Capture all 'O' regions on the board that are fully surrounded by 'X'.

    Problem Statement:
        Given an m x n matrix board of 'X' and 'O', capture all regions surrounded by 'X'.
        A region is surrounded if none of its 'O' cells touch the border. Captured regions
        are replaced with 'X' in-place.

    Approach:
        1. BFS from all border 'O' cells, marking them 'S' (safe).
        2. Replace remaining 'O' cells (surrounded) with 'X'.
        3. Revert 'S' cells back to 'O'.

    Complexity:
        Time: O(m * n).
        Space: O(m * n) for the BFS queue.
    """

    def solve(self, board: List[List[str]]) -> None:
        if not board or not board[0]:
            return

        rows, cols = len(board), len(board[0])
        queue = deque()

        for row in range(rows):
            for col in [0, cols - 1]:
                if board[row][col] == "O":
                    queue.append((row, col))
                    board[row][col] = "S"
        for col in range(cols):
            for row in [0, rows - 1]:
                if board[row][col] == "O":
                    queue.append((row, col))
                    board[row][col] = "S"

        self._bfs_mark(board, queue, rows, cols)
        self._flip_cells(board, rows, cols)

    def _bfs_mark(self, board: List[List[str]], queue: deque, rows: int, cols: int) -> None:
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        while queue:
            row, col = queue.popleft()
            for dx, dy in directions:
                nr, nc = row + dx, col + dy
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == "O":
                    queue.append((nr, nc))
                    board[nr][nc] = "S"

    def _flip_cells(self, board: List[List[str]], rows: int, cols: int) -> None:
        for row in range(rows):
            for col in range(cols):
                if board[row][col] == "O":
                    board[row][col] = "X"
                elif board[row][col] == "S":
                    board[row][col] = "O"
