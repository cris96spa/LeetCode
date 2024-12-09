from collections import deque


class Solution:
    """
    994. Rotting Oranges

    Problem Statement:
    You are given an m x n grid where each cell can have one of three values:
    - 0 representing an empty cell,
    - 1 representing a fresh orange, or
    - 2 representing a rotten orange.

    Every minute, any fresh orange that is 4-directionally adjacent to a rotten orange becomes rotten.

    Return the minimum number of minutes that must elapse until no cell has a fresh orange.
    If this is impossible, return -1.

    Example:
    Input: grid = [[2,1,1],[1,1,0],[0,1,1]]
    Output: 4

    Approach:
    - Perform BFS starting from all initial rotten oranges.
    - Track the time it takes for all reachable fresh oranges to become rotten.
    - Use a queue to store the positions of rotten oranges, processing them level by level.
    - Update the state of fresh oranges when they are adjacent to a rotten one.

    Complexity:
    - Time: O(m * n), where m and n are the dimensions of the grid.
    - Space: O(m * n), to store the queue in the worst case.
    """

    def orangesRotting(self, grid: list[list[int]]) -> int:
        m, n = len(grid), len(grid[0])
        queue = deque()

        fresh_oranges = 0

        # Initialize the count of fresh oranges and the queue with rotten ones
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    fresh_oranges += 1
                elif grid[i][j] == 2:
                    queue.append((i, j))

        # Edge case: no fresh or rotten oranges
        if fresh_oranges == 0:
            return 0

        directions = [
            (-1, 0),  # left
            (0, 1),  # up
            (1, 0),  # right
            (0, -1),  # down
        ]
        num_minutes = 0

        # BFS to simulate the rotting process
        while queue and fresh_oranges > 0:
            # Increment the minute for each level of BFS
            num_minutes += 1
            for _ in range(len(queue)):
                x, y = queue.popleft()
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    # If the neighbor is a fresh orange, rot it
                    if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] == 1:
                        grid[nx][ny] = 2
                        fresh_oranges -= 1
                        queue.append((nx, ny))

        # If fresh oranges remain, return -1; otherwise, return the elapsed time
        return num_minutes if fresh_oranges == 0 else -1
