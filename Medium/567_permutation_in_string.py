from collections import Counter


class Solution:
    """
    567. Permutation in String

    Given two strings s1 and s2, return True if s2 contains a permutation of s1, or False otherwise.
    In other words, return True if one of s1's permutations is a substring of s2.

    Example 1:
    Input: s1 = "ab", s2 = "eidbaooo"
    Output: True
    Explanation: s2 contains one permutation of s1 ("ba").

    Example 2:
    Input: s1 = "ab", s2 = "eidboaoo"
    Output: False

    Constraints:
    - 1 <= len(s1), len(s2) <= 10^4
    - s1 and s2 consist of lowercase English letters.

    Approach:
    - Use a sliding window technique with frequency counting to efficiently check for permutations.
    - Maintain two frequency dictionaries: one for `s1` and another for the current window in `s2`.
    - Slide the window over `s2`, updating the frequency counts dynamically.
    - If at any step both frequency maps match, return True.
    - If no matching window is found, return False.

    Time Complexity: O(n2) where n2 = len(s2), since we only iterate through s2 once.
    Space Complexity: O(1) since the frequency dictionaries have a limited size of 26.
    """

    def checkInclusion(self, s1: str, s2: str) -> bool:
        # Base check
        if len(s1) > len(s2):
            return False

        # Count the frequency of each element of s1
        s1_frequency = Counter(s1)

        # Use a second frequency counter for elements in the sliding window
        window_frequency = Counter()

        # Perform a sliding window approach over s2
        left = 0
        for right in range(len(s2)):
            # Expand the window
            window_frequency[s2[right]] += 1

            # If the size of the window overcome s1, increase left
            if right - left + 1 > len(s1):
                window_frequency[s2[left]] -= 1
                if window_frequency[s2[left]] == 0:
                    del window_frequency[s2[left]]
                left += 1

            if window_frequency == s1_frequency:
                return True

        return False
