# Problem: Multiply two non-negative integers represented as strings and return the result as a string.
# Note: We must not use any built-in BigInteger library or convert the inputs directly to integers.

class Solution:
    def multiply(self, num1: str, num2: str) -> str:
        # Initialize integer representations of the two numbers
        x = 0
        
        # Loop through each digit of num1, starting from the least significant digit
        # Simulate integer conversion by multiplying the digit by its positional value (10^i)
        for i, num in enumerate(reversed(num1)):
            x += int(num) * 10**i

        # Initialize integer representation for num2 in the same way
        y = 0
        # Loop through each digit of num2, starting from the least significant digit
        for i, num in enumerate(reversed(num2)):
            y += int(num) * 10**i

        # Multiply the two integer values obtained from num1 and num2
        result = x * y

        # Convert the result back into a string and return it
        return str(result)


# Example usage:

if __name__ == "__main__":
    # Create an instance of the Solution class
    solution = Solution()

    # Test cases
    num1 = "123"
    num2 = "456"
    
    # Output the product of num1 and num2 as a string
    print(f"The product of {num1} and {num2} is: {solution.multiply(num1, num2)}")
    
    # Another test case
    num1 = "2"
    num2 = "3"
    print(f"The product of {num1} and {num2} is: {solution.multiply(num1, num2)}")