from heapq import heappush, heappop
from typing import List
class Solution:
    """
    This solution solves the problem of assigning a chair to a friend at a party based on their arrival time.
    The party has an infinite number of chairs, numbered starting from 0. Friends take the smallest available
    chair when they arrive, and when they leave, their chair becomes available again.

    Given a 2D integer array `times` where each element `times[i] = [arrival_i, leaving_i]` represents the arrival
    and leaving times of the i-th friend, and an integer `targetFriend`, the task is to determine which chair the 
    `targetFriend` will sit on.

    The approach follows these steps:
    
    1. **Sort by Arrival Times**: The input array `times` is first sorted based on the arrival times of each friend. 
       This ensures that friends are processed in the order of their arrival.

    2. **Track Available Chairs**: A min-heap (`min_free`) is used to keep track of available chairs. Initially, all 
       chairs from 0 to n-1 (where n is the number of friends) are available. The heap allows efficient extraction 
       of the smallest available chair at any given time.

    3. **Manage Chair Releases**: A second min-heap (`leavings`) is used to manage when friends leave. Each time a 
       friend leaves, their chair becomes available, and it is pushed back into the `min_free` heap to be reused by 
       another friend.

    4. **Assign Chairs**: For each friend (processed in order of their arrival), we pop the smallest available chair 
       from the `min_free` heap and assign it to them. We also track when the friend will leave and push their leaving 
       time and chair into the `leavings` heap.

    5. **Identify Target Friend's Chair**: As soon as the target friend arrives, the assigned chair is returned, which 
       is the final answer.

    Time Complexity:
    - Sorting the `times` array takes O(n log n), where n is the number of friends.
    - Each chair assignment (pop and push operations on the heap) takes O(log n), and there are n such operations.
    Therefore, the total time complexity is O(n log n).

    Space Complexity:
    - The space complexity is O(n) due to the two heaps used to track available chairs and leaving times.

    Example 1:
    Input: times = [[1,4], [2,3], [4,6]], targetFriend = 1
    Output: 1
    Explanation:
    - Friend 0 arrives at time 1 and sits on chair 0.
    - Friend 1 arrives at time 2 and sits on chair 1.
    - Friend 1 leaves at time 3, and chair 1 becomes available.
    - Friend 0 leaves at time 4, and chair 0 becomes available.
    - Friend 2 arrives at time 4 and takes chair 0.
    Friend 1 sat on chair 1, so the output is 1.

    Example 2:
    Input: times = [[3,10], [1,5], [2,6]], targetFriend = 0
    Output: 2
    Explanation:
    - Friend 1 arrives at time 1 and sits on chair 0.
    - Friend 2 arrives at time 2 and sits on chair 1.
    - Friend 0 arrives at time 3 and sits on chair 2.
    Friend 0 sat on chair 2, so the output is 2.

    Constraints:
    - 2 <= n <= 10^4
    - 1 <= arrival_i < leaving_i <= 10^5
    - 0 <= targetFriend <= n - 1
    - Each arrival time is distinct.
    """
    def smallestChair(self, times: List[List[int]], targetFriend: int) -> int:
        # Get the target friend's arrival time
        target_arrival = times[targetFriend][0]

        # Sort friends by arrival time
        sorted_times = sorted(times, key=lambda x: x[0])
        
        # Min-heap to track available chairs, initially all chairs from 0 to n-1
        min_free = []
        for i in range(len(times)):
            heappush(min_free, i)

        # Min-heap to track when friends leave and free chairs
        leavings = []

        for arrival, leaving in sorted_times:
            # Free up chairs from friends who have already left before this arrival
            while leavings and leavings[0][0] <= arrival:
                leave_time, chair_to_free = heappop(leavings)
                heappush(min_free, chair_to_free)

            # Get current free position
            assigned_chair = heappop(min_free)
            
            # If this is the target friend's arrival, return their chair
            if arrival == target_arrival:
                return assigned_chair
            
            # Add leaving time to leavings
            heappush(leavings, (leaving, assigned_chair))
        
        return -1  # This should never be reached given the constraints
