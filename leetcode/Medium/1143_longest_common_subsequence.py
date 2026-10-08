class Solution:
    """🔗 Longest Common Subsequence.

    Problem:
    --------
    Given two strings `text1` and `text2`, return the length of their longest common
    subsequence, or 0 if there is none. A subsequence keeps the relative order of the
    characters but may skip some of them.

    Key Insight:
    ------------
    This is Edit Distance (LC 72) with substitution forbidden: the only way to handle a
    mismatched character is to delete it, so the best alignment keeps the most matches.
    Let `D[i][j]` be the LCS length of `text1[:i]` and `text2[:j]`, and look at the last
    characters:
    - **Equal**: they extend the LCS of both prefixes, `D[i][j] = D[i-1][j-1] + 1`.
    - **Different**: at least one of them is not in the LCS, so drop one,
      `D[i][j] = max(D[i-1][j], D[i][j-1])`.

    Base cases: `D[i][0] = D[0][j] = 0` (an empty string has no common subsequence).

    Example (`text1 = "abcde"`, `text2 = "ace"`, answer `D[5][3] = 3`):

              ""  a  c  e
          ""   0  0  0  0
          a    0  1  1  1
          b    0  1  1  1
          c    0  1  2  2
          d    0  1  2  2
          e    0  1  2  3

    Approach:
    ---------
    - Shortcut: identical strings are their own LCS.
    - Row `i` depends only on row `i - 1` (`D[i-1][j]`, `D[i-1][j-1]`) and on the cell to
      its left in row `i` (`D[i][j-1]`), so two rows suffice. Each row starts at
      `D[i][0] = 0` and fills left to right.

    Complexity:
    -----------
    - Time: O(l1 * l2)
    - Space: O(l2), down from O(l1 * l2) for the full table
    """

    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        l1, l2 = len(text1), len(text2)
        if text1 == text2:
            return l1

        prev_row = [0] * (l2 + 1)

        for i in range(1, l1 + 1):
            curr_row = [0] * (l2 + 1)
            for j in range(1, l2 + 1):
                if text1[i - 1] == text2[j - 1]:
                    curr_row[j] = prev_row[j - 1] + 1
                else:
                    curr_row[j] = max(prev_row[j], curr_row[j - 1])
            prev_row = curr_row

        return prev_row[-1]
