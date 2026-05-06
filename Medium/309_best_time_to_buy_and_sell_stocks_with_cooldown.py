class Solution:
    """
    Best Time to Buy and Sell Stock with Cooldown

    Problem:
        You are given an array `prices` where `prices[i]` is the stock price on day `i`.

        You may complete as many transactions as you want, but with two constraints:
        1. You must sell before buying again.
        2. After selling, you cannot buy on the next day because of a 1-day cooldown.

        Return the maximum profit you can achieve.

    Intuition:
        The decision at day `i` does not depend only on the day index, but also on the
        "state" we are in at the end of that day.

        A single `dp[i]` is not enough, because the best profit at day `i` is different
        depending on whether:
        - we are currently holding a stock,
        - we have just sold a stock,
        - we are resting (no stock in hand and not in cooldown).

        This naturally leads to a small DP state machine.

    DP states:
        Let:

        - hold[i]:
            Maximum profit at the end of day `i` if we are holding one stock.

        - sold[i]:
            Maximum profit at the end of day `i` if we sold a stock today.
            This state implies that the next day will be a cooldown day.

        - rest[i]:
            Maximum profit at the end of day `i` if we are not holding a stock
            and we are not in cooldown.

    Transitions:
        For each day `i > 0`:

        1. hold[i]
           To end day `i` holding a stock, there are only two possibilities:
           - we were already holding yesterday,
           - or we were resting yesterday and we buy today.

           hold[i] = max(hold[i - 1], rest[i - 1] - prices[i])

        2. sold[i]
           To sell today, we must have been holding yesterday.

           sold[i] = hold[i - 1] + prices[i]

        3. rest[i]
           To end today resting, there are two possibilities:
           - we were already resting yesterday,
           - or we sold yesterday, so today is the cooldown / resting day.

           rest[i] = max(rest[i - 1], sold[i - 1])

    Base case:
        On day 0:
        - hold[0] = -prices[0]
          If we buy on day 0, our profit becomes negative.

        - sold[0] = impossible
          We cannot sell on day 0 without having bought before.
          In the O(1) solution, we use a very small sentinel value for this state.

        - rest[0] = 0
          If we do nothing on day 0, profit is 0.

    Space optimization:
        Each state only depends on the previous day, so we do not need full arrays.
        We can store only the previous values:
        - hold_prev
        - sold_prev
        - rest_prev

        This reduces space from O(n) to O(1).

    Final answer:
        At the end of the last day, it is never optimal to still be holding a stock,
        because unrealized profit does not count.

        Therefore, the answer is:
            max(rest_prev, sold_prev)

    Complexity:
        Time:  O(n)
        Space: O(1)
    """

    def maxProfit(self, prices: list[int]) -> int:
        n = len(prices)

        hold_prev = -prices[0]
        sold_prev = float("-inf")
        rest_prev = 0

        for i in range(1, n):
            hold = max(hold_prev, rest_prev - prices[i])
            sold = hold_prev + prices[i]
            rest = max(rest_prev, sold_prev)

            hold_prev = hold
            sold_prev = sold
            rest_prev = rest

        return max(rest_prev, sold_prev)
