from typing import List


class Solution:
    """
    Problem Statement:
    You are given an m x n integer matrix "matrix" with the following two properties:
    1. Each row is sorted in non-decreasing order.
    2. The first integer of each row is greater than the last integer of the previous row.

    Given an integer "target", return True if target is in matrix or False otherwise.

    The solution must run in O(log(m * n)) time complexity.

    Approach:
    - We treat the 2D matrix as a flattened 1D sorted array and perform binary search.
    - The index "mid" represents a position in this virtual 1D array.
    - We convert "mid" back to 2D indices using:
        - row = mid // cols (integer division gives the row index)
        - col = mid % cols (modulus gives the column index)
    - If matrix[row][col] == target, return True.
    - If matrix[row][col] < target, move "left" to mid + 1.
    - Otherwise, move "right" to mid - 1.
    - Repeat until "left" exceeds "right", meaning target is not found.

    This ensures a binary search approach with O(log(m * n)) complexity.
    """

    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        # Get the number of rows and columns
        rows, cols = len(matrix), len(matrix[0])

        # Helper function to compute the indexes of the element
        # in the matrix, given the flattened index representation
        def to_row_col(n: int) -> tuple[int, int]:
            row = n // cols
            col = n % cols
            return row, col

        # Initialize left and right indexes for binary search
        left, right = 0, rows * cols - 1

        # Perform binary search
        while left <= right:
            # Compute middle element
            mid = (right + left) // 2

            # Convert the index to (row, col) indexes
            row, col = to_row_col(mid)

            # Standard binary search
            if matrix[row][col] == target:
                return True
            elif matrix[row][col] < target:
                left = mid + 1
            else:
                right = mid - 1

        return False
