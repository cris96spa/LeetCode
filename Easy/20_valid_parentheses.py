class Solution:
    """
    20. Valid Parentheses

    Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

    An input string is valid if:
    1. Open brackets must be closed by the same type of brackets.
    2. Open brackets must be closed in the correct order.
    3. Every close bracket has a corresponding open bracket of the same type.

    Example 1:
    Input: s = "()"
    Output: True

    Example 2:
    Input: s = "()[]{}"
    Output: True

    Example 3:
    Input: s = "(]"
    Output: False

    Constraints:
    - 1 <= len(s) <= 10^4
    - s consists of parentheses only: '()[]{}'.

    Approach:
    - Use a stack to track open brackets.
    - Iterate through the string:
        - If an open bracket is found, push it onto the stack.
        - If a closing bracket is found, check if it matches the last open bracket in the stack.
        - If it matches, pop the stack; otherwise, return False.
    - At the end, if the stack is empty, return True; otherwise, return False.

    Time Complexity: O(n), where n = len(s), since we process each character once.
    Space Complexity: O(n), for the stack in the worst case (all open brackets).
    """

    def isValid(self, s: str) -> bool:
        # Base check. If there is an odd number of elements
        # it cannot be a valid string
        if len(s) % 2 != 0:
            return False

        mapping = {"(": ")", "[": "]", "{": "}"}

        stack = []

        for char in s:
            # If the char is an open bracket, push it to the stack
            if char in mapping:
                stack.append(char)
            else:
                # If char is a closing bracket, check if it matches the last opened in the stack
                if stack and mapping.get(stack[-1], None) == char:
                    stack.pop()
                else:
                    # If no match, the string is invalid
                    return False

        # A valid sequence will leave the stack empty
        return len(stack) == 0
