from typing import List


class Solution:
    """Merge all overlapping intervals and return a list of non-overlapping intervals.

    Problem Statement:
        Given an array of intervals where each interval is [starti, endi], merge all overlapping
        intervals and return an array of the non-overlapping intervals that cover all the intervals
        in the input.

    Approach:
        1. Sort the intervals by their start time so overlapping intervals are adjacent.
        2. Iterate through sorted intervals; if the current interval overlaps with the last
           merged interval, extend it. Otherwise, append it as a new interval.

    Complexity:
        Time: O(n log n) due to sorting.
        Space: O(n) for the result list.
    """

    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        # Step 1: Sort the intervals based on the starting value of each interval
        intervals = sorted(intervals, key=lambda x: x[0])

        # Step 2: Initialize the results list with the first interval
        results = [intervals[0]]

        # Step 3: Traverse through the sorted intervals to merge overlapping ones
        for i in range(1, len(intervals)):
            # If the current interval overlaps with the last one in results, merge them
            if intervals[i][0] <= results[-1][1]:
                results[-1][1] = max(results[-1][1], intervals[i][1])  # Update the end time
            else:
                # If they don't overlap, add the current interval to the results
                results.append(intervals[i])

        # Return the merged intervals
        return results
