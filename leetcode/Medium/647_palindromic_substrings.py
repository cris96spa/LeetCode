class Solution:
    """LeetCode 647. Palindromic Substrings.

    Given a string s, return the number of palindromic substrings in it.

    A palindrome reads the same backward and forward.

    Approach:
    Every palindrome can be identified by its center.

    There are two possible types of centers:
    1. A single character, for odd-length palindromes.
       Example: "aba" has center "b".
    2. A gap between two characters, for even-length palindromes.
       Example: "abba" has center between the two "b"s.

    For each index i, we expand around:
    - (i, i) to count odd-length palindromes
    - (i, i + 1) to count even-length palindromes

    During expansion, whenever s[left] == s[right], the substring
    s[left:right + 1] is a palindrome, so we increase the count.

    Complexity:
    Time: O(n^2)
        For each of the n possible centers, expansion may take O(n)
        in the worst case.

    Space: O(1)
        We only use a few integer variables.
    """

    def countSubstrings(self, s: str) -> int:
        n = len(s)

        def expand(left: int, right: int) -> int:
            count = 0

            while left >= 0 and right < n and s[left] == s[right]:
                count += 1
                left -= 1
                right += 1

            return count

        total = 0

        for i in range(n):
            total += expand(i, i)
            total += expand(i, i + 1)

        return total
