class Solution:
    """Reverse all 32 bits of an unsigned integer.

    Problem Statement:
        Given a 32-bit unsigned integer n, return the integer whose binary
        representation is the reverse of n's binary representation. Two
        implementations are provided: a simple bit-by-bit approach and an
        optimized lookup-table approach.

    Approach:
        Simple (reverseBits): Iterate 32 times. Each iteration shifts the result
        left by 1 and appends the LSB of n, then right-shifts n by 1.

        Optimized (reverseBitsOptimized): Precompute a lookup table mapping each
        byte (0-255) to its bit-reversed value. Split the 32-bit input into four
        bytes, reverse each via the table, and reassemble in reversed byte order.

    Complexity:
        Time: O(1) for both methods; exactly 32 bits are processed regardless of
            input value.
        Space: O(1) for the simple approach; O(1) for the optimized approach as
            the 256-entry table is a fixed constant.
    """

    def reverseBits(self, n: int) -> int:
        result = 0
        for _ in range(32):
            result = (result << 1) | (n & 1)
            n >>= 1
        return result

    def reverseBitsOptimized(self, n: int) -> int:
        def reverse_byte(byte: int) -> int:
            result = 0
            for _ in range(8):
                result = (result << 1) | (byte & 1)
                byte >>= 1
            return result

        lookup = {i: reverse_byte(i) for i in range(256)}

        return (
            (lookup[n & 0xFF] << 24)
            | (lookup[(n >> 8) & 0xFF] << 16)
            | (lookup[(n >> 16) & 0xFF] << 8)
            | (lookup[(n >> 24) & 0xFF])
        )
