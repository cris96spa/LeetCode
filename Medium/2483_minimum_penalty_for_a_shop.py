class Solution:
    """
    LeetCode 2483: Minimum Penalty for a Shop

    PROBLEM DESCRIPTION:
    -------------------
    You are given the customer visit log of a shop represented by a 0-indexed string
    customers consisting only of characters 'N' and 'Y':

    - if the ith character is 'Y', it means that customers come at the ith hour
    - whereas 'N' indicates that no customers come at the ith hour.

    If the shop closes at the jth hour (0 <= j <= n), the penalty is calculated as follows:
    - For every hour when the shop is open and no customers come, the penalty increases by 1.
    - For every hour when the shop is closed and customers come, the penalty increases by 1.

    Return the earliest hour at which the shop must be closed to incur a minimum penalty.

    Note that if a shop closes at the jth hour, it means the shop is closed at the hour j.

    Example 1:
        Input: customers = "YYNY"
        Output: 2
        Explanation:
        - Closing the shop at the 0th hour incurs in 1+1+0+1 = 3 penalty.
        - Closing the shop at the 1st hour incurs in 0+1+0+1 = 2 penalty.
        - Closing the shop at the 2nd hour incurs in 0+0+0+1 = 1 penalty.
        - Closing the shop at the 3rd hour incurs in 0+0+1+1 = 2 penalty.
        - Closing the shop at the 4th hour incurs in 0+0+1+0 = 1 penalty.
        Closing the shop at 2nd or 4th hour gives a minimum penalty. Since 2 is earlier,
        the optimal closing time is 2.

    Example 2:
        Input: customers = "NNNNN"
        Output: 0
        Explanation: It is best to close the shop at the 0th hour as no customers arrive.

    Example 3:
        Input: customers = "YYYY"
        Output: 4
        Explanation: It is best to close the shop at the 4th hour as customers arrive at
        each hour.

    Constraints:
        - 1 <= customers.length <= 10^5
        - customers consists only of characters 'Y' and 'N'.

    SOLUTION APPROACH:
    ------------------
    The key insight is that we can calculate the penalty for each possible closing time
    incrementally, rather than recalculating from scratch each time.

    1. Initial Setup:
       - Start by assuming we close at hour 0 (immediately)
       - The penalty for this is the count of all 'Y's (customers we miss)

    2. Incremental Updates:
       - As we iterate through each hour, we update the penalty for closing at the next hour
       - If current hour has 'Y': closing one hour later REDUCES penalty by 1
         (we serve this customer instead of missing them)
       - If current hour has 'N': closing one hour later INCREASES penalty by 1
         (we're open during an hour with no customers)

    3. Track Minimum:
       - Keep track of the minimum penalty seen and the corresponding closing time
       - Return the earliest hour that achieves minimum penalty

    Time Complexity: O(n) where n is the length of customers string
    Space Complexity: O(1) as we only use constant extra space

    Example walkthrough with "YYNY":
    - Close at 0: penalty = 4 Y's = 4 (but wait, we need to count properly)
      Actually: penalty = count of Y's after position 0 = 3
    - After hour 0 (Y): penalty = 3 - 1 = 2 (close at 1)
    - After hour 1 (Y): penalty = 2 - 1 = 1 (close at 2) ← minimum!
    - After hour 2 (N): penalty = 1 + 1 = 2 (close at 3)
    - After hour 3 (Y): penalty = 2 - 1 = 1 (close at 4)

    Result: 2 (earliest hour with minimum penalty of 1)
    """

    def bestClosingTime(self, customers: str) -> int:
        # Start by counting the penalty of closing at 0
        penalty = customers.count("Y")
        best_penalty = penalty
        best_j = 0

        for idx, customer in enumerate(customers):
            # After each customer, the penalty of closing at next idx
            # is reduced, while it is increased the penalty if no one arrives
            if customer == "Y":
                penalty -= 1
            else:  # 'N'
                penalty += 1

            j = idx + 1  # closing after hour i
            if penalty < best_penalty:
                best_penalty = penalty
                best_j = j

        return best_j
