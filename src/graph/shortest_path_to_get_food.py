"""

You are given a 2D grid where:

Each cell in the grid can be one of the following:
'*': Your starting position. There is exactly one '*' in the grid.
'#': A food cell. There may be multiple food cells.
'O': An open cell you can walk through.
'X': A blocked cell you cannot walk through.
You need to find the shortest path from your starting position ('*') to any food cell ('#') in the grid. You can move
 up, down, left, or right. Return the number of steps in the shortest path, or -1 if no path exists.

Example 1:
Input: grid =   [["X","X","X","X","X","X"],
                 ["X","*","O","O","O","X"],
                 ["X","O","O","#","O","X"],
                 ["X","X","X","X","X","X"]]
Output: 3
Explanation: It takes 3 steps to reach the food.

"""
from typing import List


class Solution:
    def getFood(self, grid: List[List[str]]) -> int:
        if not grid:
            return -1
        rows, cols = len(grid), len(grid[0])
        queue = [(i, j) for i in range(rows) for j in range(cols) if grid[i][j] == '*']
        steps = 0
        while queue:
            steps += 1
            for _ in range(len(queue)):
                i, j = queue.pop(0)
                for x, y in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
                    if 0 <= x < rows and 0 <= y < cols and grid[x][y] != 'X':
                        if grid[x][y] == '#':
                            return steps
                        grid[x][y] = 'X'
                        queue.append((x, y))
        return -1