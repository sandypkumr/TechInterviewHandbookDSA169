from collections import deque
from typing import List


class Solution:
    def updateMatrix(self, mat: List[List[int]]) -> List[List[int]]:
        rows, cols = len(mat), len(mat[0])
        queue = deque()
        for i in range(rows):
            for j in range(cols):
                if mat[i][j] == 0:
                    queue.append((i, j))
                else:
                    mat[i][j] = float('inf')
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        while queue:
            cell = queue.popleft()
            for direction in directions:
                i, j = cell[0] + direction[0], cell[1] + direction[1]
                if i < 0 or j < 0 or i >= rows or j >= cols or mat[i][j] <= mat[cell[0]][cell[1]] + 1:
                    continue
                queue.append((i, j))
                mat[i][j] = mat[cell[0]][cell[1]] + 1
        return mat