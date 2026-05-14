from typing import List


class Solution:
    """Return an array where each element is the product of all other elements in nums.

    Problem Statement:
        Given an integer array nums, return answer where answer[i] equals the product of all
        elements except nums[i]. Must run in O(n) time without using division.

    Approach:
        Two-pass prefix/suffix product. First pass stores cumulative left products in result.
        Second pass (right to left) multiplies by cumulative right products in-place.

    Complexity:
        Time: O(n) — two passes over the array.
        Space: O(1) extra (output array not counted).
    """

    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        result = [1] * n

        left_prod = 1
        for i in range(n):
            result[i] = left_prod
            left_prod *= nums[i]

        right_prod = 1
        for i in range(n - 1, -1, -1):
            result[i] *= right_prod
            right_prod *= nums[i]

        return result
