class Solution:
    def coinChange(self, coins: list[int], amount: int) -> int:
        """
        Problem:
        Given a list of coin denominations and a target amount, return the
        minimum number of coins needed to make up that amount.
        If it is not possible to form the amount, return -1.

        Constraints:
        - Infinite supply of each coin
        - coins[i] >= 1
        - 0 <= amount <= 10^4

        ============================================================
        APPROACH 1 — Dynamic Programming (Bottom-Up)

        Idea:
        Instead of starting from the target and subtracting coins (BFS view),
        we build solutions incrementally from 0 up to the target amount.

        ------------------------------------------------------------
        State Definition:

        state[x] = minimum number of coins needed to form amount x

        ------------------------------------------------------------
        Recurrence:

        For each amount x:
            state[x] = min(state[x - coin] + 1)
            for all coins such that x - coin >= 0

        Interpretation:
        - If we pick coin `c` as the last coin,
          then we must already know the optimal solution for (x - c)
        - Add one coin to that solution

        ------------------------------------------------------------
        Initialization:

        state[0] = 0
        All other values initialized to +∞ (unreachable)

        ------------------------------------------------------------
        Iteration Order:

        We compute from smaller → larger amounts:
            for x in range(1, amount + 1)

        This guarantees subproblems are already solved.

        ------------------------------------------------------------
        Result:

        - If state[amount] == ∞ → return -1
        - Otherwise → return state[amount]

        ------------------------------------------------------------
        Complexity:

        Time:  O(amount * len(coins))
        Space: O(amount)

        ------------------------------------------------------------
        Pattern:

        This is a classic:
        → Unbounded Knapsack (minimization version)

        - "Unbounded" because coins can be reused infinitely
        - "Minimization" because we minimize number of items (coins)

        ============================================================
        APPROACH 2 — BFS (Shortest Path Interpretation)

        Idea:
        Model the problem as a graph:

        - Node = remaining amount
        - Edge = subtract a coin
        - Goal = reach 0
        - Each edge has cost 1

        BFS guarantees the shortest number of steps (coins).

        ------------------------------------------------------------
        BFS Skeleton:

            queue = deque([amount])
            visited = set()
            steps = 0

            while queue:
                steps += 1
                for _ in range(len(queue)):
                    curr = queue.popleft()

                    for coin in coins:
                        nxt = curr - coin

                        if nxt == 0:
                            return steps
                        if nxt > 0 and nxt not in visited:
                            queue.append(nxt)
                            visited.add(nxt)

            return -1

        ------------------------------------------------------------
        Complexity:

        Time:  O(amount * len(coins))
        Space: O(amount)

        ------------------------------------------------------------
        Key Difference vs DP:

        - BFS explores the state space level-by-level
          → "How many steps to reach 0?"

        - DP directly computes:
          → "What is the best answer for each amount x?"

        Both operate on the same state space (amounts 0..amount),
        but DP avoids queue overhead and is more direct.

        ============================================================
        Key Insight:

        Both BFS and DP rely on the same fundamental structure:

            smaller subproblems → larger solution

        BFS:
            subtract from amount → reach 0

        DP:
            build from 0 → reach amount

        They are dual views of the same state graph.

        ============================================================
        """

        state = [amount + 1] * (amount + 1)
        state[0] = 0

        if amount == 0:
            return 0

        for x in range(1, amount + 1):
            for coin in coins:
                if x - coin >= 0:
                    state[x] = min(state[x], state[x - coin] + 1)

        return state[amount] if state[amount] != amount + 1 else -1
