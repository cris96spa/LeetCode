from typing import List


class Solution:
    """Group anagrams together from an array of strings.

    rearranging the letters of another, using all the original letters exactly once.
    The function returns a list of grouped anagrams, and the order of the groups or elements
    within the groups does not matter.

    Example 1:
    Input: strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
    Output: [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]

    Example 2:
    Input: strs = [""]
    Output: [[""]]

    Example 3:
    Input: strs = ["a"]
    Output: [["a"]]

    Constraints:
    - 1 <= strs.length <= 10^4
    - 0 <= strs[i].length <= 100
    - strs[i] consists of lowercase English letters.

    Approach:
    1. Use a dictionary (`key_map`) to group strings based on a "key" that represents their sorted
    characters.
       - Sorting the characters of a string provides a unique identifier for all its anagrams.
    2. Iterate over the list of strings:
       - Sort each string to generate its key.
       - If the key is not in the dictionary, create a new entry with the string as its first value.
       - If the key already exists, append the string to the corresponding list.
    3. Return all values from the dictionary as the grouped anagrams.

    Complexity:
    - Time Complexity: O(k * n log n), where `k` is the number of strings and `n` is the average
    length of a string.
      - Sorting each string takes O(n log n), and this is done for `k` strings.
    - Space Complexity: O(k * n), for the dictionary and grouped anagrams.

    This implementation is efficient for the given constraints and handles edge cases like empty
    strings or single characters.
    """

    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        # Define a key mapping
        key_map = {}

        # Iterate on each string
        for s in strs:
            key = "".join(sorted(s))
            if key not in key_map:
                key_map[key] = [s]
            else:
                key_map[key].append(s)

        return [key_map[key] for key in key_map.keys()]
