class Solution:
    """
    Given two integers dividend and divisor, divide two integers without using multiplication, division, and mod operator.

    The integer division should truncate toward zero, which means losing its fractional part. For example, 8.345 would be truncated to 8,
    and -2.7335 would be truncated to -2.

    Return the quotient after dividing dividend by divisor.

    Note: Assume we are dealing with an environment that could only store integers within the 32-bit signed integer range: [-2^31, 2^31 - 1].
    For this problem, if the quotient is strictly greater than 2^31 - 1, then return 2^31 - 1, and if the quotient is strictly less than -2^31,
    then return -2^31.

    Solution explanation:

    - The first step is to handle the special overflow case where dividend = -2^31 and divisor = -1, since the result would exceed the 32-bit range.
    - Next, we handle the sign of the result. If either the dividend or divisor is negative (but not both), the result will be negative.
      Otherwise, it will be positive.
    - We then convert both dividend and divisor to their absolute values to simplify the division process.
    - The core logic involves repeatedly subtracting the divisor from the dividend. To optimize the division, we use bit shifting (doubling the divisor
      and a corresponding multiple) until the divisor can no longer be subtracted from the remaining dividend.
    - Finally, after calculating the quotient, we apply the sign and clamp the result to the valid 32-bit signed integer range [-2^31, 2^31 - 1].
    """

    def divide(self, dividend: int, divisor: int) -> int:
        if dividend == -(2**31) and divisor == -1:
            return 2**31 - 1
        sign = True

        # Sign check for dividend
        if dividend < 0:
            sign = False
            dividend = -dividend

        # Sign check for divisor
        if divisor < 0:
            sign = not sign
            divisor = -divisor

        quotient = 0
        while dividend >= divisor:
            temp, multiple = divisor, 1

            # Use bit manipulation to optimize
            # Until dividend is >= than twice temp
            # we double temp and multiple
            while dividend >= (temp << 1):
                temp <<= 1
                multiple <<= 1

            quotient += multiple
            dividend -= temp

        if not sign:
            quotient = -quotient

        # Clip the result
        return max(min(quotient, 2**31 - 1), -(2**31))
