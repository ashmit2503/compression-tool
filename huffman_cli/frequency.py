"""
Build a frequency table from input bytes.
"""
def build_frequency_table(data: bytes) -> dict[int, int]:
    freq: dict[int, int] = {}
    for b in data:
        freq[b] = freq.get(b, 0) + 1
    return freq

