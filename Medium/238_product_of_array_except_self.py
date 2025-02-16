from typing import List


class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        """
        Given an integer array nums, return an array answer such that answer[i] is equal to the
        product of all the elements of nums except nums[i].

        The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.

        Constraints:
        - 2 <= nums.length <= 10^5
        - -30 <= nums[i] <= 30
        - The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.
        - You must write an algorithm that runs in O(n) time and without using the division operation.

        Approach:
        - We use prefix and suffix products to compute the result without division.
        - First, we traverse the array from left to right, storing cumulative left products in the result array.
        - Then, we traverse from right to left, multiplying the stored values by cumulative right products.
        - This approach efficiently computes the result in O(n) time while using only O(1) extra space (excluding output).

        Complexity Analysis:
        - Time Complexity: O(n) (two passes over the array)
        - Space Complexity: O(1) (modifying the result array in-place)

        Example:
        >>> sol = Solution()
        >>> sol.productExceptSelf([1,2,3,4])
        [24, 12, 8, 6]
        """
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
