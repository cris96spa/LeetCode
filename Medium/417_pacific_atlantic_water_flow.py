class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        """
        Problem Description:
        There is an m x n rectangular island that borders both the Pacific Ocean and Atlantic Ocean. The Pacific Ocean touches
        the island's left and top edges, and the Atlantic Ocean touches the island's right and bottom edges.

        The island is partitioned into a grid of square cells. You are given an m x n integer matrix heights where heights[r][c]
        represents the height above sea level of the cell at coordinate (r, c).

        The island receives a lot of rain, and the rainwater can flow to neighboring cells directly north, south, east, and west
        if the neighboring cell's height is less than or equal to the current cell's height. Water can flow from any cell adjacent
        to an ocean into the ocean.

        Return a 2D list of grid coordinates result where result[i] = [ri, ci] denotes that rainwater can flow from cell (ri, ci)
        to both the Pacific and Atlantic oceans.

        Constraints:
        - m == heights.length
        - n == heights[r].length
        - 1 <= m, n <= 200
        - 0 <= heights[r][c] <= 10^5

        Example 1:
        Input: heights = [[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]
        Output: [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]
        Explanation: The following cells can flow to both oceans:
        [0,4]: Pacific ocean touches the left and top edges, and Atlantic ocean touches the right and bottom edges.
        Water can flow from [0,4] to [1,3] and [1,4], which flow to both oceans.

        Example 2:
        Input: heights = [[2,1],[1,2]]
        Output: [[0,0],[0,1],[1,0],[1,1]]
        Explanation: The following cells can flow to both oceans:
        [0,0]: Pacific ocean touches the left and top edges, and Atlantic ocean touches the right and bottom edges.

        Writeup:
        This solution employs a depth-first search (DFS) approach to simulate water flow. The algorithm:
        1. Starts DFS from the borders of the Pacific and Atlantic oceans, marking cells that can flow to each ocean.
        2. Uses two matrices (`pacific` and `atlantic`) to track visited cells for each ocean.
        3. Expands the DFS to adjacent cells if the water can flow (i.e., the next cell's height is greater than or equal to the current cell).
        4. After the DFS, checks for cells reachable from both oceans by iterating through the grid and finding cells marked as true in both matrices.

        The algorithm is efficient with a time complexity of O(m * n), where m is the number of rows and n is the number of columns,
        as each cell is visited at most twice. The space complexity is also O(m * n) due to the use of visited matrices.
        """

        rows, cols = len(heights), len(heights[0])
        # Base check
        if rows == 1:
            return [[0, col] for col in range(cols)]
        if cols == 1:
            return [[row, 0] for row in range(rows)]

        possible_actions = [
            (-1, 0),  # left
            (1, 0),  # right
            (0, 1),  # up
            (0, -1),  # down
        ]

        # Keep track of visited states
        pacific = [[False] * cols for _ in range(rows)]
        atlantic = [[False] * cols for _ in range(rows)]

        def dfs(r: int, c: int, visited: list[list[bool]], prev_height: int) -> None:
            # Check if already visited or if it is ocean or if
            # can not flow in that direction to define the base
            # case of the recursion
            if (
                r < 0
                or r > rows - 1
                or c < 0
                or c > cols - 1
                or visited[r][c]
                or heights[r][c] < prev_height
            ):
                return

            # Mark the state as visited
            visited[r][c] = True

            for dx, dy in possible_actions:
                # Check all adjacent states
                dfs(r + dx, c + dy, visited, heights[r][c])

        # We will now perform a dfs starting from all borders
        # The inner cells will be visited during the search if
        # the water can down from them
        for row in range(rows):
            # Check pacific borders
            dfs(row, 0, pacific, heights[row][0])
            # Check atlantic borders
            dfs(row, cols - 1, atlantic, heights[row][cols - 1])

        for col in range(cols):
            # Check pacific borders
            dfs(0, col, pacific, heights[0][col])
            # Check atlantic borders
            dfs(rows - 1, col, atlantic, heights[rows - 1][col])

        results = []
        # Check if a both pacific and atlantic were reachable from a state
        for r in range(rows):
            for c in range(cols):
                if pacific[r][c] and atlantic[r][c]:
                    results.append([r, c])

        return results
