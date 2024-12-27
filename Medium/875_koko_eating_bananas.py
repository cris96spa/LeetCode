from typing import List
from math import ceil


class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        """
        Koko loves to eat bananas. There are n piles of bananas, where the ith pile has piles[i] bananas.
        The guards will return in h hours. Koko can decide her bananas-per-hour eating speed `k`.

        Each hour, Koko eats `k` bananas from a single pile. If the pile has fewer than `k` bananas, she
        eats all bananas in that pile and stops for that hour.

        Return the minimum integer `k` such that she can eat all the bananas within `h` hours.

        Approach:
        - Use binary search to find the optimal eating speed `k`.
        - Start with `k` in the range [1, max(piles)].
        - For a given `k`, calculate the total hours required to eat all bananas.
        - If the required hours exceed `h`, increase `k`.
        - Otherwise, decrease `k` to find a smaller feasible value.

        Args:
            piles: List of integers representing the number of bananas in each pile.
            h: Number of hours available to eat all the bananas.

        Returns:
            Minimum integer `k` such that all bananas are eaten within `h` hours.
        """
        left, right = 1, max(piles)

        while left <= right:
            mid = (left + right) // 2
            if self._canFinish(mid, piles, h):
                right = mid - 1
            else:
                left = mid + 1

        return left

    def _canFinish(self, k: int, piles: List[int], h: int) -> bool:
        """
        Check if Koko can finish eating all bananas within `h` hours at speed `k`.

        Args:
            k: Eating speed (bananas per hour).
            piles: List of integers representing the number of bananas in each pile.
            h: Number of hours available.

        Returns:
            True if Koko can finish all bananas within `h` hours, False otherwise.
        """
        hours_needed = 0
        for bananas in piles:
            hours_needed += ceil(bananas / k)
            if hours_needed > h:
                return False
        return True
