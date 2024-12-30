from typing import List


class Solution:
    def canAttendMeetings(self, intervals: List[List[int]]) -> bool:
        """
        Problem Statement:
        ------------------
        Given an array of meeting time intervals where intervals[i] = [starti, endi],
        determine if a person could attend all meetings.

        A person can attend all meetings if no two intervals overlap.

        Parameters:
        -----------
        intervals: List[List[int]]
            A list of intervals where each interval is represented as [start, end].

        Returns:
        --------
        bool
            True if the person can attend all meetings, otherwise False.

        Approach:
        ---------
        1. If the intervals list is empty, return True since there are no meetings.
        2. Sort the intervals by their start times.
        3. Iterate through the sorted intervals and check if any two consecutive intervals overlap.
           - Two intervals overlap if the end time of the first interval is greater than
             the start time of the next interval.
        4. If any overlap is found, return False. Otherwise, return True.

        Complexity:
        -----------
        - Time Complexity: O(n log n), where n is the number of intervals (due to sorting).
        - Space Complexity: O(1), as no additional space is used beyond variables.

        Examples:
        ---------
        Example 1:
        Input: intervals = [[0, 30], [5, 10], [15, 20]]
        Output: False
        Explanation: Meeting [0, 30] overlaps with both [5, 10] and [15, 20].

        Example 2:
        Input: intervals = [[7, 10], [2, 4]]
        Output: True
        Explanation: No intervals overlap.
        """
        if not intervals:
            return True

        # Sort intervals by start time
        intervals.sort(key=lambda x: x[0])

        # Check for overlaps
        for i in range(len(intervals) - 1):
            if intervals[i][1] > intervals[i + 1][0]:
                return False

        return True
