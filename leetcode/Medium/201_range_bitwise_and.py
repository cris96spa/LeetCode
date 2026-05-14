class Solution:
    """Return the bitwise AND of all numbers in the range [left, right] inclusive.

    Problem Statement:
        Given two integers left and right representing the range [left, right], return
        the bitwise AND of all numbers in this range.

    Approach:
        Right-shift both left and right until they are equal. The number of shifts is
        the count of trailing bits that differ. Shift the common prefix back left to
        restore its original position.

    Complexity:
        Time: O(log(max(left, right))) — repeated bit shifts.
        Space: O(1).
    """

    def rangeBitwiseAnd(self, left: int, right: int) -> int:
        shift = 0
        while left < right:
            left >>= 1
            right >>= 1
            shift += 1
        return left << shift
