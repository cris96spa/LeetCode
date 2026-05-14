from typing import List


class Solution:
    """Find the single element that appears only once in an array.

    Problem Statement:
        Given a non-empty array of integers nums where every element appears
        twice except for one, find and return that single element. The solution
        must run in O(n) time and use only O(1) extra space.

    Approach:
        Use the XOR bitwise operation. XOR satisfies a ^ a = 0 and a ^ 0 = a,
        and it is commutative and associative. XORing all elements causes every
        duplicate pair to cancel out, leaving only the unique element.

    Complexity:
        Time: O(n), where n is the length of nums.
        Space: O(1), only a single accumulator variable is used.
    """

    def singleNumber(self, nums: List[int]) -> int:
        result = 0
        for num in nums:
            result ^= num
        return result
