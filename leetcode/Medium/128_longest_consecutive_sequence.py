from typing import List


class Solution:
    """Find the length of the longest consecutive elements sequence in an unsorted array.

    Problem Statement:
        Given an unsorted array of integers nums, return the length of the longest consecutive
        sequence. The algorithm must run in O(n) time.

    Approach:
        Convert nums to a set for O(1) lookups. For each number that is the start of a
        sequence (n-1 not in set), count consecutive values until the chain breaks.
        Track the maximum count seen.

    Complexity:
        Time: O(n) — each number processed at most twice.
        Space: O(n) for the set.
    """

    def longestConsecutive(self, nums: List[int]) -> int:
        if not nums:
            return 0

        numbers = set(nums)
        max_count = 0

        for n in numbers:
            if n - 1 not in numbers:
                curr_count = 1
                next_num = n + 1
                while next_num in numbers:
                    next_num += 1
                    curr_count += 1
                max_count = max(max_count, curr_count)

        return max_count
