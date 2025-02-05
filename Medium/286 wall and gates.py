from collections import deque


class Solution:
    def wallsAndGates(self, rooms: list[list[int]]) -> None:
        """
        Modify rooms in-place to fill each empty room with the distance to its nearest gate.

        BFS is used to propagate the shortest distance from each gate to reachable empty rooms.

        Time Complexity: O(m * n) - Each cell is processed once in BFS.
        Space Complexity: O(m * n) - In the worst case, all empty rooms are added to the queue.

        :param rooms: 2D grid of walls (-1), gates (0), and empty rooms (INF).
        """
        if not rooms or not rooms[0]:  # Edge case: empty grid
            return

        rows, cols = len(rooms), len(rooms[0])
        INF = 2147483647
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        queue = deque()

        # Step 1: Enqueue all gates (cells with value 0)
        for r in range(rows):
            for c in range(cols):
                if rooms[r][c] == 0:
                    queue.append((r, c))

        # Step 2: Perform multi-source BFS
        while queue:
            row, col = queue.popleft()
            curr_val = rooms[row][col]

            for dx, dy in directions:
                new_row, new_col = row + dx, col + dy
                if (
                    0 <= new_row < rows
                    and 0 <= new_col < cols
                    and rooms[new_row][new_col] == INF
                ):
                    rooms[new_row][new_col] = curr_val + 1  # Update distance
                    queue.append(
                        (new_row, new_col)
                    )  # Add cell to queue for further processing
