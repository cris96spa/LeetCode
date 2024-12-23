from collections import deque
from typing import List


class Solution:
    def solve(self, board: List[List[str]]) -> None:
        """
        Problem Statement:
        ------------------
        You are given an m x n matrix board containing letters 'X' and 'O'. Capture regions that are surrounded:

        - A cell is connected to adjacent cells horizontally or vertically.
        - To form a region, connect every 'O' cell.
        - A region is surrounded if it is completely enclosed by 'X' cells and none of its cells are on the edge
          of the board.

        The goal is to modify the board in-place such that all surrounded regions are captured, replacing all 'O'
        cells in surrounded regions with 'X'.

        Solution:
        ---------
        The solution involves three main steps:
        1. Identify all 'O' regions connected to the edges of the board. These regions cannot be surrounded,
           as they touch the border. Mark these 'O' cells temporarily as 'S'.
        2. Replace all remaining 'O' cells (which are surrounded) with 'X'.
        3. Revert the 'S' cells back to 'O', as they were part of safe regions.

        This is implemented using a BFS approach starting from all edge 'O' cells.

        Args:
            board (List[List[str]]): The m x n board containing 'X' and 'O'.

        Returns:
            None: The board is modified in-place.

        Example:
        ---------
            Input:
            board = [
                ['X', 'X', 'X', 'X'],
                ['X', 'O', 'O', 'X'],
                ['X', 'X', 'O', 'X'],
                ['X', 'O', 'X', 'X']
            ]

            Output:
            board = [
                ['X', 'X', 'X', 'X'],
                ['X', 'X', 'X', 'X'],
                ['X', 'X', 'X', 'X'],
                ['X', 'O', 'X', 'X']
            ]

        Constraints:
        -------------
            - The board will have at most 200 rows and 200 columns.
        """
        if not board or not board[0]:
            return

        rows, cols = len(board), len(board[0])
        queue = deque()

        # Directions for moving up, down, left, and right
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        # Add all edge 'O's to the queue and mark them as safe ('S')
        for row in range(rows):
            for col in [0, cols - 1]:  # Left and right borders
                if board[row][col] == "O":
                    queue.append((row, col))
                    board[row][col] = "S"
        for col in range(cols):
            for row in [0, rows - 1]:  # Top and bottom borders
                if board[row][col] == "O":
                    queue.append((row, col))
                    board[row][col] = "S"

        # Perform BFS to mark all connected 'O's as safe
        while queue:
            row, col = queue.popleft()
            for dx, dy in directions:
                new_row, new_col = row + dx, col + dy
                if (
                    0 <= new_row < rows
                    and 0 <= new_col < cols
                    and board[new_row][new_col] == "O"
                ):
                    queue.append((new_row, new_col))
                    board[new_row][new_col] = "S"

        # Final pass: replace all 'O' with 'X' and 'S' back to 'O'
        for row in range(rows):
            for col in range(cols):
                if board[row][col] == "O":
                    board[row][col] = "X"
                elif board[row][col] == "S":
                    board[row][col] = "O"
