"""
Problem Description:
There are `n` bulbs that are initially off. You first turn on all the bulbs, then you turn off every second bulb.
On the third round, you toggle every third bulb (turning on if it's off or turning off if it's on). For the ith round, 
you toggle every ith bulb. For the nth round, you only toggle the last bulb.

The task is to return the number of bulbs that remain on after `n` rounds.

The key observation is that a bulb will be toggled in each round where its index is a divisor of the round number. 
For example, bulb 6 will be toggled in rounds 1, 2, 3, and 6. Bulbs that have an odd number of divisors will remain on, 
and this happens only for perfect squares (because they have an odd number of divisors). Therefore, the problem reduces to
finding how many perfect squares are ≤ `n`.

Example Cases:
Example 1:
Input: n = 3
Output: 1
Explanation: At first, the three bulbs are [off, off, off]. After the first round, the three bulbs are [on, on, on]. 
After the second round, the bulbs become [on, off, on]. After the third round, they become [on, off, off]. 
Thus, only one bulb remains on.

Example 2:
Input: n = 0
Output: 0
Explanation: There are no bulbs to toggle.

Example 3:
Input: n = 1
Output: 1
Explanation: There is only one bulb, which is turned on in the first round and remains on.

Constraints:
- 0 <= n <= 10^9
"""

import math

class Solution:
    def bulbSwitch(self, n: int) -> int:
        # The number of bulbs that remain on corresponds to the number of perfect squares <= n
        # This is equivalent to finding the integer part of the square root of n.
        return int(math.sqrt(n))

# Example Test Cases
if __name__ == "__main__":
    solution = Solution()
    
    # Test Case 1
    n1 = 3
    print(f"Test Case 1: {solution.bulbSwitch(n1)}")  # Expected Output: 1
    
    # Test Case 2
    n2 = 0
    print(f"Test Case 2: {solution.bulbSwitch(n2)}")  # Expected Output: 0
    
    # Test Case 3
    n3 = 1
    print(f"Test Case 3: {solution.bulbSwitch(n3)}")  # Expected Output: 1
