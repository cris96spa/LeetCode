from typing import List


class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        # Sort by end values
        intervals.sort(key=lambda x: x[1])

        count = 0
        prev_end = float("-inf")

        # Scan each interval
        for interval in intervals:
            # An overlap is found if start_i < end_(i-1)
            if interval[0] < prev_end:
                count += 1
            # Update previous end
            else:
                prev_end = interval[1]

        return count
