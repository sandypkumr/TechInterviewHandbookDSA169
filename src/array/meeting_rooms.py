"""

The "Meeting Rooms" problem is about determining if a person can attend all their meetings without overlap. Given an
array of intervals where each interval represents a meeting time [start, end], the goal is to check if any of these
intervals overlap. If there’s overlap, return False; otherwise, return True.

For example:

Input: [[0, 30], [5, 10], [15, 20]]
Output: False (since the meetings overlap).

"""
from typing import List

class Interval(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end


class Solution:
    def canAttendMeetings(self, intervals: List[Interval]) -> bool:
        intervals.sort(key=lambda x: x.start)
        for i in range(1, len(intervals)):
            if intervals[i].start < intervals[i - 1].end:
                return False
        return True
