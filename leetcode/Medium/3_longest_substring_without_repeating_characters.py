class Solution:
    """Find the length of the longest substring without repeating characters.

    Problem Statement:
        Given a string s, find the length of the longest substring that contains no
        repeating characters.

    Approach:
        Sliding window with a set. Expand the right pointer; if the new character already
        exists in the window, shrink from the left until the duplicate is removed. Track
        the maximum window size seen.

    Complexity:
        Time: O(n) — each character processed at most twice.
        Space: O(min(n, 128)) — the set holds at most 128 ASCII characters.
    """

    def lengthOfLongestSubstring(self, s: str) -> int:
        if not s:
            return 0

        left, right = 0, 1
        window = {s[left]}
        best_count = 1

        while right < len(s):
            if s[right] not in window:
                window.add(s[right])
                right += 1
            else:
                window.remove(s[left])
                left += 1
            best_count = max(best_count, right - left)

        return best_count
