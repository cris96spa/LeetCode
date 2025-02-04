class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        """
        Given a string `s`, find the length of the longest substring
        without repeating characters.

        Constraints:
        - 0 <= len(s) <= 5 * 10^4
        - `s` consists of English letters, digits, symbols, and spaces.

        Approach:
        - We use a **sliding window** technique with two pointers (`left` and `right`).
        - Maintain a **set** to track unique characters in the current window.
        - Expand `right` to grow the window while there are no repeating characters.
        - If a duplicate character is found, move `left` forward to remove it
          from the window and continue expanding `right`.
        - Track the **maximum window size** encountered.

        Complexity Analysis:
        - **Time Complexity: O(n)** — Each character is processed at most twice
          (once when added, once when removed).
        - **Space Complexity: O(min(n, 128))** — The set stores at most 128
          ASCII characters.

        Edge Cases Considered:
        - An empty string (`s = ""`) should return `0`.
        - A string with all unique characters (`s = "abcdef"`) should return `len(s)`.
        - A string with all repeated characters (`s = "aaaaaa"`) should return `1`.
        - A long string with repeating patterns (`s = "abcabcbb"`) should return `3`.

        Example:
        ```
        Input: s = "abcabcbb"
        Output: 3
        Explanation: The longest substring is "abc" with length 3.
        ```

        Returns:
        - An integer representing the length of the longest substring without repeating characters.
        """

        if not s:
            return 0  # Edge case: empty string

        left, right = 0, 1
        window = set(s[left])  # Initialize set with the first character
        best_count = 1

        while right < len(s):
            if s[right] not in window:  # If character is unique, expand window
                window.add(s[right])
                right += 1
            else:
                window.remove(s[left])  # Remove leftmost character and shrink window
                left += 1

            best_count = max(best_count, right - left)  # Track max window size

        return best_count
