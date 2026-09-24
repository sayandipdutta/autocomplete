import sys

class Trie:
    def __init__(self):
        self.children = {}
        self.is_end = False

root = Trie()
size_count = 0
out = []

for raw in sys.stdin:
    line = raw.rstrip("\n")
    if not line: continue
    parts = line.split(" ", 1)
    cmd = parts[0]; arg = parts[1] if len(parts) > 1 else ""
    if cmd == "INSERT":
        # TODO: walk `arg` from root, creating a Trie() node for any missing
        # character. Mark the final node's is_end = True; if it wasn't
        # already an end node, increment size_count. Append "OK" to out.
        pass
    elif cmd == "CONTAINS":
        # TODO: walk `arg` from root. If any character is missing, append
        # "NO". Otherwise append "YES" if the final node's is_end is True,
        # else "NO".
        pass
    elif cmd == "SIZE":
        out.append(str(size_count))

print("\n".join(out))
