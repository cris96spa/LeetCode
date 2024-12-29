from typing import List


class Solution:
    def letterCombinations(self, digits: str) -> list[str]:
        """
        Given a string containing digits from 2-9 inclusive, return all possible letter
        combinations that the number could represent. Return the answer in any order.

        Problem Description:
        -------------------
        Each digit from 2-9 maps to a set of letters, mimicking the layout of a telephone keypad.
        For instance:
        - 2 maps to ['a', 'b', 'c']
        - 3 maps to ['d', 'e', 'f']
        - ...
        - 9 maps to ['w', 'x', 'y', 'z']

        The task is to generate all possible combinations of letters by choosing one letter
        from the set corresponding to each digit in the input string. If the input string is
        empty, return an empty list. The order of the combinations in the output does not matter.

        Approach:
        ---------
        1. Use a dictionary (`char_map`) to define the mapping of digits to letters.
        2. Employ backtracking to explore all possible combinations:
           - At each recursive step, append a letter from the current digit's mapped set.
           - Move to the next digit and repeat until all digits are processed.
           - Add the completed combination to the result list.
        3. Handle edge cases like an empty input string directly.

        Parameters:
        -----------
        digits (str): A string of digits between '2' and '9'.

        Returns:
        --------
        list[str]: All possible letter combinations that the digits could represent.

        Examples:
        ---------
        Input: digits = "23"
        Output: ["ad","ae","af","bd","be","bf","cd","ce","cf"]

        Input: digits = ""
        Output: []

        Input: digits = "2"
        Output: ["a","b","c"]
        """

        char_map = {
            "2": ["a", "b", "c"],
            "3": ["d", "e", "f"],
            "4": ["g", "h", "i"],
            "5": ["j", "k", "l"],
            "6": ["m", "n", "o"],
            "7": ["p", "q", "r", "s"],
            "8": ["t", "u", "v"],
            "9": ["w", "x", "y", "z"],
        }

        if not digits:
            return []

        results = []

        def generate_combinations(index: int, current_combination: list[str]):
            # Base case: when the combination length equals the digits length
            if index == len(digits):
                results.append("".join(current_combination))
                return

            # Iterate over the characters mapped to the current digit
            for char in char_map[digits[index]]:
                current_combination.append(char)
                generate_combinations(index + 1, current_combination)
                current_combination.pop()

        generate_combinations(0, [])
        return results
