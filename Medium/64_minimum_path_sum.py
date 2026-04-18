class Solution:
    def minPathSum(self, grid: list[list[int]]) -> int:
        """
        Problem:
        Given an m x n grid of non-negative integers, find a path from the
        top-left to the bottom-right corner that minimizes the sum of values
        along the path.

        Constraints:
        - You can only move either right or down at any point.
        - 0 <= grid[i][j] <= 200

        ------------------------------------------------------------
        Dynamic Programming Approach (Space Optimized)

        Idea:
        Each cell (i, j) can be reached either:
        - from above (i-1, j)
        - from the left (i, j-1)

        So the recurrence is:
            dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])

        Instead of storing the full m x n DP table, we observe that:
        - To compute the current row, we only need:
            * the previous row (dp[i-1][j])
            * the current row's previous value (dp[i][j-1])

        This allows us to compress the DP table into a single array.

        ------------------------------------------------------------
        State Definition (1D Optimization):

        Let `state[j]` represent the minimum path sum to reach column `j`
        in the current row.

        During iteration:
        - Before updating `state[j]`, it stores the value from the previous row
          → represents dp[i-1][j] (from up)
        - After updating `state[j-1]`, it represents dp[i][j-1] (from left)

        Transition:
            state[j] = grid[i][j] + min(state[j], state[j-1])

            where:
            - state[j]   → from up
            - state[j-1] → from left

        ------------------------------------------------------------
        Initialization:

        First cell:
            state[0] = grid[0][0]

        First row (can only come from left):
            state[j] = state[j-1] + grid[0][j]

        First column (can only come from above):
            state[0] += grid[i][0]  (for each new row)

        ------------------------------------------------------------
        Complexity:

        Time:  O(m * n)
        Space: O(n)   (optimized from O(m * n))

        ------------------------------------------------------------
        Key Insight:

        We can reuse a single array because each state depends only on:
        - the previous row (old value of state[j])
        - the current row (updated value of state[j-1])

        The left-to-right iteration order ensures we do not overwrite
        values before they are used.
        """

        m, n = len(grid), len(grid[0])
        state = [0] * n

        state[0] = grid[0][0]

        # Initialize first row
        for j in range(1, n):
            state[j] = grid[0][j] + state[j - 1]

        # Process remaining rows
        for i in range(1, m):
            state[0] += grid[i][0]
            for j in range(1, n):
                state[j] = grid[i][j] + min(state[j - 1], state[j])

        return state[-1]