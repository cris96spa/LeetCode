from bisect import bisect_left


class Solution:
    """✉️ Russian Doll Envelopes.

    Problem:
    --------
    Given `envelopes[i] = [w_i, h_i]`, an envelope fits inside another iff **both** its
    width and its height are strictly smaller. Envelopes can't be rotated. Return the
    maximum number of envelopes that can be nested one inside the other.

    Key Insight:
    ------------
    A nesting chain is a sequence that strictly increases in both dimensions. Sort by
    width, and the chain becomes a subsequence of the sorted list, so the problem looks
    like LIS (LC 300) on the heights. Ties in width are the catch: two envelopes with the
    same width never nest, but if equal widths are sorted by height ascending, LIS on the
    heights happily chains them:

        [[1, 1], [1, 2], [1, 3]]   heights 1, 2, 3 -> LIS 3, but the answer is 1

    Fix: sort by width ascending and, within equal widths, by height **descending**.
    Then:
    - **Every strictly increasing height subsequence is a valid chain.** Within a group
      of equal widths, heights decrease, so the subsequence takes at most one envelope
      from each group. Its widths therefore strictly increase too.
    - **Every chain appears as such a subsequence.** A chain has strictly increasing
      widths, so its envelopes come from different groups, in sorted order, with
      strictly increasing heights.

    So the answer is exactly the LIS of the heights in this order, and the width
    dimension disappears.

    Example (`envelopes = [[5, 4], [6, 4], [6, 7], [2, 3]]`, answer 3):

          sorted (w asc, h desc):  [2, 3]  [5, 4]  [6, 7]  [6, 4]
          heights:                    3       4       7       4

    The LIS of the heights is 3, 4, 7: the chain [2, 3] -> [5, 4] -> [6, 7]. With heights
    ascending inside the width-6 group (..., [6, 4], [6, 7]), the order would be
    3, 4, 4, 7, and any LIS through both width-6 envelopes would be wrong.

    Approach:
    ---------
    The O(n^2) LIS (`length[i]` = longest chain *ending at* envelope `i`, answer
    `max(length)`) is too slow for n up to 1e5. Use the patience-sorting LIS from LC 300
    instead:

        tails[k] = smallest last height of any increasing subsequence of length k + 1

    For each height `h`, `k = bisect_left(tails, h)` is the first tail `>= h`: append if
    `h` beats every tail, otherwise `h` becomes the new smallest tail for length `k + 1`.
    `bisect_left` keeps the increase strict, as the strict nesting rule requires.

          h     k     tails
          3     0     [3]
          4     1     [3, 4]
          7     2     [3, 4, 7]
          4     1     [3, 4, 7]     (equal to tails[1]: replaces it, doesn't extend)

    Complexity:
    -----------
    - Time: O(n log n), for the sort and one binary search per envelope
    - Space: O(n)
    """

    def maxEnvelopes(self, envelopes: list[list[int]]) -> int:
        envelopes = sorted(envelopes, key=lambda x: (x[0], -x[1]))

        # tails[k] is the smallest possible last height of an increasing subsequence of k + 1 envelopes
        tails = []

        for i in range(len(envelopes)):
            height = envelopes[i][1]
            k = bisect_left(tails, height)
            if k == len(tails):
                tails.append(height)
            else:
                tails[k] = height

        return len(tails)
