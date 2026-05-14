from typing import List


class Solution:
    """Determine whether a person can attend all meetings without conflicts.

    Problem Statement:
        Given an array of meeting time intervals where intervals[i] = [start,
        end], return True if a person can attend all meetings (no two intervals
        overlap), otherwise return False.

    Approach:
        Sort the intervals by start time. Iterate through consecutive pairs and
        check whether any meeting starts before the previous one ends. If an
        overlap is detected, return False immediately; otherwise return True.

    Complexity:
        Time: O(n log n) due to sorting, where n is the number of intervals.
        Space: O(1), no additional data structures are needed.
    """

    def canAttendMeetings(self, intervals: List[List[int]]) -> bool:
        if not intervals:
            return True

        intervals.sort(key=lambda x: x[0])

        for i in range(len(intervals) - 1):
            if intervals[i][1] > intervals[i + 1][0]:
                return False

        return True
