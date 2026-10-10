from typing import List


class Solution:
    """Find the maximum amount of money you can rob from houses arranged in a circle.

    Problem Statement:
        Given an array nums of house values arranged in a circle, return the maximum money
        you can rob without alerting the police (no two adjacent houses can be robbed). Since
        houses are circular, the first and last houses are also adjacent.

    Approach:
        Reduce to two linear House Robber problems: one excluding the first house, one
        excluding the last. Take the maximum of the two results. Use dynamic programming
        with two variables to track prev and current max.

    Complexity:
        Time: O(n) — two linear scans.
        Space: O(1) — only two variables used.
    """

    def rob(self, nums: List[int]) -> int:
        if len(nums) == 1:
            return nums[0]

        return max(self._get_max(nums[:-1]), self._get_max(nums[1:]), nums[0])

    def _get_max(self, nums: List[int]) -> int:
        prev_rob = max_rob = 0
        for curr in nums:
            temp = max(max_rob, prev_rob + curr)
            prev_rob = max_rob
            max_rob = temp
        return max_rob
