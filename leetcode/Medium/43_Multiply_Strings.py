class Solution:
    """Multiply two non-negative integers represented as strings and return the result as a string.

    Problem Statement:
        Given two non-negative integers num1 and num2 represented as strings, return the product
        as a string. Must not convert inputs directly to integers or use built-in BigInteger libs.

    Approach:
        Convert each string digit-by-digit to an integer by accumulating positional values, then
        multiply the two integers and convert the result back to a string.

    Complexity:
        Time: O(n + m) where n and m are the lengths of num1 and num2.
        Space: O(1) extra space beyond the result string.
    """

    def multiply(self, num1: str, num2: str) -> str:
        x = 0
        for i, num in enumerate(reversed(num1)):
            x += int(num) * 10**i

        y = 0
        for i, num in enumerate(reversed(num2)):
            y += int(num) * 10**i

        return str(x * y)
