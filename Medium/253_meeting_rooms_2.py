from heapq import heappush, heappop
from typing import List


class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        """
        Given an array of meeting time intervals `intervals` where intervals[i] = [start_i, end_i],
        return the minimum number of conference rooms required.

        Constraints:
        - 1 <= intervals.length <= 10^4
        - 0 <= start_i < end_i <= 10^6

        Approach:
        - Sort the intervals based on the start time.
        - Use a min-heap to track the end times of ongoing meetings.
        - Iterate through the sorted intervals:
            - If a meeting starts after the earliest ending meeting in the heap, reuse the room (pop the heap).
            - Otherwise, allocate a new room (push the end time to the heap).
        - The maximum heap size at any point gives the required number of rooms.

        Time Complexity: O(N log N) (due to sorting and heap operations)
        Space Complexity: O(N) (in the worst case when all meetings overlap)

        """
        if not intervals:
            return 0

        # Sort the meetings by start time
        intervals.sort()

        # Min-heap to track end times of meetings
        min_heap = []

        # Start processing meetings
        for start, end in intervals:
            # If the earliest ending meeting is done before this one starts, reuse the room
            if min_heap and min_heap[0] <= start:
                heappop(min_heap)  # Remove the meeting that has ended

            # Allocate a new room (or reallocate an old room)
            heappush(min_heap, end)

        # The heap size tells us the max concurrent meetings (rooms needed)
        return len(min_heap)
