class Solution:
    """✏️ Edit Distance.

    Problem:
    --------
    Given two strings `word1` and `word2`, return the minimum number of operations needed
    to convert `word1` into `word2`. Allowed operations, each on a single character:
    insert, delete, replace.

    Key Insight:
    ------------
    Ask only what happens to the **last characters**. Let `D[i][j]` be the edit distance
    between `word1[:i]` and `word2[:j]`. In an optimal sequence of edits, the last one is:
    - **Replace / match** `word1[i-1]` with `word2[j-1]`: `D[i-1][j-1] + (chars differ)`.
    - **Insert** `word2[j-1]`: `D[i][j-1] + 1`.
    - **Delete** `word1[i-1]`: `D[i-1][j] + 1`.

    `D[i][j]` is the min of the three. Base cases: `D[i][0] = i` (delete everything) and
    `D[0][j] = j` (insert everything). There are only `(l1 + 1) * (l2 + 1)` states, each
    filled in O(1).

    Example (`word1 = "horse"`, `word2 = "ros"`, answer `D[5][3] = 3`):

              ""  r  o  s
          ""   0  1  2  3
          h    1  1  2  3
          o    2  2  1  2
          r    3  2  2  2
          s    4  3  3  2
          e    5  4  4  3

    Approach:
    ---------
    Row `i` depends only on row `i - 1` (`D[i-1][j]`, `D[i-1][j-1]`) and on the cell to
    its left in row `i` (`D[i][j-1]`), so two rows suffice:
    - `prev_row` starts as row 0: `[0, 1, ..., l2]`.
    - Each new row starts with `D[i][0] = i`, then fills left to right.
    Reconstructing the actual edits would need the full table.

    Complexity:
    -----------
    - Time: O(l1 * l2)
    - Space: O(l2), down from O(l1 * l2) for the full table
    """

    def minDistance(self, word1: str, word2: str) -> int:
        l1, l2 = len(word1), len(word2)
        prev_row = list(range(l2 + 1))

        for i in range(1, l1 + 1):
            current_row = [i] + [0] * l2
            for j in range(1, l2 + 1):
                delete = prev_row[j] + 1
                insert = current_row[j - 1] + 1
                replace = prev_row[j - 1] + (word1[i - 1] != word2[j - 1])
                current_row[j] = min(delete, insert, replace)
            prev_row = current_row

        return prev_row[-1]
