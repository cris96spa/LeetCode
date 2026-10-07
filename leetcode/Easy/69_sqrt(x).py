from typing import Callable


class Solution:
    """√ Sqrt(x).

    Problem:
    --------
    Given a non-negative integer `x`, return its square root rounded down to the nearest
    integer. Built-in exponent functions and operators (e.g. `pow(x, 0.5)`, `x ** 0.5`)
    are not allowed.

    Key Insight:
    ------------
    We want the largest `k` with `k * k <= x`. Equivalently, find the first `k` with
    `k * k > x` and step back by one. The predicate `P(k) = k * k > x` is monotone:

        k:    0  1  2  ...  x + 1
        P(k): F  F  F  T  T  T

    Approach:
    ---------
    - Run the `first_true` template over [0, x + 2). The first True is at most `x + 1`,
      since `(x + 1)^2 > x` for every `x >= 0`.
    - Subtract 1 to go from "first k with k^2 > x" to "last k with k^2 <= x".
    - `x = 0`: the first True is `k = 1`, so the answer is 0.

    Complexity:
    -----------
    - Time: O(log x)
    - Space: O(1)
    """

    def mySqrt(self, x: int) -> int:
        def first_true(low: int, high: int, predicate: Callable[[int], bool]) -> int:
            while low < high:
                mid = (low + high) // 2
                if predicate(mid):
                    high = mid
                else:
                    low = mid + 1
            return low

        return first_true(0, x + 2, lambda k: k * k > x) - 1
