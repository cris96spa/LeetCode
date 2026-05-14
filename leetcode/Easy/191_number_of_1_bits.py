class Solution:
    """Count the number of set bits (Hamming weight) in an integer.

    Problem Statement:
        Given a positive integer n, return the number of set bits (1s) in its
        binary representation, also known as the Hamming weight. Two
        implementations are provided.

    Approach:
        hammingWeight: Check the LSB with n & 1, increment the counter if set,
        then right-shift n. Repeat until n becomes 0.

        hammingWeight_optimized: Apply the trick n &= (n - 1) which clears the
        lowest set bit on each iteration. Count iterations until n becomes 0.
        This is faster for integers with few set bits.

    Complexity:
        Time: O(log n) for hammingWeight (iterates over all bits);
            O(k) for hammingWeight_optimized where k is the number of set bits.
        Space: O(1) for both approaches.
    """

    def hammingWeight(self, n: int) -> int:
        set_bits_count = 0
        while n:
            if n & 1:
                set_bits_count += 1
            n = n >> 1
        return set_bits_count

    def hammingWeight_optimized(self, n: int) -> int:
        set_bits_count = 0
        while n:
            n &= n - 1
            set_bits_count += 1
        return set_bits_count
