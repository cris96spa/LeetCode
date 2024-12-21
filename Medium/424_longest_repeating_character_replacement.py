class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        """
        Problem Description:
        You are given a string s and an integer k. You can choose any character of the string and change it to any other
        uppercase English character. You can perform this operation at most k times.

        Return the length of the longest substring containing the same letter you can get after performing the above operations.

        Example 1:
        Input: s = "ABAB", k = 2
        Output: 4
        Explanation: Replace the two 'A's with two 'B's or vice versa.

        Example 2:
        Input: s = "AABABBA", k = 1
        Output: 4
        Explanation: Replace the one 'A' in the middle with 'B' and form "AABBBBA".
        The substring "BBBB" has the longest repeating letters, which is 4.

        Constraints:
        - 1 <= s.length <= 10^5
        - s consists of only uppercase English letters.
        - 0 <= k <= s.length
        """

        # Base check
        n = len(s)
        if n <= k:
            return n

        left = 0
        max_len = 0
        char_freq = {}
        max_freq = 0

        # Sliding window approach
        for right in range(n):
            # Increase the count of the current character
            char_freq[s[right]] = char_freq.get(s[right], 0) + 1

            # Update the max frequency of any character in the current window
            max_freq = max(max_freq, char_freq[s[right]])

            # Check if the current window size minus the most frequent character count exceeds k
            while right - left + 1 - max_freq > k:
                # Decrement the frequency of the leftmost character and shrink the window
                char_freq[s[left]] -= 1
                left += 1

            # Update the maximum length of the valid substring
            max_len = max(max_len, right - left + 1)

        return max_len


# Write-up:
# The solution employs a sliding window approach to efficiently find the longest substring where at most k replacements
# allow all characters to become the same. The algorithm maintains a frequency map (char_freq) to track character counts
# within the current window and a variable (max_freq) to record the frequency of the most common character in the window.
#
# The window is expanded by moving the `right` pointer across the string. If the window becomes invalid (i.e.,
# the number of characters to be replaced exceeds k), the `left` pointer is incremented to shrink the window
# and restore validity. Throughout the process, the maximum valid window size is recorded.
#
# This approach ensures an O(n) time complexity as each character is processed at most twice (once by the `right` pointer
# and once by the `left` pointer). The space complexity is O(1) since the frequency map size is limited to the alphabet size (26).
