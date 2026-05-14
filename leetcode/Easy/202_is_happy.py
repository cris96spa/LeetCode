class Solution:
    """Determine whether a positive integer is a happy number.

    Problem Statement:
        A happy number is defined by the following process: start with any
        positive integer, replace it with the sum of squares of its digits,
        and repeat. If the process eventually reaches 1, the number is happy.
        If it enters an infinite cycle that never reaches 1, it is not happy.

    Approach:
        Use a set to track previously seen values. On each step, compute the
        sum of squares of the digits. If the result is 1, return True. If it
        has appeared before, a cycle exists and we return False.

    Complexity:
        Time: O(log n) per iteration; the cycle length before detection is
            bounded by O(log n) distinct values.
        Space: O(log n) for the set of previously seen values.
    """

    def isHappy(self, n: int) -> bool:
        def get_next(n: int) -> int:
            return sum(int(digit) ** 2 for digit in str(n))

        seen = set()
        while n not in seen:
            seen.add(n)
            n = get_next(n)
            if n == 1:
                return True

        return False
