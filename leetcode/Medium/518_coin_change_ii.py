class Solution:
    """🪙 Coin Change II.

    Problem:
    --------
    Given distinct coin values `coins` and an integer `amount`, return the number of
    **combinations** of coins that sum to exactly `amount`, or 0 if none does. Each coin
    can be used any number of times. Order doesn't matter: `[2, 2, 1]` and `[1, 2, 2]`
    are the same combination.

    Example (`coins = [1, 2, 5]`, `amount = 5`, answer 4):
    `[5]`, `[2, 2, 1]`, `[2, 1, 1, 1]`, `[1, 1, 1, 1, 1]`.

    Key Insight:
    ------------
    This is the counting version of **unbounded knapsack**: the same table as Coin Change
    (LC 322), adding up ways instead of taking the minimum.

    State: `W[i][j]` = number of combinations of the first `i` coin types summing to
    exactly `j`.

    Split on coin type `c = coins[i - 1]`. Every combination either:
    - **uses no `c`**: it's a combination of the first `i - 1` types, so `W[i-1][j]`;
    - **uses at least one `c`** (only if `c <= j`): remove one copy, and what's left is a
      combination summing to `j - c` that may still use `c`, so `W[i][j - c]`.

        W[i][j] = W[i-1][j] + W[i][j - c]

    The take branch reads row `i`, not `i - 1`: taking a coin doesn't remove it from the
    menu. That's the only difference from 0/1 knapsack.

    Base case: `W[0][0] = 1` (the empty combination makes 0) and `W[0][j] = 0` for
    `j > 0`. The answer is `W[n][amount]`.

    Example (`coins = [1, 2, 5]`, `amount = 5`):

          j       0  1  2  3  4  5
          none    1  0  0  0  0  0
          + 1     1  1  1  1  1  1
          + 2     1  1  2  2  3  3
          + 5     1  1  2  2  3  4

    `W[2][4] = W[1][4] + W[2][2] = 1 + 2 = 3`: `[1, 1, 1, 1]` without a 2, plus one 2
    added to each of the two ways to make 2 (`[1, 1]`, `[2]`).

    **Why each combination is counted once.** Coin types are decided in a fixed order:
    row `i` only decides how many copies of `coins[i - 1]` to use. So `[2, 2, 1]` is built
    one way only (the 1 in row 1, both 2s in row 2), never as `[1, 2, 2]` and `[2, 1, 2]`
    separately. Counting ordered sequences instead (Combination Sum IV, LC 377) needs a
    different state, `ways[j]` with no coin index, split on the **last** coin.

    Approach:
    ---------
    Row `i` reads only rows `i - 1` and `i`, so one array `state` of size `amount + 1`
    suffices, updated in place with coin types in the outer loop. Since the take branch
    reads the **current** row at `j - c`, `j` goes **upward**: `state[j - c]` has already
    been updated for coin `c`, which is exactly what reuse means. (0/1 subset sum, LC 416,
    goes downward for the opposite reason.)

    Complexity:
    -----------
    With `n = len(coins)`:
    - Time: O(n * amount)
    - Space: O(amount), down from O(n * amount) for the full table
    """

    def change(self, amount: int, coins: list[int]) -> int:
        # state[j] represents how many way we have to reach exactly j using elements of coins
        state: list[int] = [1] + [0] * amount

        for coin in coins:
            for j in range(amount + 1):
                if j >= coin:
                    state[j] += state[j - coin]

        return state[-1]
