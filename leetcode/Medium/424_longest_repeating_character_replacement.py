class Solution:
    """Find the length of the longest substring with at most k character replacements.

    Problem Statement:
        Given a string s and integer k, you can replace any character at most k times. Return
        the length of the longest substring containing the same letter after performing the
        operations.

    Approach:
        Sliding window. Maintain a frequency map and the max frequency in the window.
        If (window size - max frequency) > k, the characters that differ from the most
        frequent one cannot all be replaced in k moves, so shrink the window from the left.

        max_freq is never decreased when the window shrinks, so it ends up as the highest
        count of a single character reached by any valid window. That window holds max_freq
        copies plus at most k others, so extending it with any neighbours up to length
        max_freq + k still needs at most k replacements. Hence the answer is
        min(max_freq + k, len(s)), with no need to track the best window length.

    Complexity:
        Time: O(n) — each character enters and leaves the window at most once.
        Space: O(1) — frequency map bounded by alphabet size (26).
    """

    def characterReplacement(self, s: str, k: int) -> int:
        window: dict[str, int] = {}
        lo, max_freq = 0, 0

        for hi, char in enumerate(s):
            window[char] = window.get(char, 0) + 1
            max_freq = max(max_freq, window[char])

            while hi - lo + 1 - max_freq > k:
                window[s[lo]] -= 1
                lo += 1

        return min(max_freq + k, len(s))
