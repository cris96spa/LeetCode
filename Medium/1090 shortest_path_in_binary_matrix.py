from collections import deque

class Solution:
   """
    Given an n x n binary matrix grid, return the length of the shortest clear path in the matrix. 
    If there is no clear path, return -1.

    A clear path in a binary matrix is a path from the top-left cell (i.e., (0, 0)) to the bottom-right cell 
    (i.e., (n - 1, n - 1)) such that:
    - All the visited cells of the path are 0.
    - All the adjacent cells of the path are 8-directionally connected (i.e., they share an edge or a corner).

    The length of a clear path is the number of visited cells in this path.

    Solution:
    1. **Initial Validation**:
       - Check if the starting cell `(0, 0)` or the ending cell `(n-1, n-1)` is blocked (`1`). 
         If either is blocked, immediately return `-1`.
    2. **Breadth-First Search (BFS)**:
       - BFS is used to explore the shortest path in an unweighted grid, as it guarantees 
         the shortest path when visiting nodes level by level.
       - The BFS queue stores tuples `(i, j, dist)` representing the current cell coordinates `(i, j)` 
         and the distance `dist` from the starting cell.
    3. **Marking Visited Cells**:
       - To avoid revisiting cells, mark them as visited by setting their value to `1` in the grid 
         as soon as they are added to the queue.
    4. **Traversing in 8 Directions**:
       - From the current cell `(i, j)`, compute the next potential positions `(new_i, new_j)` 
         using the predefined 8-directional moves.
       - If a new position is valid (within bounds and unvisited), add it to the queue 
         and mark it as visited.
    5. **Check for the Target**:
       - If the BFS reaches the bottom-right corner `(n-1, n-1)`, return the current distance `dist`.
    6. **No Path Found**:
       - If the BFS completes without reaching the target, return `-1`.

    Complexity:
    - Time Complexity: O(n^2), where n is the grid size, as each cell is processed at most once 
      and there are up to 8 directions to explore for each cell.
    - Space Complexity: O(n^2), as the BFS queue can hold up to n^2 cells in the worst case.
    """


    def shortestPathBinaryMatrix(self, grid: list[list[int]]) -> int:
        """
        Returns the length of the shortest clear path in the binary matrix.

        Args:
        grid (List[List[int]]): The n x n binary grid.

        Returns:
        int: The length of the shortest path if one exists, or -1 if no path exists.
        """
        n = len(grid)

        # If the start or end cell is blocked, there's no path
        if grid[0][0] != 0 or grid[n-1][n-1] != 0:
            return -1

        # Directions for 8-directional movement
        directions = [
            (-1, 0),  # Up
            (1, 0),   # Down
            (0, -1),  # Left
            (0, 1),   # Right
            (-1, -1), # Top-left diagonal
            (-1, 1),  # Top-right diagonal
            (1, -1),  # Bottom-left diagonal
            (1, 1)    # Bottom-right diagonal
        ]

        # BFS queue: stores (row, col, distance)
        queue = deque([(0, 0, 1)])
        # Mark the cell as visited
        grid[0][0] = 1

        while queue:
            i, j, dist = queue.popleft()

            # If we've reached the bottom-right corner
            if i == n-1 and j == n-1:
                return dist

            # Check all directions to find feasible paths
            for dx, dy in directions:
                new_i, new_j = i + dx, j + dy

                # If the new position is valid and not visited, we can add it to the queue
                if 0 <= new_i < n and 0 <= new_j < n and grid[new_i][new_j] == 0:
                    queue.append((new_i, new_j, dist + 1))

                    # Mark the new position as visited
                    grid[new_i][new_j] = 1
            
        return -1
