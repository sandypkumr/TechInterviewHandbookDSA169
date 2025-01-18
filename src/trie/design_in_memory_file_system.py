"""

You need to design an in-memory file system that supports the following operations:

- ls: Given a path in string format. If it is a file path, return a list that only contains this file's name. If it is
a directory path, return the list of file and directory names in this directory. Your output (file and directory names
together) should in lexicographic order.

- mkdir: Given a directory path that does not exist, you should make a new directory according to the path. If the middle
directories in the path don't exist either, you should create them as well. This function has void return type.

- addContentToFile: Given a file path and file content in string format. If the file doesn't exist, you need to create
that file containing given content. If the file already exists, you need to append the given content to original content.
This function has void return type.

- readContentFromFile: Given a file path, return its content in string format.

Example 1:

Input
["FileSystem", "ls", "mkdir", "addContentToFile", "ls", "readContentFromFile"]
[[], ["/"], ["/a/b/c"], ["/a/b/c/d", "hello"], ["/"], ["/a/b/c/d"]]
Output
[null, [], null, null, ["a"], "hello"]

"""


from typing import List


class FileSystem:
    def __init__(self):
        self.root = {}

    def ls(self, path: str) -> List[str]:
        node = self.root
        if path != '/':
            for p in path.split('/')[1:]:
                node = node[p]
        if isinstance(node, str):
            return [path.split('/')[-1]]
        return sorted(node.keys())

    def mkdir(self, path: str) -> None:
        node = self.root
        for p in path.split('/')[1:]:
            node = node.setdefault(p, {})

    def addContentToFile(self, filePath: str, content: str) -> None:
        node = self.root
        parts = filePath.split('/')[1:]
        for p in parts[:-1]:
            node = node.setdefault(p, {})
        node[parts[-1]] = node.get(parts[-1], '') + content

    def readContentFromFile(self, filePath: str) -> str:
        node = self.root
        for p in filePath.split('/')[1:]:
            node = node[p]
        return node