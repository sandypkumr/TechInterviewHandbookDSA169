class WordDictionary:

    def __init__(self):
        self.trie = {}

    def addWord(self, word: str) -> None:
        node = self.trie
        for char in word:
            if char not in node:
                node[char] = {}
            node = node[char]
        node['$'] = True

    def search(self, word: str) -> bool:
        def dfs(i, node):
            if i == len(word):
                return '$' in node
            if word[i] == '.':
                return any(dfs(i + 1, node[char]) for char in node if char != '$')
            if word[i] not in node:
                return False
            return dfs(i + 1, node[word[i]])

        return dfs(0, self.trie)