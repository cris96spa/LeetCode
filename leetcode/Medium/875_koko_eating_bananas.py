from math import ceil
from typing import List


class Solution:
    """Find the minimum eating speed so Koko can eat all bananas within h hours.

    Problem Statement:
        Given n piles of bananas and h hours, find the minimum integer k (bananas/hour) such
        that Koko can eat all piles within h hours. Each hour Koko eats k bananas from one pile
        (or finishes the pile if it has fewer than k bananas).

    Approach:
        Binary search on k in range [1, max(piles)]. For each candidate k, compute the
        total hours needed. Converge on the minimum valid k.

    Complexity:
        Time: O(n log m) where m = max(piles) and n = number of piles.
        Space: O(1).
    """

    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        left, right = 1, max(piles)

        while left <= right:
            mid = (left + right) // 2
            if self._canFinish(mid, piles, h):
                right = mid - 1
            else:
                left = mid + 1

        return left

    def _canFinish(self, k: int, piles: List[int], h: int) -> bool:
        hours_needed = 0
        for bananas in piles:
            hours_needed += ceil(bananas / k)
            if hours_needed > h:
                return False
        return True
