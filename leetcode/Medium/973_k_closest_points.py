from heapq import heappop, heappush
from typing import List


class Solution:
    """Return the k closest points to the origin (0, 0) using Euclidean distance.

    Problem Statement:
        Given an array of points[i] = [xi, yi] and integer k, return the k closest points
        to the origin. Distance is Euclidean: sqrt(x^2 + y^2). Answer may be in any order.

    Approach:
        Push all points onto a min-heap keyed by squared distance (no sqrt needed). Pop
        k elements to get the k closest points.

    Complexity:
        Time: O(n log n) for heap operations.
        Space: O(n) for the heap.
    """

    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        if len(points) == k:
            return points

        heap: list[tuple[int, int, int]] = []
        for x, y in points:
            heappush(heap, (x * x + y * y, x, y))

        results = []
        for _ in range(k):
            _, x, y = heappop(heap)
            results.append([x, y])

        return results
