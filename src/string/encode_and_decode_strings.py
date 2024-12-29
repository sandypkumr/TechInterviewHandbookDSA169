"""

Design an algorithm to encode a list of strings to a string. The encoded string is then sent over the network and is
decoded back to the original list of strings.

Please implement encode and decode

Example:
    Input: ["Hello", "World", "this is a test"]
    codec = Solution()
    encoded_string = codec.encode(["Hello", "World", "this is a test"])
    print(encoded_string)
    Output: "5#Hello5#World14#this is a test"
    decoded_string = codec.decode(encoded_string)
    print(decoded_string)
    Output: ["Hello", "World", "this is a test"]

"""
from typing import List


class Solution:
    def encode(self, strs: List[str]) -> str:
        return ''.join(str(len(s)) + '#' + s for s in strs)

    def decode(self, s: str) -> List[str]:
        res = []
        i = 0
        while i < len(s):
            j = i
            while s[j] != '#':
                j += 1
            length = int(s[i:j])
            res.append(s[j + 1:j + 1 + length])
            i = j + 1 + length
        return res