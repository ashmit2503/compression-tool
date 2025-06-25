#!/usr/bin/env python3
import os
import subprocess
import random
import string
from pathlib import Path

# Configuration: filenames and target sizes (in bytes)
FILE_SPECS = {
    "small.txt": 1 * 1024 * 1024,    # 1 MB
    "medium.txt": 5 * 1024 * 1024,   # 5 MB
    "large.txt": 10 * 1024 * 1024,   # 10 MB
}

def generate_random_text_file(path: Path, size: int):
    """Generate a file of ~`size` bytes of random lowercase text + spaces."""
    chunk = "".join(random.choices(string.ascii_lowercase + " ", k=4096))
    with path.open("w", encoding="utf-8") as f:
        written = 0
        while written < size:
            to_write = min(len(chunk), size - written)
            f.write(chunk[:to_write])
            written += to_write

def ensure_dirs(base: Path):
    for sub in ("raw", "compressed", "decompressed"):
        d = base / sub
        d.mkdir(exist_ok=True)

def run_cli(command: list[str]):
    """Run the huffman_cli command, raising on error."""
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERROR {' '.join(command)}:")
        print(result.stderr)
        raise RuntimeError("CLI call failed")
    return result.stdout

def human_readable(n: int) -> str:
    """Convert bytes to human-readable form."""
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f}{unit}"
        n /= 1024
    return f"{n:.1f}TB"

def main():
    base = Path(__file__).parent.resolve()
    raw_dir = base / "raw"
    comp_dir = base / "compressed"
    decomp_dir = base / "decompressed"
    log_path = base / "results.log"

    ensure_dirs(base)

    # 1. Generate
    print("Generating raw files…")
    for name, size in FILE_SPECS.items():
        p = raw_dir / name
        if not p.exists() or p.stat().st_size != size:
            generate_random_text_file(p, size)

    # Prepare log
    with log_path.open("w", encoding="utf-8") as log:
        header = f"{'File':<12} {'Raw Size':>10} {'Comp Size':>12} {'Ratio':>8}\n"
        log.write(header)
        log.write("-" * len(header) + "\n")

        # 2/3. Compress & Decompress
        for name in FILE_SPECS:
            raw_path = raw_dir / name
            comp_path = comp_dir / (name + ".huff")
            decomp_path = decomp_dir / name

            # Compress
            print(f"Compressing {name}…")
            run_cli(["huffman_cli", "compress", str(raw_path), str(comp_path)])

            # Decompress
            print(f"Decompressing {name}…")
            run_cli(["huffman_cli", "decompress", str(comp_path), str(decomp_path)])

            # 4. Stats
            raw_size = raw_path.stat().st_size
            comp_size = comp_path.stat().st_size
            ratio = (1 - comp_size / raw_size) * 100

            log.write(
                f"{name:<12} "
                f"{human_readable(raw_size):>10} "
                f"{human_readable(comp_size):>12} "
                f"{ratio:7.2f}%\n"
            )

    print(f"\nAll done. Results logged to {log_path}")

if __name__ == "__main__":
    main()
