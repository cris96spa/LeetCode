
class Solution:
    def minCostClimbingStairs(self, cost: list[int]) -> int:
        """
            Use dynamic programming with space optimization.

            At each step i, the minimum cost to reach it is:
                cost[i] + min(cost to reach i-1, cost to reach i-2)

            We keep only two variables:
                prev_1 → min cost to reach previous step
                prev_2 → min cost to reach step before that

            Iterate through the array, updating the current cost each time.

            Since we can end on either of the last two steps to reach the top,
            the result is:
                min(prev_1, prev_2)

            Time: O(n)
            Space: O(1)
        """
        prev_2 = 0
        prev_1 = cost[0]
        for i in range(1, len(cost)):
            curr_cost = cost[i] + min(prev_1, prev_2)
            prev_2 = prev_1
            prev_1 = curr_cost

        return min(prev_1, prev_2)