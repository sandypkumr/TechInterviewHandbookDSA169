from typing import List


class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        if n == 0:
            return len(tasks)
        task_count = [0] * 26
        for task in tasks:
            task_count[ord(task) - ord('A')] += 1
        task_count.sort()
        max_task = task_count[-1] - 1
        idle_slots = max_task * n
        for i in range(24, -1, -1):
            idle_slots -= min(max_task, task_count[i])
        return len(tasks) + max(0, idle_slots)