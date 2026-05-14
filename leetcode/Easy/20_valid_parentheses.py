class Solution:
    """Determine if a string of brackets is valid.

    Problem Statement:
        Given a string s containing only '(', ')', '{', '}', '[', ']', return
        True if the input string is valid. A string is valid when open brackets
        are closed by the same type, closed in the correct order, and every
        closing bracket has a matching open bracket.

    Approach:
        Use a stack. Iterate through the string: push each opening bracket.
        For a closing bracket, check whether it matches the top of the stack.
        If it matches, pop the stack; otherwise return False. After processing,
        the string is valid if and only if the stack is empty.

    Complexity:
        Time: O(n), where n is the length of s. Each character is processed once.
        Space: O(n) for the stack in the worst case (all opening brackets).
    """

    def isValid(self, s: str) -> bool:
        if len(s) % 2 != 0:
            return False

        mapping = {"(": ")", "[": "]", "{": "}"}
        stack = []

        for char in s:
            if char in mapping:
                stack.append(char)
            else:
                if stack and mapping.get(stack[-1], None) == char:
                    stack.pop()
                else:
                    return False

        return len(stack) == 0
