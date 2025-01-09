class Solution:
    """
    Problem Description:
    ---------------------
    You are climbing a staircase. It takes `n` steps to reach the top.

    Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

    Example:
    --------
    Input: n = 3
    Output: 3
    Explanation:
        There are three ways to climb to the top:
        1. 1 step + 1 step + 1 step
        2. 1 step + 2 steps
        3. 2 steps + 1 step

    Constraints:
    ------------
    1 <= n <= 45

    Solutions:
    ----------
    1. Recursive Solution with Memoization:
        - Approach:
            This solution uses recursion to compute the number of ways to climb the stairs.
            It avoids redundant computations by storing intermediate results in a dictionary (`mem`)
            through memoization.
        - Time Complexity: O(n), each subproblem is computed once.
        - Space Complexity: O(n), for recursion stack and memoization dictionary.

        Implementation:
        ----------------
        def climbStairs(self, n: int) -> int:
            mem = {}
            def solve(n: int) -> int:
                if n < 0:
                    return 0
                elif n == 0:
                    return 1
                elif n in mem:
                    return mem[n]
                mem[n] = solve(n - 1) + solve(n - 2)
                return mem[n]
            return solve(n)

    2. Iterative Dynamic Programming:
        - Approach:
            This solution uses an iterative dynamic programming approach with an array (`dp`)
            to store the number of ways to reach each step.
            It builds the solution from the base cases (0 and 1 step) up to `n`.
        - Time Complexity: O(n), since we iterate once from 2 to n.
        - Space Complexity: O(n), for the `dp` array.

        Implementation:
        ----------------
        def climbStairs(self, n: int) -> int:
            if n <= 1:
                return 1
            dp = [0] * (n + 1)
            dp[0], dp[1] = 1, 1
            for i in range(2, n + 1):
                dp[i] = dp[i - 1] + dp[i - 2]
            return dp[n]

    3. Space-Optimized Iterative Approach:
        - Approach:
            This approach improves on the iterative DP solution by reducing the space complexity.
            Instead of storing results for all steps, it keeps track of only the last two results,
            as they are the only ones needed to calculate the next step.
        - Time Complexity: O(n), as we iterate once from 2 to n.
        - Space Complexity: O(1), using only two variables.

        Implementation:
        ----------------
        def climbStairs(self, n: int) -> int:
            if n <= 1:
                return 1
            prev, curr = 1, 1
            for _ in range(2, n + 1):
                prev, curr = curr, prev + curr
            return curr
    """

    def climbStairs(self, n: int) -> int:
        mem = {}

        def solve(n: int) -> int:
            if n < 0:
                return 0
            elif n == 0:
                return 1
            elif n in mem:
                return mem[n]

            mem[n] = solve(n - 1) + solve(n - 2)
            return mem[n]

        return solve(n)
