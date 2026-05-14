from typing import List


class Solution:
    """Find two indices in an array whose values sum to the target.

    Problem Statement:
        Given an array of integers nums and an integer target, return indices of
        the two numbers such that they add up to target. Each input has exactly
        one solution, and the same element may not be used twice.

    Approach:
        Use a hash map to store each number and its index as we iterate. For
        each element, compute its complement (target - current). If the complement
        already exists in the map, return the two indices. Otherwise, store the
        current number and its index and continue.

    Complexity:
        Time: O(n), where n is the length of nums. Each element is visited once.
        Space: O(n) for the hash map storing up to n elements.
    """

    def twoSum(self, nums: List[int], target: int) -> List[int]:
        sum_dict = {}
        for i in range(len(nums)):
            diff = target - nums[i]
            if diff in sum_dict:
                return [i, sum_dict[diff]]
            sum_dict[nums[i]] = i

        return []
