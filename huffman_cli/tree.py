import heapq

class Node:
    def __init__(self, freq: int, char: int | None = None, left=None, right=None):
        self.freq = freq
        self.char = char
        self.left = left
        self.right = right
    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree(freq: dict[int, int]) -> Node | None:
    heap = [Node(f, c) for c, f in freq.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, merged)
    return heap[0] if heap else None


def serialize_tree(node: Node, bits: list[str] = []) -> str:
    if node.char is not None:
        bits.append('1')
        bits.append(f"{node.char:08b}")
    else:
        bits.append('0')
        serialize_tree(node.left, bits)
        serialize_tree(node.right, bits)
    return ''.join(bits)


def deserialize_tree(bits_iter) -> Node | None:
    try:
        flag = next(bits_iter)
    except StopIteration:
        return None
    if flag == '1':
        byte = ''.join(next(bits_iter) for _ in range(8))
        return Node(0, char=int(byte, 2))
    left = deserialize_tree(bits_iter)
    right = deserialize_tree(bits_iter)
    return Node(0, left=left, right=right)