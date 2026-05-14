from typing import List


class Solution:
    """Find the single element that appears once while every other element appears exactly 3 times.

    Problem Statement:
        Given an integer array nums where every element appears exactly three times except for
        one element which appears once. Find and return the single element. Must use O(n) time
        and O(1) space.

    Approach:
        Bit manipulation using two variables 'ones' and 'twos'. Track bits appearing once vs.
        twice. When a bit appears three times, it is cleared from both variables. At the end,
        'ones' holds the unique number.

    Complexity:
        Time: O(n) — single pass through the array.
        Space: O(1) — only two integer variables used.
    """

    def singleNumber(self, nums: List[int]) -> int:
        ones, twos = 0, 0
        for num in nums:
            ones = (ones ^ num) & ~twos
            twos = (twos ^ num) & ~ones
        return ones
