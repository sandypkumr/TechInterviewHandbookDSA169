from typing import List


class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        graph = {i: [] for i in range(numCourses)}
        indegree = {i: 0 for i in range(numCourses)}
        for u, v in prerequisites:
            graph[v].append(u)
            indegree[u] += 1
        queue = [i for i in indegree if indegree[i] == 0]
        order = []
        while queue:
            node = queue.pop(0)
            order.append(node)
            for neighbor in graph[node]:
                indegree[neighbor] -= 1
                if indegree[neighbor] == 0:
                    queue.append(neighbor)
        return order if len(order) == numCourses else []