class Solution:
    """
    Description:
    You are given an integer `num`. You can swap two digits at most once to get the maximum valued number.
    The task is to return the maximum valued number you can get by performing at most one swap.

    Example 1:
    Input: num = 2736
    Output: 7236
    Explanation: Swap the number 2 and the number 7.

    Example 2:
    Input: num = 9973
    Output: 9973
    Explanation: No swap needed since the number is already the largest possible.

    Solution:
    1. Convert the number to a list of its digits for easy manipulation.
    2. Create a dictionary that stores the last occurrence of each digit in the number. This helps us quickly find the rightmost larger digit to swap with.
    3. Traverse the digits from left to right. For each digit, check if there exists a larger digit (from 9 down to the current digit) that appears later in the number.
    4. If such a digit exists, swap the current digit with the rightmost occurrence of the larger digit.
    5. Once the swap is made, return the number as an integer formed by the modified list.
    6. If no swap is made after traversing the entire list, return the original number as it is already the largest possible.

    Time Complexity: O(n), where n is the number of digits in the number.
    Space Complexity: O(n), for storing the list of digits and the dictionary of last positions.
    """

    def maximumSwap(self, num: int) -> int:
        # Convert the num to list
        num_list = list(str(num))

        # Get the last position of each digit
        last_pos = {int(digit): i for i, digit in enumerate(num_list)}

        # Scan the list left to right
        for i, d in enumerate(num_list):
            # Check for each digit, from 9 to num
            for digit in range(9, int(d), -1):
                if last_pos.get(digit, -1) > i:
                    # Swap the digits
                    num_list[i], num_list[last_pos[digit]] = (
                        num_list[last_pos[digit]],
                        num_list[i],
                    )
                    return int("".join(num_list))

        return num
