from typing import List


class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        """
        Given a non-empty array of integers `nums`, every element appears twice except for one.
        Find that single one.

        Problem Description:
        -------------------
        Each element in the array `nums` appears exactly twice, except for one unique element that
        appears only once. The goal is to find and return the element that appears once.

        Constraints:
        ------------
        - The array is guaranteed to have a single unique element.
        - You must implement the solution with a linear runtime complexity (O(n)).
        - You must use only constant extra space (O(1)).

        Approach:
        ---------
        1. Use the XOR operation to identify the unique number:
           - XOR properties:
             - `a ^ a = 0` (a number XORed with itself is 0)
             - `a ^ 0 = a` (a number XORed with 0 remains unchanged)
             - XOR is commutative and associative.
           - By XORing all elements in the array, duplicate elements cancel out, leaving only the
             unique element.

        Parameters:
        -----------
        nums (List[int]): A list of integers where every element appears twice except for one.

        Returns:
        --------
        int: The single element that appears only once.

        Examples:
        ---------
        Input: nums = [4, 1, 2, 1, 2]
        Output: 4

        Input: nums = [2, 2, 1]
        Output: 1

        Input: nums = [1]
        Output: 1
        """
        result = 0
        for num in nums:
            result ^= num

        return result
