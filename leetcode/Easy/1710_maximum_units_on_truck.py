from typing import List


class Solution:
    """Maximize the total units loaded onto a truck given a capacity constraint.

    Problem Statement:
        Given a 2D list boxTypes where boxTypes[i] = [numberOfBoxes,
        numberOfUnitsPerBox], and an integer truckSize representing the maximum
        number of boxes the truck can hold, return the maximum total units that
        can be loaded without exceeding truckSize.

    Approach:
        Greedy: Sort box types by units per box in descending order so that the
        most valuable boxes are loaded first. Greedily take as many boxes as
        possible from each type until the truck is full. A custom merge sort
        helper is also provided as an alternative sorter.

    Complexity:
        Time: O(n log n) for sorting, where n is the number of box types.
        Space: O(1) when using the built-in sort; O(n) when using merge_sort.
    """

    def merge_sort(self, elements: List[List[int]]) -> List[List[int]]:
        if len(elements) <= 1:
            return elements

        mid = len(elements) // 2
        left = self.merge_sort(elements[:mid])
        right = self.merge_sort(elements[mid:])
        return self._merge(left, right)

    def _merge(self, left: List[List[int]], right: List[List[int]]) -> List[List[int]]:
        sorted_list = []
        l_idx, r_idx = 0, 0

        while l_idx < len(left) and r_idx < len(right):
            if left[l_idx][1] >= right[r_idx][1]:
                sorted_list.append(left[l_idx])
                l_idx += 1
            else:
                sorted_list.append(right[r_idx])
                r_idx += 1

        sorted_list.extend(left[l_idx:])
        sorted_list.extend(right[r_idx:])
        return sorted_list

    def maximumUnits(self, boxTypes: List[List[int]], truckSize: int) -> int:
        boxTypes.sort(key=lambda x: x[1], reverse=True)

        total_units = 0
        for box in boxTypes:
            if truckSize == 0:
                break
            count = min(truckSize, box[0])
            total_units += count * box[1]
            truckSize -= count

        return total_units
