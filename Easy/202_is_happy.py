class Solution:
    def isHappy(self, n: int) -> bool:
        """
        Determines if a number n is a happy number.

        A happy number is defined by the following process:
        1. Start with any positive integer.
        2. Replace the number with the sum of the squares of its digits.
        3. Repeat the process until the number equals 1 (where it will stay),
           or it loops endlessly in a cycle which does not include 1.
        4. Those numbers for which this process ends in 1 are happy numbers.

        This function returns True if the given number is a happy number, otherwise False.

        Approach:
        - We use a helper function `get_next` to compute the sum of the squares of the digits.
        - We use a set `seen` to store previously encountered numbers to detect cycles.
        - If we encounter a number we've seen before, a loop exists, and we return False.
        - If we reach 1, we return True.

        Time Complexity: O(log n)
            - The number of digits in `n` is O(log n), and each transformation significantly reduces `n`.
        Space Complexity: O(log n)
            - We store previously seen numbers in a set.

        :param n: int - The number to check for happiness.
        :return: bool - True if `n` is a happy number, False otherwise.
        """

        def get_next(n: int) -> int:
            return sum(int(digit) ** 2 for digit in str(n))

        seen = set()
        while n not in seen:
            seen.add(n)
            n = get_next(n)
            if n == 1:
                return True

        return False
