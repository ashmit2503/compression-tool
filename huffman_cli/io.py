from .tree import serialize_tree, deserialize_tree

def write_bits_to_file(bitstring: str, outfile):
    b = bytearray()
    for i in range(0, len(bitstring), 8):
        chunk = bitstring[i:i+8].ljust(8, '0')
        b.append(int(chunk, 2))
    outfile.write(b)


def read_bits_from_file(infile):
    for byte in infile.read():
        for i in range(8):
            yield '1' if byte & (1 << (7-i)) else '0'