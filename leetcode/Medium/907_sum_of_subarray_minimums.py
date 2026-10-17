class Solution:
    """Sum the minimum of every contiguous subarray.

    Problem Statement:
        Given an array of integers arr, return the sum of min(b), where b
        ranges over every contiguous subarray of arr, modulo 10^9 + 7.

    Example:
        arr = [3, 1, 2, 4]
        -> 17 (mins: 3, 1, 2, 4, 1, 1, 2, 1, 1, 1)

    Approach:
        Brute force extends each start with a running minimum: O(n^2).

        Flip the question: for how many subarrays is arr[i] the minimum? Let
        L be the index of the previous smaller element and R the index of the
        next smaller-or-equal one. arr[i] is the minimum of every subarray
        starting in (L, i] and ending in [i, R), so it contributes
        arr[i] * (i - L) * (R - i). Using strict on one side and non-strict
        on the other counts each subarray with repeated minima exactly once.

        A monotonic increasing stack of indices finds both bounds in one
        pass. When arr[right] <= arr[stack[-1]], pop i: right is its R, and
        the new top (or -1) is its L. A trailing 0 sentinel flushes the
        stack at the end, since all values are positive. This is needed
        to ensure that all elements are processed. In case the array ends with increasing
        elements, adding a sentinel that has the smallest possible value (0 in this case)
        ensure everything is processed correctly.

    Complexity:
        Time: O(n), each index is pushed and popped at most once.
        Space: O(n) for the stack.
    """

    def sumSubarrayMins(self, arr: list[int]) -> int:
        stack: list[int] = []
        total = 0

        for right, value in enumerate([*arr, 0]):
            while stack and arr[stack[-1]] >= value:
                i = stack.pop()
                left = stack[-1] if stack else -1
                total += arr[i] * (i - left) * (right - i)
            stack.append(right)

        return total % (10**9 + 7)
