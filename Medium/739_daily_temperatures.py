from typing import List


class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        """
        Given an array of daily temperatures, return an array where each index represents
        the number of days until a warmer temperature is encountered.

        If there is no future day with a warmer temperature, the answer at that index is 0.

        Approach:
        - Use a **monotonic decreasing stack** to store indices of temperatures.
        - Traverse the list once and update the stack efficiently.
        - If the current temperature is higher than the temperature at the top of the stack,
          pop the stack and compute the number of days waited.

        Time Complexity: O(N) - Each element is pushed and popped at most once.
        Space Complexity: O(N) - In the worst case, all temperatures are stored in the stack.

        Parameters:
        - temperatures (List[int]): A list of integers representing daily temperatures.

        Returns:
        - List[int]: A list where each index contains the number of days to wait for a warmer temperature.
        """
        n = len(temperatures)
        answer = [0] * n  # Initialize result array with 0s
        stack = []  # Stack to store indices

        for i, temp in enumerate(temperatures):
            while stack and temperatures[stack[-1]] < temp:
                prev_index = stack.pop()
                answer[prev_index] = i - prev_index  # Compute wait days

            stack.append(i)  # Push current index onto the stack

        return answer
