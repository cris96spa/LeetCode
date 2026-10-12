class Solution:
    """🪞 Longest Palindromic Substring.

    Problem:
    --------
    Given a string `s` (digits and English letters, `len(s) <= 1000`), return the longest
    palindromic substring in `s`.

    Example (`s = "babad"`, answer `"bab"`; `"aba"` is also valid).
    Example (`s = "cbbd"`, answer `"bb"`).

    Key Insight:
    ------------
    Checking one string is easy: two pointers from the ends, stop at the first mismatch.
    But we need the longest over all substrings, so instead grow palindromes **outward
    from their center**: <--lo-- center --hi--> until the chars differ or a border is hit.

    Every palindrome has exactly one center, and there are two kinds:
    - a character, for odd lengths (`"aba"`): start with `expand(i, i)`
    - a gap between two characters, for even lengths (`"abba"`): start with
      `expand(i, i + 1)`

    That gives `2n - 1` centers, and trying all of them covers every palindrome.
    Same expansion as 647 (Palindromic Substrings), but tracking the longest instead of
    counting.

    Approach:
    ---------
    - When the loop stops, `lo` and `hi` are one step **past** the palindrome, so it
      spans `s[lo + 1:hi]` with length `hi - lo - 1`.
    - An even center with `s[i] != s[i + 1]` returns length 0, so it never wins.

    Complexity:
    -----------
    - Time: O(n^2), `2n - 1` centers, each expansion O(n)
    - Space: O(1), apart from the returned substring
    """

    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        best_start = 0
        max_len = 0

        def expand(lo: int, hi: int) -> tuple[int, int]:
            while lo >= 0 and hi < n and s[lo] == s[hi]:
                lo -= 1
                hi += 1

            start = lo + 1
            seq_len = hi - lo - 1
            return start, seq_len

        for pivot in range(n):
            # Odd-length palindromes
            start1, len1 = expand(pivot, pivot)

            # Even-length palindromes
            start2, len2 = expand(pivot, pivot + 1)

            if len1 > max_len:
                best_start = start1
                max_len = len1

            if len2 > max_len:
                best_start = start2
                max_len = len2

        return s[best_start : best_start + max_len]
