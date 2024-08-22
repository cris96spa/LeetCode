"""
Roman numerals are represented by seven different symbols: I, V, X, L, C, D and M.

Symbol       Value
I             1
V             5
X             10
L             50
C             100
D             500
M             1000
For example, 2 is written as II in Roman numeral, just two ones added together. 12 is written as XII, which is simply X + II. The number 27 is written as XXVII, which is XX + V + II.

Roman numerals are usually written largest to smallest from left to right. However, the numeral for four is not IIII. Instead, the number four is written as IV. Because the one is before the five we subtract it making four. The same principle applies to the number nine, which is written as IX. There are six instances where subtraction is used:

I can be placed before V (5) and X (10) to make 4 and 9. 
X can be placed before L (50) and C (100) to make 40 and 90. 
C can be placed before D (500) and M (1000) to make 400 and 900.
Given a roman numeral, convert it to an integer.

Example 1:

Input: s = "III"
Output: 3
Explanation: III = 3.
Example 2:

Input: s = "LVIII"
Output: 58
Explanation: L = 50, V= 5, III = 3.
Example 3:

Input: s = "MCMXCIV"
Output: 1994
Explanation: M = 1000, CM = 900, XC = 90 and IV = 4.
 
Constraints:
1 <= s.length <= 15
s contains only the characters ('I', 'V', 'X', 'L', 'C', 'D', 'M').
It is guaranteed that s is a valid roman numeral in the range [1, 3999].
"""

class Solution:
    def romanToInt(self, s: str) -> int:
        mapping = {
            'I' : 1,
            'V' : 5,
            'X' : 10,
            'L' : 50,
            'C' : 100,
            'D' : 500,
            'M' : 1000
        }

        summ = 0
        for i in range(len(s)):
            num = mapping[s[i]]
            
            if i+1 < len(s) and num < mapping[s[i+1]]:
                summ -= num
            else:
                summ += num
        return summ
    
"""
This function converts a Roman numeral string into its equivalent integer value. The Roman numeral system uses seven symbols with specific values, and certain combinations of these symbols represent numbers through both addition and subtraction rules.

The approach taken in this function is as follows:

1. **Mapping Roman Numerals to Integers**:
   - A dictionary `mapping` is created to store the integer values corresponding to each Roman numeral character ('I', 'V', 'X', 'L', 'C', 'D', 'M').

2. **Iterating Through the Roman Numeral String**:
   - We initialize a variable `summ` to store the cumulative integer value as we iterate through the string.
   - The loop iterates over each character in the string `s`:
     - For each character `s[i]`, we look up its value in the `mapping` dictionary.
     - If the current numeral is followed by a numeral with a larger value (e.g., 'I' before 'V' in "IV"), we subtract the current value from `summ`. This is because in Roman numerals, a smaller numeral before a larger numeral indicates subtraction.
     - If the current numeral is followed by a numeral with a smaller or equal value, we add the current value to `summ`.

3. **Returning the Final Sum**:
   - After processing all characters in the string, the final value of `summ` represents the integer equivalent of the Roman numeral, which is then returned.

This algorithm efficiently converts a Roman numeral to an integer with a time complexity of O(n), where n is the length of the string, by making a single pass through the string.
"""
