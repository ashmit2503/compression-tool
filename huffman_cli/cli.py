import click
import os
from .frequency import build_frequency_table
from .tree import build_huffman_tree, serialize_tree, deserialize_tree
from .codes import build_codes
from .io import write_bits_to_file, read_bits_from_file

@click.group()
def cli():
    """Huffman CLI: compress or decompress files"""
    pass

@cli.command()
@click.argument('input', type=click.Path(exists=True))
@click.argument('output', type=click.Path())
def compress(input, output):
    data = open(input, 'rb').read()
    freq = build_frequency_table(data)
    tree = build_huffman_tree(freq)
    codes = build_codes(tree)
    tree_bits = serialize_tree(tree)
    data_bits = ''.join(codes[b] for b in data)
    with open(output, 'wb') as out:
        out.write(len(tree_bits).to_bytes(4, 'big'))
        write_bits_to_file(tree_bits, out)
        write_bits_to_file(data_bits, out)
    click.echo(f"Compressed {input} -> {output}: {len(data)}B to {os.path.getsize(output)}B")

@cli.command()
@click.argument('input', type=click.Path(exists=True))
@click.argument('output', type=click.Path())
def decompress(input, output):
    with open(input, 'rb') as f:
        tree_len = int.from_bytes(f.read(4), 'big')
        num_bytes = (tree_len + 7)//8
        bits = []
        for byte in f.read(num_bytes):
            bits.extend('1' if byte & (1<<(7-i)) else '0' for i in range(8))
        bits = bits[:tree_len]
        tree = deserialize_tree(iter(bits))
        data_bits = list(read_bits_from_file(f))
    out = bytearray()
    node = tree
    for bit in data_bits:
        node = node.right if bit=='1' else node.left
        if node.char is not None:
            out.append(node.char)
            node = tree
    with open(output, 'wb') as f:
        f.write(out)
    click.echo(f"Decompressed {input} -> {output}: {len(out)}B")

@cli.command()
def interactive():
    """Interactive mode"""
    action = click.prompt("choose action", type=click.Choice(['compress', 'decompress']))
    inp = click.prompt("input file path", type=click.Path(exists=True))
    out = click.prompt("output file path")
    if action == 'compress':
        compress.callback(inp, out)
    else:
        decompress.callback(inp, out)