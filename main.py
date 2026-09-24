import sys
from threading import Lock
from typing import Dict, Union  # ruff:ignore[deprecated-import]


class Trie:
    def __init__(self):
        self.children: Dict[str, Trie] = {}  # ruff:ignore[non-pep585-annotation]
        self.is_end = False
        self.count = 0
        self._num_nodes = 0
        self.num_nodes_upto_date = True
        self.lock = Lock()

    @property
    def node_count(self) -> int:
        with self.lock:
            if not self.num_nodes_upto_date:
                self._num_nodes = self._count_nodes()
                self.num_nodes_upto_date = True
            return self._num_nodes

    def _count_nodes(self) -> int:
        return sum(
            (child._count_nodes() for child in self.children.values()),
            start=len(self.children),
        )

    def insert(self, word: str) -> bool:
        with self.lock:
            self.num_nodes_upto_date = False
            new_child = self
            for c in word:
                new_child = new_child.children.setdefault(c, Trie())
                new_child.count += 1
            already_marked = new_child.is_end
            new_child.is_end = True
            return already_marked

    def match_prefix(self, word: str) -> "Union[Trie, None]":  # ruff:ignore[non-pep604-annotation-union]
        child = self
        for c in word:
            child = child.children.get(c)
            if not child:
                return None
        return child if child.is_end else None

    def contains(self, word: str) -> bool:
        return self.match_prefix(word) is not None

    def frequency(self, word: str) -> int:
        return node.count if (node := self.match_prefix(word)) else 0

    def __repr__(self):
        return (
            f"Trie(children={self.children}, is_end={self.is_end}, count={self.count})"
        )


class WordStore:
    def __init__(self):
        self._root = Trie()
        self.num_uniques = 0

    def insert(self, word: str):
        already_marked = self._root.insert(word)
        if not already_marked:
            self.num_uniques += 1

    def contains(self, word: str):
        return self._root.contains(word)

    def frequency(self, word: str) -> int:
        return self._root.frequency(word)

    def node_count(self) -> int:
        return self._root.node_count

    def _inspect(self):
        print(f"WordStore(_store={self._root}, nunique={self.num_uniques})")


words = WordStore()

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
    if cmd == "INSERT":
        words.insert(word)
        # print("OK")
        # words._inspect()
    # elif cmd == "CONTAINS":
    #     print("YES" if words.contains(word) else "NO")
    elif cmd == "FREQ":
        print(words.frequency(word))
    elif cmd == "SIZE":
        print(words.num_uniques)
    elif cmd == "NODES":
        print(words.node_count())
