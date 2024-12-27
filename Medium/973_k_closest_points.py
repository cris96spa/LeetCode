from heapq import heappop, heappush
from typing import List
from math import sqrt


class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        """
        Given an array of points where points[i] = [xi, yi] represents a point on the X-Y plane and an integer k,
        return the k closest points to the origin (0, 0).

        The distance between two points on the X-Y plane is the Euclidean distance:

            sqrt((x1 - x2)^2 + (y1 - y2)^2).

        You may return the answer in any order. The answer is guaranteed to be unique (except for the order that it is in).

        Approach:
        - Use a min-heap to store the points by their Euclidean distance from the origin.
        - Push all points onto the heap with their distance.
        - Extract the k smallest elements from the heap, as these are the closest points.

        Args:
            points: List of points represented as [xi, yi].
            k: Number of closest points to return.

        Returns:
            List of k points closest to the origin.
        """
        if len(points) == k:
            return points

        heap = []
        for x, y in points:
            distance = x * x + y * y
            heappush(heap, (distance, x, y))

        results = []
        for _ in range(k):
            _, x, y = heappop(heap)
            results.append([x, y])

        return results
