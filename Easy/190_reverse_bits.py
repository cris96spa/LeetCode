class Solution:
    def reverseBits(self, n: int) -> int:
        """
        Problem Statement:
        -------------------
        Reverse the bits of a given 32-bit unsigned integer.

        Note:
        - In some languages, such as Java, there is no unsigned integer type.
          The integer's internal binary representation is the same, whether signed or unsigned.
        - In Java, the compiler represents signed integers using 2's complement notation.

        Examples:
        ---------
        Input: n = 00000010100101000001111010011100
        Output: 964176192 (00111001011110000010100101000000)

        Input: n = 11111111111111111111111111111101
        Output: 3221225471 (10111111111111111111111111111111)

        Constraints:
        ------------
        - Input must be a binary string of length 32.

        Follow-Up:
        ----------
        If this function is called many times, optimization using a lookup table can improve efficiency.
        """

        # Simple Solution
        result = 0
        for _ in range(32):
            result = (result << 1) | (
                n & 1
            )  # Append the least significant bit of n to result
            n >>= 1  # Shift n to the right to process the next bit
        return result

    def reverseBitsOptimized(self, n: int) -> int:
        """
        Optimized Solution:
        -------------------
        Use a lookup table to reverse bits in chunks (e.g., 8 bits) to reduce computation time.

        Steps:
        ------
        1. Precompute the reverse of all 8-bit numbers (256 values) into a lookup table.
        2. Split the 32-bit number into 4 bytes.
        3. Reverse each byte using the lookup table and combine them.

        Complexity:
        -----------
        - Precomputation: O(256 * 8) = O(2048) (constant time).
        - Runtime per call: O(1) (4 table lookups and bit operations).
        """

        # Precompute reversed bits for all 8-bit numbers
        def reverseByte(byte: int) -> int:
            result = 0
            for _ in range(8):
                result = (result << 1) | (byte & 1)
                byte >>= 1
            return result

        lookup = {i: reverseByte(i) for i in range(256)}

        # Reverse each byte of the 32-bit number and combine
        return (
            (lookup[n & 0xFF] << 24)
            | (lookup[(n >> 8) & 0xFF] << 16)
            | (lookup[(n >> 16) & 0xFF] << 8)
            | (lookup[(n >> 24) & 0xFF])
        )
