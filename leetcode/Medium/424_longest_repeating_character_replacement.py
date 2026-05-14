class Solution:
    """Find the length of the longest substring with at most k character replacements.

    Problem Statement:
        Given a string s and integer k, you can replace any character at most k times. Return
        the length of the longest substring containing the same letter after performing the
        operations.

    Approach:
        Sliding window. Maintain a frequency map and the max frequency in the window.
        If (window size - max frequency) > k, shrink the window from the left. Track
        the maximum valid window length throughout.

    Complexity:
        Time: O(n) — each character processed at most twice.
        Space: O(1) — frequency map bounded by alphabet size (26).
    """

    def characterReplacement(self, s: str, k: int) -> int:
        n = len(s)
        if n <= k:
            return n

        left = 0
        max_len = 0
        char_freq: dict[str, int] = {}
        max_freq = 0

        for right in range(n):
            char_freq[s[right]] = char_freq.get(s[right], 0) + 1
            max_freq = max(max_freq, char_freq[s[right]])

            while right - left + 1 - max_freq > k:
                char_freq[s[left]] -= 1
                left += 1

            max_len = max(max_len, right - left + 1)

        return max_len
