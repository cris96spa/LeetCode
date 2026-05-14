from typing import List


class Solution:
    """Find all cells from which water can flow to both the Pacific and Atlantic oceans.

    Problem Statement:
        Given an m x n matrix 'heights' of an island bordered by the Pacific Ocean (top/left
        edges) and Atlantic Ocean (bottom/right edges), return all cells from which rainwater
        can flow to both oceans. Water flows to neighbors with equal or lesser height.

    Approach:
        Reverse-flood-fill using DFS from each ocean's border cells. Mark all cells reachable
        by each ocean. The answer is cells reachable by both.

    Complexity:
        Time: O(m * n) — each cell visited at most twice.
        Space: O(m * n) for the visited matrices and recursion stack.
    """

    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        rows, cols = len(heights), len(heights[0])
        if rows == 1:
            return [[0, col] for col in range(cols)]
        if cols == 1:
            return [[row, 0] for row in range(rows)]

        pacific = [[False] * cols for _ in range(rows)]
        atlantic = [[False] * cols for _ in range(rows)]

        for row in range(rows):
            self._dfs(row, 0, pacific, heights, rows, cols, heights[row][0])
            self._dfs(row, cols - 1, atlantic, heights, rows, cols, heights[row][cols - 1])
        for col in range(cols):
            self._dfs(0, col, pacific, heights, rows, cols, heights[0][col])
            self._dfs(rows - 1, col, atlantic, heights, rows, cols, heights[rows - 1][col])

        return [
            [r, c]
            for r in range(rows)
            for c in range(cols)
            if pacific[r][c] and atlantic[r][c]
        ]

    def _dfs(
        self,
        r: int,
        c: int,
        visited: List[List[bool]],
        heights: List[List[int]],
        rows: int,
        cols: int,
        prev_height: int,
    ) -> None:
        if r < 0 or r >= rows or c < 0 or c >= cols or visited[r][c]:
            return
        if heights[r][c] < prev_height:
            return
        visited[r][c] = True
        for dr, dc in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            self._dfs(r + dr, c + dc, visited, heights, rows, cols, heights[r][c])
