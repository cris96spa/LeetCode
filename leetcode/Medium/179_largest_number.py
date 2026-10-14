from functools import cmp_to_key


class Solution:
    """Arrange non-negative integers to form the largest possible number.

    Problem Statement:
        Given a list of non-negative integers nums, arrange them such that
        they form the largest number and return it. Since the result may be
        very large, return it as a string.

    Example:
        nums = [10, 2]
        -> "210"

        nums = [3, 30, 34, 5, 9]
        -> "9534330"

    Approach:
        Sorting by numeric value fails ([3, 30] would give "303", not "330"),
        and plain string order fails too ("30" > "3" but "3" should go first).
        Instead, compare two strings a and b by the number they form together:
        a goes before b when a + b > b + a. This order is transitive, so
        sorting with it puts every pair in the best relative order.

        If the first string after sorting is "0", every number is 0 and the
        answer is "0" rather than "00...0".

    Complexity:
        Time: O(n log n * L), where n = len(nums) and L is the maximum number
            of digits. Each comparison concatenates two strings of length up
            to L.
        Space: O(n * L) for the string representations.
    """

    def largestNumber(self, nums: list[int]) -> str:

        strings = list(map(str, nums))

        def compare(a: str, b: str) -> int:
            if a + b > b + a:
                return -1
            elif b + a > a + b:
                return 1
            else:
                return 0

        strings.sort(key=cmp_to_key(compare))
        return "0" if strings[0] == "0" else "".join(strings)
