from typing import List


class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        if not heights:
            return []
        rows, cols = len(heights), len(heights[0])
        pacific, atlantic = set(), set()
        def dfs(i, j, ocean):
            ocean.add((i, j))
            for x, y in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
                if 0 <= x < rows and 0 <= y < cols and (x, y) not in ocean and heights[x][y] >= heights[i][j]:
                    dfs(x, y, ocean)
        for i in range(rows):
            dfs(i, 0, pacific)
            dfs(i, cols - 1, atlantic)
        for j in range(cols):
            dfs(0, j, pacific)
            dfs(rows - 1, j, atlantic)
        return list(pacific & atlantic)