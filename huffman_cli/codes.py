from .tree import Node

def build_codes(node: Node, prefix: str = "", table: dict[int, str] = None) -> dict[int, str]:
    if table is None:
        table = {}
    if node is None:
        return table
    if node.char is not None:
        table[node.char] = prefix or "0"
    else:
        build_codes(node.left, prefix + "0", table)
        build_codes(node.right, prefix + "1", table)
    return table