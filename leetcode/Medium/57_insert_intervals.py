from typing import List


class Solution:
    """Insert a new interval into a sorted list of non-overlapping intervals and merge if needed.

    Problem Statement:
        Given a sorted list of non-overlapping intervals and a newInterval, insert it and merge
        any overlapping intervals, returning the updated sorted list.

    Approach:
        1. Add all intervals that end before newInterval starts.
        2. Merge all intervals that overlap with newInterval by expanding its bounds.
        3. Add the merged interval, then add all remaining intervals.

    Complexity:
        Time: O(n) — single pass through the intervals.
        Space: O(n) for the result list.
    """

    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        results = []
        n = len(intervals)
        i = 0

        while i < n and intervals[i][1] < newInterval[0]:
            results.append(intervals[i])
            i += 1

        while i < n and intervals[i][0] <= newInterval[1]:
            newInterval = [
                min(newInterval[0], intervals[i][0]),
                max(newInterval[1], intervals[i][1]),
            ]
            i += 1
        results.append(newInterval)

        while i < n:
            results.append(intervals[i])
            i += 1

        return results
