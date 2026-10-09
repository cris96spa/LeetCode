class Solution:
    """🔗 Decode Ways.

    Problem:
    --------
    A message of letters is encoded with `A -> "1"`, `B -> "2"`, ..., `Z -> "26"`. Given the
    digit string `s`, return the number of ways to decode it, or 0 if it can't be decoded.
    Codes are exactly the strings "1".."26": "06" is not a code, so a "0" can only appear
    as the second digit of "10" or "20".

    Key Insight:
    ------------
    This is Word Break (LC 139) with the dictionary {"1", ..., "26"}, counting the ways
    to split instead of asking whether one exists. Let `D[i]` be the number of ways to
    decode the prefix `s[:i]`, and look at the last code of a decoding of `s[:i]`. It is
    either:
    - **One digit** `s[i-1]`: valid if it isn't "0"; the rest is a decoding of `s[:i-1]`,
      giving `D[i-1]` ways.
    - **Two digits** `s[i-2:i]`: valid if it's between "10" and "26"; the rest is a
      decoding of `s[:i-2]`, giving `D[i-2]` ways.

    The two cases end with different codes, so they never count the same decoding twice:

        D[i] = [s[i-1] != "0"] * D[i-1] + ["10" <= s[i-2:i] <= "26"] * D[i-2]

    Base case: `D[0] = 1`. The empty prefix has exactly one decoding (decode nothing),
    so a code that covers the whole prefix counts once. With `D[0] = 0`, every count
    would stay 0.

    Example (`s = "2101"`, answer `D[4] = 1`, the only decoding is 2 10 1):

          i      0   1   2   3   4
          s[:i]  ""  2   21  210 2101
          D[i]   1   1   2   1   1

    `D[3] = 1`: "0" can't be a code on its own, so only "10" works, giving `D[1] = 1`.
    `D[4] = 1`: "01" is not a code, so only "1" works, giving `D[3] = 1`.

    Approach:
    ---------
    - `D[i]` reads only `D[i-1]` and `D[i-2]`, so two variables replace the table, as in
      Climbing Stairs (LC 70). `last_1 = D[i-1]` and `last_2 = D[i-2]`, both starting at
      `D[0] = 1`. Before `i = 2` the two-digit case doesn't apply, so `last_2` isn't read.
    - The range test compares two-character digit strings, so string order is the same
      as numeric order, and "06" < "10" correctly rejects a leading zero.
    - Strings that can't be decoded, such as "0" or "30", need no special case: neither
      code is valid at the stray "0", so the recurrence returns 0.

    Complexity:
    -----------
    - Time: O(n)
    - Space: O(1), down from O(n) for the full table
    """

    def numDecodings(self, s: str) -> int:
        last_2, last_1 = 1, 1

        for i in range(1, len(s) + 1):
            current = 0

            if s[i - 1] != "0":
                current += last_1

            if i >= 2 and "10" <= s[i - 2 : i] <= "26":
                current += last_2

            last_2, last_1 = last_1, current

        return last_1
