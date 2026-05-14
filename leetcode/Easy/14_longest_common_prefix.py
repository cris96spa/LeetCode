from typing import List


class Solution:
    """Find the longest common prefix among all strings in an array.

    Problem Statement:
        Given an array of strings strs, return the longest common prefix shared
        by all strings. If there is no common prefix, return an empty string.

    Approach:
        Find the minimum string length to bound comparisons. Iterate character
        by character up to that length, checking whether all strings share the
        same character at each position. Stop as soon as a mismatch is found.

    Complexity:
        Time: O(S), where S is the total number of characters across all strings.
            In the worst case every character position is compared.
        Space: O(p), where p is the length of the longest common prefix.
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
