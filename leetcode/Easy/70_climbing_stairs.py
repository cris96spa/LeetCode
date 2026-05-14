class Solution:
    """Count the distinct ways to climb n stairs taking 1 or 2 steps at a time.

    Problem Statement:
        You are climbing a staircase that takes n steps to reach the top. Each
        time you can either climb 1 or 2 steps. Return the number of distinct
        ways you can climb to the top.

    Approach:
        Use top-down recursion with memoization. Define solve(n) as the number
        of ways to reach step n. Base cases: solve(0) = 1 (one way to stay at
        the bottom), solve(n < 0) = 0. For other n, the result is
        solve(n-1) + solve(n-2), cached in a dictionary to avoid recomputation.
        This is equivalent to computing the (n+1)-th Fibonacci number.

    Complexity:
        Time: O(n), each subproblem is computed exactly once.
        Space: O(n) for the memoization dictionary and the recursion stack.
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
