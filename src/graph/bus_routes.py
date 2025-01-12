from collections import defaultdict, deque
from typing import List


class Solution:
    def numBusesToDestination(self, routes: List[List[int]], source: int, target: int) -> int:
        graph = defaultdict(set)
        for i, route in enumerate(routes):
            for stop in route:
                graph[stop].add(i)

        queue = deque([(source, 0)])
        visited = {source}
        while queue:
            stop, count = queue.popleft()
            if stop == target:
                return count
            for bus in graph[stop]:
                for next_stop in routes[bus]:
                    if next_stop not in visited:
                        visited.add(next_stop)
                        queue.append((next_stop, count + 1))
                routes[bus] = []
        return -1