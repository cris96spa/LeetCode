from typing import List


class Solution:
    """Determine the number of car fleets that arrive at the target.

    Problem Statement:
        Given target distance and arrays position and speed for n cars, return the number of
        car fleets. A faster car behind a slower car merges into a fleet at the slower car's
        speed. A car catching up exactly at the target still forms one fleet.

    Approach:
        Sort cars by position descending. Compute time-to-target for each car. Use a stack:
        if the current car's time exceeds the top of the stack, it forms a new fleet.

    Complexity:
        Time: O(n log n) for sorting.
        Space: O(n) for the stack.
    """

    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
        cars = sorted(zip(position, speed), reverse=True)
        stack: List[float] = []

        for pos, spe in cars:
            time = (target - pos) / spe
            if not stack or time > stack[-1]:
                stack.append(time)

        return len(stack)
