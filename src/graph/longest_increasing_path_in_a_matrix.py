from typing import List


class Solution:
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        if not matrix:
            return 0
        rows, cols = len(matrix), len(matrix[0])
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        cache = [[0] * cols for _ in range(rows)]

        def dfs(row: int, col: int) -> int:
            if cache[row][col]:
                return cache[row][col]
            for dx, dy in directions:
                new_row, new_col = row + dx, col + dy
                if 0 <= new_row < rows and 0 <= new_col < cols and matrix[new_row][new_col] > matrix[row][col]:
                    cache[row][col] = max(cache[row][col], dfs(new_row, new_col))
            cache[row][col] += 1
            return cache[row][col]

        return max(dfs(i, j) for i in range(rows) for j in range(cols))