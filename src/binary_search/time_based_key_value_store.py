from collections import defaultdict


class TimeMap:

        def __init__(self):
            """
            Initialize your data structure here.
            """
            self.map = defaultdict(list)

        def set(self, key: str, value: str, timestamp: int) -> None:
            self.map[key].append((timestamp, value))

        def get(self, key: str, timestamp: int) -> str:
            if key not in self.map:
                return ""
            arr = self.map[key]
            left, right = 0, len(arr) - 1
            while left < right:
                mid = (left + right + 1) // 2
                if arr[mid][0] <= timestamp:
                    left = mid
                else:
                    right = mid - 1
            return arr[left][1] if arr[left][0] <= timestamp else ""