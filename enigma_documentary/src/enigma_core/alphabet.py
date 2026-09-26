"""Letters <-> indices. Everything inside the simulator works on 0..25."""
from __future__ import annotations

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
N = 26


def idx(letter: str) -> int:
    letter = letter.upper()
    if len(letter) != 1 or letter not in ALPHABET:
        raise ValueError(f"not a letter A-Z: {letter!r}")
    return ALPHABET.index(letter)


def ch(i: int) -> str:
    return ALPHABET[i % N]


def clean(text: str) -> str:
    """Keep only A-Z (upper-cased), as an operator would type it."""
    return "".join(c for c in text.upper() if c in ALPHABET)
