from typing import List


class Solution:
    """Find the contiguous subarray with the largest sum.

    Problem Statement:
        Given an integer array nums, find the subarray with the largest sum and return its sum.

    Approach:
        Kadane's Algorithm: iterate through the array maintaining curr_sum (best sum ending
        here) and max_sum (best seen so far). At each element, decide whether to extend the
        current subarray or start a new one.

    Complexity:
        Time: O(n) — single pass through the array.
        Space: O(1) — only two variables needed.
    """

    def maxSubArray(self, nums: List[int]) -> int:
        max_sum, curr_sum = nums[0], nums[0]

        for num in nums[1:]:
            curr_sum = max(num, curr_sum + num)
            max_sum = max(max_sum, curr_sum)

        return max_sum
