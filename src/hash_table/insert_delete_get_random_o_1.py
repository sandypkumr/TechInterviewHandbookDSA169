from random import choice


class RandomizedSet:

    def __init__(self):
        self.hash_map = {}
        self.list = []

    def insert(self, val: int) -> bool:
        if val in self.hash_map:
            return False
        self.hash_map[val] = len(self.list)
        self.list.append(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.hash_map:
            return False
        index = self.hash_map[val]
        last_element = self.list[-1]
        self.list[index], self.hash_map[last_element] = last_element, index
        self.list.pop()
        del self.hash_map[val]
        return True

    def getRandom(self) -> int:
        return choice(self.list)