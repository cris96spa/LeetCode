class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        """
        Problem Description:
        --------------------
        Given an array of intervals where each interval is represented as [starti, endi],
        the goal is to merge all overlapping intervals and return a list of non-overlapping intervals
        that cover all the intervals in the input.

        Example 1:
        ----------
        Input: intervals = [[1,3],[2,6],[8,10],[15,18]]
        Output: [[1,6],[8,10],[15,18]]
        Explanation: Since intervals [1,3] and [2,6] overlap, merge them into [1,6].

        Example 2:
        ----------
        Input: intervals = [[1,4],[4,5]]
        Output: [[1,5]]
        Explanation: Intervals [1,4] and [4,5] are considered overlapping.

        Constraints:
        ------------
        1 <= intervals.length <= 10^4
        intervals[i].length == 2
        0 <= starti <= endi <= 10^4

        Approach:
        ---------
        1. **Sort the intervals by their start time**:
           Sorting allows us to arrange the intervals such that overlapping intervals are adjacent
           to each other. This makes the merging process easier.
           
        2. **Iterate through the sorted intervals**:
           Compare each interval with the last added interval in the result list. If the current interval
           overlaps with the last one, merge them by updating the end time. If it does not overlap,
           simply add the current interval to the result list.

        3. **Efficient processing**:
           By sorting the intervals first and then performing a single scan through the list, we achieve an
           optimal time complexity of O(n log n), where n is the number of intervals (the sorting step dominates).
        """

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