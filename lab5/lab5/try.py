class Node:
    def __init__(self):
        self.children = {}
        self.fail = None
        self.output = []

node_count = 0

def build_trie(patterns):
    global node_count
    root = Node()
    node_count = 1
    for pattern in patterns:
        node = root
        for char in pattern:
            if char not in node.children:
                node.children[char] = Node()
                node_count += 1
            node = node.children[char]
        node.output.append(patterns.index(pattern))
    return root

def build_links(root):
    queue = []
    for child in root.children.values():
        child.fail = root
        queue.append(child)
    while queue:
        current = queue.pop(0)
        for char, child in current.children.items():
            fail_node = current.fail
            while fail_node and char not in fail_node.children:
                fail_node = fail_node.fail
            child.fail = fail_node.children[char] if fail_node and char in fail_node.children else root
            child.output += child.fail.output
            queue.append(child)

def aho_corasick(text, patterns):
    root = build_trie(patterns)
    build_links(root)
    node = root
    result = []
    for i, char in enumerate(text):
        while node and char not in node.children:
            node = node.fail
        node = node.children[char] if node and char in node.children else root
        for pattern_id in node.output:
            start = i - len(patterns[pattern_id]) + 1
            end = i
            result.append((start, end, pattern_id + 1))
    return result


text = input().strip()
n = int(input())
patterns = [input().strip() for _ in range(n)]

matches = aho_corasick(text, patterns)

print(node_count)

intersecting = set()
matches.sort()
for i in range(len(matches)):
    for j in range(i + 1, len(matches)):
        s1, e1, id1 = matches[i]
        s2, e2, id2 = matches[j]
        if s2 > e1:
            break
        if e2 >= s1:
            intersecting.add(id1)
            intersecting.add(id2)

for id in sorted(intersecting):
    print(id)

for s, e, id in sorted(matches):
    print(s + 1, id)
