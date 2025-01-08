"""

You are given a graph represented as an integer n (the number of nodes, labeled from 0 to n-1) and a list of edges
where each edge is a pair of nodes [u, v] that connects two nodes in the graph.

Write a function to determine if the graph is a valid tree.

A valid tree must satisfy the following conditions:

It is connected (there is a path between any two nodes).
It contains no cycles.

Example 1:
Input: n = 5, edges = [[0,1],[0,2],[0,3],[1,4]]
Output: true

Example 2:
Input: n = 5, edges = [[0,1],[1,2],[2,3],[1,3],[1,4]]
Output: false

"""
from typing import List


class Solution:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        if n - 1 != len(edges):
            return False
        parent = list(range(n))
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        def union(x, y):
            root_x, root_y = find(x), find(y)
            if root_x == root_y:
                return False
            parent[root_x] = root_y
            return True
        for u, v in edges:
            if not union(u, v):
                return False
        return True