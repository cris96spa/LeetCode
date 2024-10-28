from typing import List


class Solution:
    """
    Problem:
    Given an array of strings, find the longest common prefix among them. If there is no common prefix, return an empty string.

    Examples:
    - Example 1:
        Input: ["flower", "flow", "flight"]
        Output: "fl"

    - Example 2:
        Input: ["dog", "racecar", "car"]
        Output: ""
        Explanation: There is no common prefix among the input strings.

    Solution:
    This algorithm determines the longest common prefix by:
    1. Finding the minimum string length in the array to restrict character comparisons to the shortest string length.
    2. Iterating over each character position up to this length.
    3. Checking if all strings contain the same character at each position.
    4. Adding the character to the result if all strings match at that position; if any string does not match, the loop breaks.

    Complexity:
    - Time Complexity: O(S), where S is the sum of all characters in all strings. Each character position up to the shortest string length is compared.
    - Space Complexity: O(N), where N is the length of the longest common prefix.

    Returns:
    The longest common prefix as a string.
    """

    def longestCommonPrefix(self, strs: List[str]) -> str:
        if not strs:
            return ""

        min_len = min(len(s) for s in strs)
        output = []

        for i in range(min_len):
            char = strs[0][i]
            if all(s[i] == char for s in strs[1:]):
                output.append(char)
            else:
                break

        return "".join(output)
