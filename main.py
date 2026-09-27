import sys
from pprint import pprint
from threading import Lock, RLock

rlock = RLock()


class Trie:
    def __init__(self):
        self.children: dict[str, Trie] = {}
        self.is_end = False
        self.count = 0
        self.num_uniques = 0
        self._num_nodes = 0
        self._num_nodes_upto_date = True
        self._lock = Lock()

    @property
    def node_count(self) -> int:
        with self._lock:
            if not self._num_nodes_upto_date:
                self._num_nodes = self._count_nodes()
                self._num_nodes_upto_date = True
            return self._num_nodes

    def _count_nodes(self) -> int:
        return sum(
            (child._count_nodes() for child in self.children.values()),
            start=1,
        )

    def insert(self, word: str) -> bool:
        with self._lock:
            self._num_nodes_upto_date = False
            new_child = self
            for c in word:
                new_child = new_child.children.setdefault(c, Trie())
                new_child.count += 1
            already_marked = new_child.is_end
            if not already_marked:
                self.num_uniques += 1
            new_child.is_end = True
            return already_marked

    def delete(self, word: str) -> bool:
        with self._lock:
            deleted = False
            self._num_nodes_upto_date = False
            node = self.find_substr(word, complete=True)
            if node is not None:
                node.is_end = False
                deleted = True
                self.num_uniques -= 1
            self.prune()
            return deleted

    def prune(self):
        with rlock:
            chars_to_delete = []
            for char, child in self.children.items():
                if child.is_end:
                    continue
                if not child.children:
                    chars_to_delete.append(char)
                else:
                    child.prune()
                    if not child.children:
                        chars_to_delete.append(char)
            for char in chars_to_delete:
                del self.children[char]

    def find_substr(self, prefix: str, complete: bool = True) -> Trie | None:
        child = self
        for c in prefix:
            child = child.children.get(c)
            if not child:
                return None
        if complete and not child.is_end:
            return None
        return child

    def prefix_matches(self, prefix: str) -> list[str]:
        node = self.find_substr(prefix, complete=False)
        matches = []
        if node is not None:
            if node.is_end:
                matches.append(prefix)
            for choice in node.walk_words():
                matches.append("".join((prefix, *choice)))
        return matches

    def walk_words(self):
        for char in sorted(self.children):
            node = self.children[char]
            if node.is_end:
                yield char
            yield from ((char, *word) for word in node.walk_words())

    def contains(self, word: str) -> bool:
        return self.find_substr(word) is not None

    def frequency(self, word: str) -> int:
        return node.count if (node := self.find_substr(word)) else 0

    def __repr__(self):
        return (
            f"Trie(children={self.children}, is_end={self.is_end}, count={self.count})"
        )


class WordStore:
    def __init__(self):
        self._root = Trie()

    def insert(self, word: str):
        return self._root.insert(word)

    def contains(self, word: str) -> bool:
        return self._root.contains(word)

    __contains__ = contains

    def frequency(self, word: str) -> int:
        return self._root.frequency(word)

    def node_count(self) -> int:
        return self._root.node_count

    def prefix_matches(self, prefix: str) -> list[str]:
        return self._root.prefix_matches(prefix)

    def delete(self, word: str):
        self._root.delete(word)

    __delitem__ = delete

    def __len__(self) -> int:
        return self._root.num_uniques

    def _inspect(self):
        pprint(f"WordStore(_store={self._root}, nunique={len(self)})")


words = WordStore()

for line in filter(None, map(str.strip, sys.stdin)):
    cmd, _, word = line.partition(" ")
    match (cmd, word):
        case "INSERT", word:
            words.insert(word)
            print("OK")
        case "CONTAINS", word:
            print("YES" if word in words else "NO")
        case "PREFIX", word:
            print(",".join(words.prefix_matches(word)) or "none")
        case "DELETE", word:
            del words[word]
        case "FREQ", _:
            print(words.frequency(word))
        case "SIZE", _:
            print(len(words))
        case "NODES", _:
            print(words.node_count())
        case "DEBUG", _:
            words._inspect()
