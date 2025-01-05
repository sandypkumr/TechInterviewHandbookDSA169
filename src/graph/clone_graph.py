from typing import Optional


class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        if not node:
            return None
        visited = {}
        return self.clone(node, visited)

    def clone(self, node, visited):
        if node in visited:
            return visited[node]
        clone_node = Node(node.val)
        visited[node] = clone_node
        for neighbor in node.neighbors:
            clone_node.neighbors.append(self.clone(neighbor, visited))
        return clone_node