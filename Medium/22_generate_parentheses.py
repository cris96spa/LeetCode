from typing import List


class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        """
        Given n pairs of parentheses, generate all possible combinations of well-formed parentheses.

        A well-formed parentheses string means:
        - Every opening parenthesis '(' has a corresponding closing parenthesis ')'.
        - At any point in the string, the number of closing parentheses should not exceed the number of opening parentheses.

        Example 1:
        Input: n = 3
        Output: ["((()))", "(()())", "(())()", "()(())", "()()()"]

        Example 2:
        Input: n = 1
        Output: ["()"]

        Approach:
        - This problem can be solved using a recursive approach with backtracking.
        - We maintain two counters, `open_count` and `closed_count`, to track the number of open and closed parentheses used.
        - We ensure that `open_count` never exceeds `n` and `closed_count` never exceeds `open_count`.
        - If `open_count + closed_count == 2 * n`, a valid sequence is formed and added to the result.

        Complexity Analysis:
        - Time Complexity: O(4^n / sqrt(n)), which follows the nth Catalan number complexity.
        - Space Complexity: O(n) for the recursion stack.
        """

        def backtrack(path: str, open_count: int, closed_count: int):
            if open_count + closed_count == 2 * n:
                result.append(path)
                return

            # Add an opening parenthesis if allowed
            if open_count < n:
                backtrack(path + "(", open_count + 1, closed_count)

            # Add a closing parenthesis if valid
            if closed_count < open_count:
                backtrack(path + ")", open_count, closed_count + 1)

        result = []
        backtrack("", 0, 0)  # Start with an empty string
        return result
