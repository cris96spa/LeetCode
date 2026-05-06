class Solution:
    def rob(self, nums: list[int]) -> int:
        """
        Dynamic Programming (House Robber)

        Problem:
        Given a list of non-negative integers representing money in each house,
        determine the maximum amount you can rob without robbing two adjacent houses.

        Approach:
        Let dp[i] represent the maximum money that can be robbed up to house i.

        At each house, we have two choices:
            1. Rob the current house:
               nums[i] + dp[i-2]
            2. Skip the current house:
               dp[i-1]

        Transition:
            dp[i] = max(nums[i] + dp[i-2], dp[i-1])

        Base Cases:
            dp[0] = nums[0]
            dp[1] = max(nums[0], nums[1])

        Space Optimization:
        Instead of maintaining the full DP array, we only track:
            prev_2 → dp[i-2]
            prev_1 → dp[i-1]

        For each house:
            curr = max(nums[i] + prev_2, prev_1)

        Then shift:
            prev_2 = prev_1
            prev_1 = curr

        Final Answer:
            The maximum profit after processing all houses.

        Time Complexity:
            O(n)

        Space Complexity:
            O(1) (optimized version)
            O(n) (if using full DP array)
        """
        n = len(nums)
        if n == 1:
            return nums[0]

        prev_2 = nums[0]
        prev_1 = max(nums[:2])

        for i in range(2, n):
            curr = max(nums[i] + prev_2, prev_1)
            prev_2 = prev_1
            prev_1 = curr

        return max(prev_2, prev_1)
