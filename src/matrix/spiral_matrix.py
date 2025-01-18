from typing import List


class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        if not matrix:
            return []
        rows, cols = len(matrix), len(matrix[0])
        visited = [[False] * cols for _ in range(rows)]
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        row, col, direction = 0, 0, 0
        spiral = []
        for _ in range(rows * cols):
            spiral.append(matrix[row][col])
            visited[row][col] = True
            next_row, next_col = row + directions[direction][0], col + directions[direction][1]
            if 0 <= next_row < rows and 0 <= next_col < cols and not visited[next_row][next_col]:
                row, col = next_row, next_col
            else:
                direction = (direction + 1) % 4
                row, col = row + directions[direction][0], col + directions[direction][1]
        return spiral