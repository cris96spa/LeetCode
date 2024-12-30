from typing import List


class Solution:
    def insert(
        self, intervals: List[List[int]], newInterval: List[int]
    ) -> List[List[int]]:
        """
        Problem Statement:
        ------------------
        You are given a list of non-overlapping intervals `intervals` where intervals[i] = [starti, endi]
        represent the start and the end of the ith interval and intervals is sorted in ascending order
        by starti. You are also given an interval `newInterval = [start, end]` that represents the start
        and end of another interval.

        Insert `newInterval` into intervals such that the list remains sorted in ascending order
        by starti and the list remains free of overlapping intervals (merge overlapping intervals if necessary).

        Return the updated list of intervals.

        Parameters:
        -----------
        intervals: List[List[int]]
            A list of non-overlapping intervals sorted by their start times.
        newInterval: List[int]
            A new interval to insert into the list of intervals.

        Returns:
        --------
        List[List[int]]
            The updated list of non-overlapping intervals sorted by start times.

        Approach:
        ---------
        1. Traverse the `intervals` list to append all intervals that end before `newInterval` starts.
        2. Merge all overlapping intervals with `newInterval` by updating its start and end times.
        3. Append the merged interval.
        4. Add all remaining intervals that start after `newInterval` ends.

        Complexity:
        -----------
        - Time Complexity: O(n), where `n` is the number of intervals in the input list.
        - Space Complexity: O(n), as we store the results in a new list.

        Examples:
        ---------
        Example 1:
        Input: intervals = [[1,3],[6,9]], newInterval = [2,5]
        Output: [[1,5],[6,9]]

        Example 2:
        Input: intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]
        Output: [[1,2],[3,10],[12,16]]

        Example 3:
        Input: intervals = [], newInterval = [5,7]
        Output: [[5,7]]
        """
        results = []
        n = len(intervals)
        i = 0

        # Add all intervals that end before newInterval[0]
        while i < n and intervals[i][1] < newInterval[0]:
            results.append(intervals[i])
            i += 1

        # Merge overlapping intervals
        while i < n and intervals[i][0] <= newInterval[1]:
            newInterval = [
                min(newInterval[0], intervals[i][0]),
                max(newInterval[1], intervals[i][1]),
            ]
            i += 1
        results.append(newInterval)

        # Add remaining intervals
        while i < n:
            results.append(intervals[i])
            i += 1

        return results
