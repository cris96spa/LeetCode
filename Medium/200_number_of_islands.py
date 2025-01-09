from collections import deque
from typing import List


class Solution:
    """
    Problem Description:
    ---------------------
    Given an m x n 2D binary grid `grid` representing a map of '1's (land) and '0's (water),
    return the number of islands. An island is surrounded by water and is formed by connecting
    adjacent lands horizontally or vertically. You may assume all four edges of the grid are
    surrounded by water.

    Approach:
    ---------
    This solution uses Breadth-First Search (BFS) to traverse the grid:
    1. Iterate over all cells in the grid.
    2. When a land cell ('1') is found, increment the island count and perform BFS to mark all
       connected land cells as visited by changing their value to 'x'.
    3. Continue until all cells in the grid are processed.

    Complexity:
    -----------
    - Time Complexity: O(n * m), where n is the number of rows and m is the number of columns.
      Each cell is visited at most once.
    - Space Complexity: O(n * m) in the worst case, for the BFS queue.

    Example:
    --------
    Input:
    grid = [
        ["1","1","0","0","0"],
        ["1","1","0","0","0"],
        ["0","0","1","0","0"],
        ["0","0","0","1","1"]
    ]
    Output: 3
    """

    def numIslands(self, grid: List[List[str]]) -> int:
        rows, cols = len(grid), len(grid[0])
        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        ]  # Possible moves: up, down, left, right
        islands = 0

        def bfs(row: int, col: int):
            queue = deque([(row, col)])
            grid[row][col] = "x"  # Mark as visited

            while queue:
                r, c = queue.popleft()

                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    # If valid cell and unvisited land
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "1":
                        queue.append((nr, nc))
                        grid[nr][nc] = "x"  # Mark as visited

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "1":  # Start BFS when land is found
                    islands += 1
                    bfs(r, c)

        return islands
