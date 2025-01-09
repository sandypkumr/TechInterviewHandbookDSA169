"""
In an infinite chessboard, a knight is placed at the position (0, 0) and you are given a target position (x, y). Your
task is to determine the minimum number of moves required for the knight to reach the target position.

The knight moves in an "L" shape:

Two squares in one direction and one square in a perpendicular direction.
Or one square in one direction and two squares in a perpendicular direction.
You can assume the target position (x, y) is on the board, and both x and y are integers.

Example 1:
Input: x = 2, y = 1
Output: 1

Example 2:
Input: x = 5, y = 5
Output: 4

"""

from collections import deque


class Solution:
    def minKnightMoves(self, x: int, y: int) -> int:
        x, y = abs(x), abs(y)
        directions = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
        queue = deque([(0, 0, 0)])
        visited = {(0, 0)}
        while queue:
            i, j, steps = queue.popleft()
            if i == x and j == y:
                return steps
            for di, dj in directions:
                ni, nj = i + di, j + dj
                if (ni, nj) not in visited and -2 <= ni <= x + 2 and -2 <= nj <= y + 2:
                    visited.add((ni, nj))
                    queue.append((ni, nj, steps + 1))
        return -1