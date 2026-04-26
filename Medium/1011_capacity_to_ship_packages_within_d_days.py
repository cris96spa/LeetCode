class Solution:
    """
    🚢 Capacity To Ship Packages Within D Days

    Problem:
    --------
    Given an array `weights` where `weights[i]` represents the weight of the i-th package,
    and an integer `days`, return the minimum ship capacity required to ship all packages
    within `days` days.

    Constraints:
    ------------
    - Packages must be shipped in order (no reordering allowed).
    - Each package must be shipped entirely in one day (no splitting).
    - The total weight shipped in a day cannot exceed the ship's capacity.

    Key Insight:
    ------------
    We are asked to minimize the ship capacity while satisfying a constraint (shipping within `days`).
    This is a classic **binary search on the answer space** problem.

    Observations:
    -------------
    - The minimum possible capacity is `max(weights)` (we must at least carry the heaviest package).
    - The maximum possible capacity is `sum(weights)` (ship everything in one day).
    - If a capacity `C` works (i.e., we can ship within `days`), then any capacity > C will also work.
      -> This monotonic property makes binary search applicable.

    Approach:
    ---------
    1. Perform binary search on the capacity range [max(weights), sum(weights)].
    2. For a candidate capacity:
       - Simulate the shipping process greedily:
         - Keep adding packages to the current day until capacity is exceeded.
         - Move to the next day when needed.
    3. If we can finish within `days`, try a smaller capacity.
       Otherwise, increase the capacity.

    Feasibility Check:
    ------------------
    Greedily pack packages:
    - If adding a package exceeds capacity -> move to next day.
    - Count how many days are needed.

    Complexity:
    -----------
    - Time: O(n * log(sum(weights) - max(weights)))
      - Binary search over capacity range
      - Each feasibility check is O(n)
    - Space: O(1)
    """

    def shipWithinDays(self, weights: list[int], days: int) -> int:
        low, high = max(weights), sum(weights)

        def can_ship(capacity: int) -> bool:
            days_needed = 1
            current_load = 0

            for w in weights:
                if current_load + w <= capacity:
                    current_load += w
                else:
                    days_needed += 1
                    current_load = w

            return days_needed <= days

        while low < high:
            mid = (low + high) // 2
            if can_ship(mid):
                high = mid
            else:
                low = mid + 1

        return low