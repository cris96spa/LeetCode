from collections import defaultdict
from typing import List


class TimeMap:
    """
    Problem Statement:
    ------------------
    Design a time-based key-value data structure that can store multiple values for the same key at different timestamps
    and retrieve the key's value at a specific timestamp.

    Implement the TimeMap class:
        - `TimeMap()` Initializes the object of the data structure.
        - `void set(String key, String value, int timestamp)` Stores the key with the value at the given time timestamp.
        - `String get(String key, int timestamp)` Returns a value such that `set` was called previously, with
          `timestamp_prev <= timestamp`. If there are multiple such values, it returns the value associated with
          the largest `timestamp_prev`. If there are no values, it returns an empty string "".

    Example:
    --------
        Input:
        ["TimeMap", "set", "get", "get", "set", "get", "get"]
        [[], ["foo", "bar", 1], ["foo", 1], ["foo", 3], ["foo", "bar2", 4], ["foo", 4], ["foo", 5]]

        Output:
        [null, null, "bar", "bar", null, "bar2", "bar2"]

        Explanation:
        TimeMap timeMap = new TimeMap();
        timeMap.set("foo", "bar", 1);  // store the key "foo" and value "bar" with timestamp = 1.
        timeMap.get("foo", 1);         // return "bar"
        timeMap.get("foo", 3);         // return "bar", since the closest timestamp <= 3 is 1.
        timeMap.set("foo", "bar2", 4); // store the key "foo" and value "bar2" with timestamp = 4.
        timeMap.get("foo", 4);         // return "bar2"
        timeMap.get("foo", 5);         // return "bar2"

    Constraints:
    ------------
    - 1 <= key.length, value.length <= 100
    - key and value consist of lowercase English letters and digits.
    - 1 <= timestamp <= 10^7
    - All the timestamps of `set` are strictly increasing.
    - At most 2 * 10^5 calls will be made to `set` and `get`.

    Solution:
    ---------
    1. **Data Structure**:
        Use a dictionary `time_map` where each key maps to a list of tuples `(value, timestamp)`.

    2. **Binary Search for Retrieval**:
        - When retrieving a value for a key at a given timestamp, use binary search to efficiently find the largest
          timestamp less than or equal to the given timestamp.

    3. **Efficiency**:
        - Storing values is O(1) per call.
        - Retrieving values using binary search is O(log n) per call.
    """

    def __init__(self):
        self.time_map = defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        """
        Stores the key with the value at the given timestamp.

        Args:
            key (str): The key for the value.
            value (str): The value to be stored.
            timestamp (int): The timestamp of the value.
        """
        self.time_map[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        """
        Retrieves the value for the given key at the largest timestamp less than or equal to the given timestamp.

        Args:
            key (str): The key for the value.
            timestamp (int): The timestamp to search for.

        Returns:
            str: The value associated with the key at the closest timestamp, or "" if no such value exists.
        """
        if key not in self.time_map:
            return ""

        values = self.time_map[key]
        left, right = 0, len(values) - 1
        result = ""

        while left <= right:
            mid = (left + right) // 2
            if values[mid][0] <= timestamp:
                result = values[mid][
                    1
                ]  # Update result and move right to search for closer timestamps
                left = mid + 1
            else:
                right = mid - 1

        return result
