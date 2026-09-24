import sys


class Trie:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.words = set()
        self.word_count = 0

    def insert(self, word: str):
        self.words.add(word)
        self.word_count += 1

    def contains(self, word: str) -> bool:
        return word in self.words

    def size(self) -> int:
        return self.word_count


trie = Trie()

# for raw in sys.stdin:
#     line = raw.rstrip("\n")
#     if not line:
#         continue
#     parts = line.split(" ", 1)
#     cmd = parts[0]
#     arg = parts[1] if len(parts) > 1 else ""
#     if cmd == "INSERT":
#         # TODO: walk `arg` from root, creating a Trie() node for any missing
#         # character. Mark the final node's is_end = True; if it wasn't
#         # already an end node, increment size_count. Append "OK" to out.
#         pass
#     elif cmd == "CONTAINS":
#         # TODO: walk `arg` from root. If any character is missing, append
#         # "NO". Otherwise append "YES" if the final node's is_end is True,
#         # else "NO".
#         pass
#     elif cmd == "SIZE":
#         out.append(str(size_count))

for line in filter(None, map(str.strip, sys.stdin)):
    cmd, _, word = line.partition(" ")
    if cmd == "INSERT" and word:
        trie.insert(word)
        print("OK")
    elif cmd == "CONTAINS" and word:
        print("YES" if trie.contains(word) else "NO")
    elif cmd == "SIZE":
        print(f"{trie.size()}")
