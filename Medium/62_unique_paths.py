class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        """
        Dynamic Programming

        We want to count how many distinct paths lead from the top-left corner
        to the bottom-right corner of an m x n grid, where the robot can only
        move right or down.

        State:
            state[i][j] = number of unique paths to reach cell (i, j)

        Transition:
            A cell can only be reached:
                - from the cell above    -> state[i-1][j]
                - from the cell on left  -> state[i][j-1]

            Therefore:
                state[i][j] = state[i-1][j] + state[i][j-1]

        Base Case:
            The first row and first column each have exactly 1 way to be reached,
            because the robot can only move in one straight direction there.

        Example for m=3, n=2:
            [1, 1]
            [1, 2]
            [1, 3]

        Time Complexity:
            O(m * n)

        Space Complexity:
            O(m * n)
        """
        state = [[0] * n for _ in range(m)]

        for i in range(m):
            for j in range(n):
                if i == 0 or j == 0:
                    state[i][j] = 1
                else:
                    state[i][j] = state[i - 1][j] + state[i][j - 1]

        return state[-1][-1]
