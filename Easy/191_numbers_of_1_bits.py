class Solution:
    def hammingWeight(self, n: int) -> int:
        """
        Problem Statement:
        -------------------
        Given a positive integer `n`, return the number of set bits (1s) in its binary representation.
        This is also known as the Hamming weight of the number.

        Approach 1:
        -----------
        1. Initialize a counter (`set_bits_count`) to track the number of set bits.
        2. Iterate until `n` becomes 0:
           - Check if the least significant bit (LSB) of `n` is 1 using `n & 1`.
           - If it is, increment the counter.
           - Right-shift `n` by 1 to process the next bit.
        3. Return the counter.

        Complexity:
        -----------
        - Time Complexity: O(log n), where log n is the number of bits in the binary representation of `n`.
        - Space Complexity: O(1), as no extra space is used.

        Approach 2:
        -----------
        1. Use the bitwise trick `n & (n - 1)` which removes the lowest set bit of `n` in each iteration.
        2. Initialize a counter (`set_bits_count`) to track the number of set bits.
        3. While `n` is not 0:
           - Remove the lowest set bit using `n &= (n - 1)`.
           - Increment the counter.
        4. Return the counter.

        Complexity:
        -----------
        - Time Complexity: O(number of set bits), which can be faster for sparse numbers.
        - Space Complexity: O(1), as no extra space is used.

        Parameters:
        -----------
        n (int): A positive integer whose set bits are to be counted.

        Returns:
        --------
        int: The number of 1s in the binary representation of `n`.

        Examples:
        ---------
        Input: n = 11 (binary: 1011)
        Output: 3

        Input: n = 128 (binary: 10000000)
        Output: 1

        Input: n = 4294967293 (binary: 11111111111111111111111111111101)
        Output: 31
        """
        set_bits_count = 0

        # Approach 1: Using n & 1 and n >> 1
        while n:
            if n & 1:  # Check if the least significant bit is set
                set_bits_count += 1
            n = n >> 1  # Right-shift n to process the next bit

        return set_bits_count

    def hammingWeight_optimized(self, n: int) -> int:
        """
        Optimized Approach using n & (n - 1):
        ------------------------------------
        Use the bitwise trick `n & (n - 1)` to count set bits efficiently.

        Steps:
        ------
        1. Initialize a counter (`set_bits_count`) to track the number of set bits.
        2. While `n` is not 0:
           - Remove the lowest set bit using `n &= (n - 1)`.
           - Increment the counter.
        3. Return the counter.

        Complexity:
        -----------
        - Time Complexity: O(number of set bits), which is efficient for sparse numbers.
        - Space Complexity: O(1).
        """
        set_bits_count = 0

        while n:
            n &= n - 1  # Remove the lowest set bit
            set_bits_count += 1

        return set_bits_count
