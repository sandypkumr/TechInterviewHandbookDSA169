from collections import defaultdict
from typing import List


class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        email_to_index = defaultdict(list)
        for i, account in enumerate(accounts):
            for email in account[1:]:
                email_to_index[email].append(i)
        def dfs(k):
            visited[k] = True
            for cur_email in accounts[k][1:]:
                emails.add(cur_email)
                for j in email_to_index[cur_email]:
                    if not visited[j]:
                        dfs(j)
        visited = [False] * len(accounts)
        result = []
        for i in range(len(accounts)):
            if visited[i]:
                continue
            emails = set()
            dfs(i)
            result.append([accounts[i][0]] + sorted(emails))
        return result
