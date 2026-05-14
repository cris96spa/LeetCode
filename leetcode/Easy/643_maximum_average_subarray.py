from typing import List


class Solution:
    """Find the contiguous subarray of length k with the maximum average value.

    Problem Statement:
        Given an integer array nums and an integer k, find the contiguous
        subarray of length exactly k that has the maximum average value and
        return that value. Answers within 10^-5 of the actual answer are
        accepted.

    Approach:
        Use a sliding window. Compute the sum of the first k elements as the
        initial window. Then slide one position at a time: subtract the element
        leaving the left side and add the element entering the right side. Track
        the maximum sum encountered and return it divided by k.

    Complexity:
        Time: O(n), where n is the length of nums. Each element is processed
            once.
        Space: O(1), only scalar variables are used.
    """

    def findMaxAverage(self, nums: List[int], k: int) -> float:
        curr_sum = sum(nums[:k])
        max_sum = curr_sum

        for i in range(len(nums) - k):
            curr_sum = curr_sum - nums[i] + nums[i + k]
            max_sum = max(max_sum, curr_sum)

        return max_sum / k
