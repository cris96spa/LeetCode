class Solution:
    """Return all possible letter combinations that a digit string could represent.

    Problem Statement:
        Given a string of digits from 2-9, return all possible letter combinations based on
        the telephone keypad mapping. Return an empty list if input is empty.

    Approach:
        Backtracking. At each recursive step, append one letter from the current digit's
        mapped set, recurse to the next digit, then remove the letter (backtrack). Add to
        results when all digits are processed.

    Complexity:
        Time: O(4^n * n) where n is the number of digits (4 for digits with 4 letters like 7, 9).
        Space: O(n) for the recursion stack.
    """

    def letterCombinations(self, digits: str) -> list[str]:
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

        results: list[str] = []

        def generate_combinations(index: int, current_combination: list[str]) -> None:
            if index == len(digits):
                results.append("".join(current_combination))
                return
            for char in char_map[digits[index]]:
                current_combination.append(char)
                generate_combinations(index + 1, current_combination)
                current_combination.pop()

        generate_combinations(0, [])
        return results
