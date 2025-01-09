from collections import defaultdict, deque
from typing import List


class Solution:
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        graph = defaultdict(list)
        for u, v, w in flights:
            graph[u].append((v, w))
        dist = [float('inf')] * n
        dist[src] = 0
        queue = deque()
        queue.append((src, 0))
        stops = 0
        while queue:
            for _ in range(len(queue)):
                city, cost = queue.popleft()
                for neighbor, price in graph[city]:
                    if cost + price < dist[neighbor]:
                        dist[neighbor] = cost + price
                        queue.append((neighbor, cost + price))
            stops += 1
            if stops > k:
                break
        return dist[dst] if dist[dst] != float('inf') else -1