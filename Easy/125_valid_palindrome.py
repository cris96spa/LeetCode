class Solution:
    """
    Given a string s, determine if it is a palindrome, considering only alphanumeric characters
    and ignoring cases. A string is a palindrome if it reads the same backward as forward after
    filtering out non-alphanumeric characters and converting all uppercase letters to lowercase.

    This solution filters the input string to include only lowercase alphanumeric characters, then
    uses a two-pointer approach to check if the resulting sequence reads the same forwards and backwards.

    Example:
        Input: "A man, a plan, a canal: Panama"
        Output: True

    Example:
        Input: "race a car"
        Output: False

    Complexity:
        - Time Complexity: O(n), where n is the length of the input string, as we iterate over the string twice
          (once for filtering and once for checking palindrome).
        - Space Complexity: O(n), due to the additional space required to store the filtered characters.

    Constraints:
        - 1 <= s.length <= 2 * 10^5
        - s consists only of printable ASCII characters.
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
