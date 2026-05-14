class Solution:
    """Determine if a string is a valid palindrome.

    Problem Statement:
        Given a string s, return True if it is a palindrome considering only
        alphanumeric characters and ignoring case, False otherwise. A palindrome
        reads the same forward and backward after filtering.

    Approach:
        Filter the string to keep only lowercase alphanumeric characters. Then
        use two pointers starting from both ends, moving inward and comparing
        characters. If any pair differs, return False; otherwise return True.

    Complexity:
        Time: O(n), where n is the length of s. The string is scanned twice:
            once to filter and once to check.
        Space: O(n) for storing the filtered character list.
    """

    def isPalindrome(self, s: str) -> bool:
        filtered_chars = [c.lower() for c in s if c.isalnum()]
        start, end = 0, len(filtered_chars) - 1
        while start < end:
            if filtered_chars[start] != filtered_chars[end]:
                return False
            start += 1
            end -= 1
        return True
