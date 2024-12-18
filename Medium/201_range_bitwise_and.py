class Solution:
    def rangeBitwiseAnd(left, right):
        """
        Given two integers left and right that represent the range [left, right],
        return the bitwise AND of all numbers in this range, inclusive.

        Approach:
        - Keep shifting both `left` and `right` to the right until they are equal.
        - The number of shifts corresponds to the number of trailing bits that differ.
        - The result is the common prefix, shifted back to its original position.

        Example:
        Input: left = 5, right = 7
        Output: 4

        Input: left = 1, right = 2147483647
        Output: 0

        Constraints:
        - 0 <= left <= right <= 2^31 - 1

        Time Complexity: O(log(max(left, right))), since we are repeatedly shifting bits.
        Space Complexity: O(1), as no additional data structures are used.
        """
        shift = 0
        # Find the common prefix by shifting
        while left < right:
            left >>= 1
            right >>= 1
            shift += 1
        # Shift the result back to its original position
        return left << shift
