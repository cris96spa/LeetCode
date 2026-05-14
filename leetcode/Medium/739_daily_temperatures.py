from typing import List


class Solution:
    """Return an array of days to wait for a warmer temperature at each position.

    Problem Statement:
        Given an array of daily temperatures, return an array where answer[i] is the number
        of days until a warmer temperature. If no future warmer day exists, answer[i] = 0.

    Approach:
        Monotonic decreasing stack storing indices. For each temperature, while the stack top
        has a lower temperature, pop it and record the difference in indices as the wait days.

    Complexity:
        Time: O(n) — each element pushed and popped at most once.
        Space: O(n) for the stack.
    """

    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        n = len(temperatures)
        answer = [0] * n
        stack: List[int] = []

        for i, temp in enumerate(temperatures):
            while stack and temperatures[stack[-1]] < temp:
                prev_index = stack.pop()
                answer[prev_index] = i - prev_index
            stack.append(i)

        return answer
