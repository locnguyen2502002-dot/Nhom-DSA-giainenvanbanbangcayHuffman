import heapq
from collections import Counter


# 1. Tao nut trong cay Huffman
class Node:
    def __init__(self, char, freq, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq


# 2. Dem tan suat ky tu
def count_frequency(text):
    return Counter(text)


# 3. Xay dung cay Huffman
def build_huffman_tree(freq_table):
    if not freq_table:
        return None

    heap = []

    for char, freq in freq_table.items():
        node = Node(char, freq)
        heapq.heappush(heap, node)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        parent = Node(
            None,
            left.freq + right.freq,
            left,
            right
        )

        heapq.heappush(heap, parent)

    return heapq.heappop(heap)


# 4. Tao bang ma Huffman
def generate_codes(root):
    codes = {}

    if root is None:
        return codes

    def dfs(node, code):
        if node.char is not None:
            codes[node.char] = code if code else "0"
            return

        dfs(node.left, code + "0")
        dfs(node.right, code + "1")

    dfs(root, "")
    return codes


# 5. Ma hoa van ban
def encode(text, codes):
    return "".join(codes[char] for char in text)


# 6. Giai ma chuoi bit
def decode(bits, root):
    if root is None:
        return ""

    # Truong hop cay chi co mot nut
    if root.char is not None:
        if any(bit != "0" for bit in bits):
            raise ValueError("Chuoi bit khong hop le")
        return root.char * len(bits)

    result = []
    current = root

    for bit in bits:
        if bit == "0":
            current = current.left
        elif bit == "1":
            current = current.right
        else:
            raise ValueError("Chuoi chi duoc chua bit 0 va 1")

        if current is None:
            raise ValueError("Chuoi bit khong hop le")

        if current.char is not None:
            result.append(current.char)
            current = root

    if current is not root:
        raise ValueError("Chuoi bit bi thieu")

    return "".join(result)