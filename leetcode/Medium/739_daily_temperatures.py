class Solution:
    """Return an array of days to wait for a warmer temperature at each position.

    Problem Statement:
        Given an array of daily temperatures, return an array where answer[i]
        is the number of days after day i until a warmer temperature. If no
        such day exists, answer[i] = 0.

    Example:
        temperatures = [73, 74, 75, 71, 69, 72, 76, 73]
        -> [1, 1, 4, 2, 1, 1, 0, 0]

    Approach:
        Brute force scans forward from each day for a warmer one: O(n^2).

        Instead, scan left to right with a stack of indices of days still
        waiting for a warmer day; their temperatures are non-increasing from
        bottom to top. For each day, pop every colder day on top and set its
        answer to the index difference, then push the current day. Days left
        on the stack never get warmer and keep answer = 0.

    Complexity:
        Time: O(n), each index is pushed and popped at most once.
        Space: O(n) for the stack.
    """

    def dailyTemperatures(self, temperatures: list[int]) -> list[int]:
        answer = [0] * len(temperatures)
        stack: list[int] = []

        for day, temp in enumerate(temperatures):
            while stack and temperatures[stack[-1]] < temp:
                prev_day = stack.pop()
                answer[prev_day] = day - prev_day
            stack.append(day)

        return answer
