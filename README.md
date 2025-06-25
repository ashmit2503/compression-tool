# Huffman Compression Tool

A command-line tool for compressing and decompressing files using Huffman coding, implemented in Python.

## Features
- **Compress**: Reduce file size using Huffman encoding.
- **Decompress**: Restore compressed files to their original form.
- **Interactive Mode**: User-friendly prompts for compression and decompression.

## Installation

1. Clone the repository:
   ```sh
   git clone <repo-url>
   cd compression-tool
   ```
2. (Optional) Create and activate a virtual environment:
   ```sh
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   source venv/bin/activate   # On Unix/Mac
   ```
3. Install dependencies:
   ```sh
   pip install .
   ```

## Usage

You can use the tool via the command line:

### Compress a file
```sh
python -m huffman_cli compress <input_file> <output_file>
```

### Decompress a file
```sh
python -m huffman_cli decompress <input_file> <output_file>
```

### Interactive mode
```sh
python -m huffman_cli interactive
```

## Example

Compress a file:
```sh
python -m huffman_cli compress tests/raw/small.txt tests/compressed/small.txt.huff
```

Decompress a file:
```sh
python -m huffman_cli decompress tests/compressed/small.txt.huff tests/decompressed/small.txt
```

## Project Structure

- `huffman_cli/` — Main package with CLI and Huffman logic
- `tests/` — Test files and results
- `run_huffman_tests.py` — Script to run tests
- `pyproject.toml` — Project metadata and dependencies

## How It Works

- **Compression**: Reads the input file, builds a frequency table, constructs a Huffman tree, encodes the data, and writes the compressed output.
- **Decompression**: Reads the compressed file, reconstructs the Huffman tree, decodes the data, and writes the original file.
