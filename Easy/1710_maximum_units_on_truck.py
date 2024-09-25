"""
Problem Description:

You are tasked with loading boxes onto a truck. You are given a 2D list called `boxTypes`, 
where each element is in the form [numberOfBoxesi, numberOfUnitsPerBoxi]. 

- `numberOfBoxesi`: This is the number of boxes of type i.
- `numberOfUnitsPerBoxi`: This is the number of units in each box of the type i.

You are also given an integer `truckSize`, representing the maximum number of boxes that 
the truck can hold. The goal is to choose boxes such that the total number of boxes loaded 
onto the truck does not exceed `truckSize` and the total number of units loaded is maximized.

You need to return the maximum total number of units that can be loaded onto the truck.

### Example 1:
Input: boxTypes = [[1, 3], [2, 2], [3, 1]], truckSize = 4
Output: 8
Explanation: 
- 1 box of type 1 contains 3 units.
- 2 boxes of type 2 contain 2 units each.
- 3 boxes of type 3 contain 1 unit each.
You can take all boxes of type 1 and 2, and one box of type 3. 
Total number of units = (1 * 3) + (2 * 2) + (1 * 1) = 8.

### Example 2:
Input: boxTypes = [[5, 10], [2, 5], [4, 7], [3, 9]], truckSize = 10
Output: 91
Explanation:
- Take boxes of types in order that maximizes units, ensuring the truck capacity isn't exceeded.

### Constraints:
- 1 <= boxTypes.length <= 1000
- 1 <= numberOfBoxesi, numberOfUnitsPerBoxi <= 1000
- 1 <= truckSize <= 10^6

Solution Approach:

1. **Sorting by Unit Count**: Since the goal is to maximize the total units loaded, the best approach is to load boxes with the most units first. To do this, we can sort the `boxTypes` list by the number of units per box in descending order.
   
2. **Greedy Approach**: Once sorted, iterate through the sorted list and load as many boxes as possible from each type until the truck is full. If there’s leftover space on the truck, load as much as possible from the next box type.

3. **Merge Sort Implementation (Optional)**: The provided code includes a `merge_sort` function, which can also be used to sort `boxTypes`. However, Python's built-in `sort` function (based on Timsort) is more optimized and directly used in this solution.

4. **Complexity Consideration**: Sorting the list of boxes takes O(n log n), where n is the number of box types. Iterating through the list to load the truck takes O(n). Thus, the overall time complexity is O(n log n), which is efficient given the problem constraints.
"""

from typing import List

class Solution:

    def merge_sort(self, elements: List[List[int]]) -> List[List[int]]:
        # Base case: if the list is a single element, return it
        if len(elements) <= 1:
            return elements
    
        # Split the list in half and recursively sort both halves
        mid = len(elements) // 2
        left = self.merge_sort(elements[:mid])
        right = self.merge_sort(elements[mid:])
        
        # Merge the two sorted halves
        return self._merge(left, right)

    def _merge(self, left: List[List[int]], right: List[List[int]]) -> List[List[int]]:
        sorted_list = []
        l_idx = 0
        r_idx = 0
        
        # Merge until one of the halves is exhausted
        while l_idx < len(left) and r_idx < len(right):
            if left[l_idx][1] >= right[r_idx][1]:  # Compare based on the second element
                sorted_list.append(left[l_idx])
                l_idx += 1
            else:
                sorted_list.append(right[r_idx])
                r_idx += 1
        
        # Append any remaining elements from either half
        sorted_list.extend(left[l_idx:])
        sorted_list.extend(right[r_idx:])
        
        return sorted_list

    def maximumUnits(self, boxTypes: List[List[int]], truckSize: int) -> int:
        """
        Given a list of box types and the truck size, calculate the maximum number of units that
        can be loaded onto the truck by prioritizing boxes with the highest units per box.
        """
        # Sort the boxes by the number of units per box in descending order
        # Optionally, you can use merge_sort instead of the built-in sort function
        # boxTypes = self.merge_sort(boxTypes)
        
        boxTypes.sort(key=lambda x: x[1], reverse=True)  # Sort by units per box in descending order
        
        total_units = 0
        for box in boxTypes:
            if truckSize == 0:
                break
            
            # Take as many boxes as the truck can fit, up to the number of boxes available
            count = min(truckSize, box[0])
            total_units += count * box[1]  # Add the units from these boxes to the total
            truckSize -= count  # Decrease the available truck space
        
        return total_units