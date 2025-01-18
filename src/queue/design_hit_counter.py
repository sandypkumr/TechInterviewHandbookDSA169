"""

Design a hit counter which counts the number of hits received in the past 5 minutes.

Each function accepts a timestamp parameter (in seconds granularity) and you may assume that calls are being made to
the system in chronological order (i.e., timestamp is monotonically increasing). You may assume that the earliest
timestamp starts at 1.

It is possible that several hits arrive roughly at the same time.

Implement the HitCounter class:

HitCounter() Initializes the object of the hit counter system.

void hit(int timestamp) Records a hit that happened at the given timestamp.

int getHits(int timestamp) Returns the number of hits in the past 5 minutes from the given timestamp.

Example 1:

Input
["HitCounter", "hit", "hit", "hit", "getHits", "hit", "getHits"]
[[], [1], [2], [3], [4], [300], [300]]
Output
[null, null, null, null, 3, null, 4]

"""

from collections import deque


class HitCounter:
    def __init__(self):
        self.hits = deque()

    def hit(self, timestamp: int) -> None:
        if not self.hits or self.hits[-1][0] != timestamp:
            self.hits.append([timestamp, 1])
        else:
            self.hits[-1][1] += 1

    def getHits(self, timestamp: int) -> int:
        while self.hits and timestamp - self.hits[0][0] >= 300:
            self.hits.popleft()
        return sum(hit[1] for hit in self.hits)