class Solution:
    """Convert a Roman numeral string to its integer equivalent.

    Problem Statement:
        Roman numerals use seven symbols: I(1), V(5), X(10), L(50), C(100),
        D(500), M(1000). They are written largest to smallest from left to right.
        However, when a smaller symbol appears before a larger one, it is
        subtracted (e.g. IV=4, IX=9, XL=40, XC=90, CD=400, CM=900). Given a
        valid Roman numeral string in the range [1, 3999], convert it to an int.

    Approach:
        Iterate through the string. For each character, look up its integer
        value. If it is smaller than the value of the next character, subtract
        it from the running total; otherwise add it. This single pass handles
        all subtraction rules correctly.

    Complexity:
        Time: O(n), where n is the length of the input string.
        Space: O(1), only a fixed-size mapping dictionary is used.
    """

    def romanToInt(self, s: str) -> int:
        mapping = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}

        summ = 0
        for i in range(len(s)):
            num = mapping[s[i]]
            if i + 1 < len(s) and num < mapping[s[i + 1]]:
                summ -= num
            else:
                summ += num
        return summ
