from typing import List


class Solution:
    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
        """
        Given the target distance, and two lists `position` and `speed`, representing the
        starting positions and speeds of `n` cars, determine the number of car fleets
        that will arrive at the target.

        A car fleet is a group of cars that travel together at the same speed because a
        faster car cannot pass a slower car ahead of it. If a car catches up to another
        car at the target, they are still considered part of the same fleet.

        Approach:
        - Sort the cars in descending order based on their starting position.
        - Compute the time taken for each car to reach the target.
        - Use a stack to track fleets; a new fleet is formed if a car takes longer than
          the last recorded fleet time.

        Time Complexity: O(N log N) (due to sorting, followed by O(N) traversal)
        Space Complexity: O(N) (to store fleet times in the stack)

        Parameters:
        - target (int): The destination mile marker.
        - position (List[int]): The starting positions of the cars.
        - speed (List[int]): The speed of each car.

        Returns:
        - int: The number of car fleets that reach the target.
        """
        # Sort the cars in reverse order according to their position.
        # A fleet can occur if a car closer to the target requires more time
        # than a car farther.
        cars = sorted(zip(position, speed), reverse=True)

        # To track fleets we can use a stack
        stack = []

        # For each car we can compute the time to target
        for pos, spe in cars:
            time = (target - pos) / spe

            # If the stack is empty or
            # the time required by a farther car
            # is greater than the one required
            # by a closer one, the two cars cannot
            # fleet up, therefore they form two different batches
            if not stack or time > stack[-1]:
                stack.append(time)

        return len(stack)
