class Solution:
    """Find the minimum cost to reach the top of the staircase.

    Problem Statement:
        You are given an integer array cost where cost[i] is the cost of the
        i-th step. Once you pay the cost, you can climb one or two steps. You
        can start from index 0 or index 1. Return the minimum cost to reach the
        floor beyond the top of the staircase.

    Approach:
        Use space-optimized dynamic programming. At each step i, the minimum
        cost to reach it is cost[i] + min(cost to reach i-1, cost to reach i-2).
        Keep only two variables (prev_2 and prev_1) instead of a full DP array.
        The answer is min(prev_1, prev_2) since we can finish from either of the
        last two steps.

    Complexity:
        Time: O(n), where n is the length of cost.
        Space: O(1), only two scalar variables are maintained.
    """

    def minCostClimbingStairs(self, cost: list[int]) -> int:
        prev_2 = 0
        prev_1 = cost[0]
        for i in range(1, len(cost)):
            curr_cost = cost[i] + min(prev_1, prev_2)
            prev_2 = prev_1
            prev_1 = curr_cost

        return min(prev_1, prev_2)
