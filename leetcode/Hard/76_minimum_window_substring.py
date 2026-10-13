from collections import Counter


class Solution:
    """Return the shortest substring of s that contains every character of t.

    Problem Statement:
        Given two strings s and t, return the minimum window substring of s
        such that every character in t, including duplicates, is included in
        the window. If there is no such substring, return "".

    Example:
        s = "ADOBECODEBANC", t = "ABC"
        -> "BANC"

        s = "a", t = "aa"
        -> ""

    Approach:
        Use a sliding window s[lo..hi]. target_chars counts how many of each
        character the window still needs (negative means surplus), and
        missing_chars counts how many characters of t are still missing in
        total, so checking validity is O(1) instead of comparing counts.

        Extend hi one character at a time. When missing_chars hits 0 the
        window contains all of t: record it if it is the best so far, then
        shrink from lo while the window stays valid. Each shrink gives back
        s[lo]; if that leaves its count positive, a needed character was
        dropped and the window is invalid again.

    Complexity:
        Time: O(m + n), where m = len(s) and n = len(t). Each index enters and
            leaves the window at most once.
        Space: O(k), where k is the number of distinct characters in s and t.
    """

    def minWindow(self, s: str, t: str) -> str:
        if len(s) < len(t):
            return ""

        target_chars = Counter(t)
        missing_chars = len(t)

        lo = 0
        best_lo, best_len = 0, float("inf")

        for hi, char in enumerate(s):
            if target_chars[char] > 0:
                missing_chars -= 1
            target_chars[char] -= 1

            while missing_chars == 0:
                curr_len = hi - lo + 1
                if curr_len < best_len:
                    best_lo, best_len = lo, curr_len

                target_chars[s[lo]] += 1
                if target_chars[s[lo]] > 0:
                    missing_chars += 1
                lo += 1

        if best_len == float("inf"):
            return ""

        return s[best_lo : best_lo + best_len]
