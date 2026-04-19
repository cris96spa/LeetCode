class Solution:
    def wordBreak(self, s: str, wordDict: list[str]) -> bool:
        """
        Return True if `s` can be segmented into a sequence of one or more
        words from `wordDict`, otherwise return False.

        Dynamic programming idea:
        Let `dp[i]` mean whether the prefix `s[:i]` can be formed using words
        from `wordDict`.

        Base case:
        - `dp[0] = True` because the empty prefix is always segmentable.

        Transition:
        For each position `i` from 1 to `len(s)`, check every word in
        `wordDict`.
        If:
        1. the word has length `L` such that `i >= L`,
        2. the prefix before that word is segmentable, meaning `dp[i - L]` is True,
        3. the suffix `s[i - L:i]` matches the current word,

        then `dp[i] = True`.

        Intuition:
        A prefix `s[:i]` is segmentable if we can split it into:
        - a previously segmentable prefix `s[:i-L]`
        - followed by a dictionary word `s[i-L:i]`

        Example:
        s = "mydpsolution"
        wordDict = ["dp", "solution", "my"]

        dp[0] = True
        dp[2] = True   because "my" is in wordDict
        dp[4] = True   because dp[2] is True and "dp" matches
        dp[12] = True  because dp[4] is True and "solution" matches

        Therefore the answer is True.

        Complexity:
        - Time: O(n * m * L) in the worst case
          where:
          n = len(s),
          m = len(wordDict),
          L = maximum length of a word in wordDict
          Since each word length is at most 20, this is efficient enough.
        - Space: O(n)

        Notes:
        - The same dictionary word may be used multiple times.
        - This is similar in spirit to coin change / reachability DP:
          each state asks whether the current prefix can be reached from
          an earlier valid state by appending one valid word.
        """
        dp = [False] * (len(s) + 1)
        dp[0] = True

        for i in range(1, len(s) + 1):
            for word in wordDict:
                L = len(word)
                if i >= L and dp[i - L] and s[i - L:i] == word:
                    dp[i] = True
                    break

        return dp[-1]