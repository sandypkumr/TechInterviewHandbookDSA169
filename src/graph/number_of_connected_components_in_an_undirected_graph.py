"""

You are given an integer n representing the number of nodes labeled from 0 to n-1 and a list of edges where each edge
is a pair of nodes [u, v] that represents an undirected edge between nodes u and v.

Write a function to return the number of connected components in the graph.

Example 1:
Input: n = 5, edges = [[0,1],[1,2],[3,4]]
Output: 2

Example 2:
Input: n = 5, edges = [[0,1],[1,2],[2,3],[3,4]]
Output: 1

"""
from typing import List


class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        graph = {i: [] for i in range(n)}
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)
        visited = set()
        def dfs(node):
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    dfs(neighbor)
        count = 0
        for i in range(n):
            if i not in visited:
                count += 1
                dfs(i)
        return count