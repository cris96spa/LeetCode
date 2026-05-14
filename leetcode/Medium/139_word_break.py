class Solution:
    """Determine if string s can be segmented into words from wordDict.

    Problem Statement:
        Given a string s and a dictionary of strings wordDict, return True if s can be
        segmented into a space-separated sequence of one or more dictionary words.

    Approach:
        Dynamic programming. Let dp[i] = True if s[:i] can be formed from wordDict.
        Base case: dp[0] = True. For each position i, check each word; if dp[i-L] is
        True and s[i-L:i] matches the word, set dp[i] = True.

    Complexity:
        Time: O(n * m * L) where n = len(s), m = len(wordDict), L = max word length.
        Space: O(n) for the dp array.
    """

    def wordBreak(self, s: str, wordDict: list[str]) -> bool:
        dp = [False] * (len(s) + 1)
        dp[0] = True

        for i in range(1, len(s) + 1):
            for word in wordDict:
                L = len(word)
                if i >= L and dp[i - L] and s[i - L : i] == word:
                    dp[i] = True
                    break

        return dp[-1]
