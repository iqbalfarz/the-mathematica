"""Cribs: guessed plaintext slid under ciphertext.

Because the reflector never wires a contact to itself, Enigma can never encrypt
a letter to itself. Any alignment where a crib letter sits above the same
ciphertext letter is impossible.
"""
from __future__ import annotations

from dataclasses import dataclass

from .alphabet import clean


@dataclass
class Alignment:
    offset: int
    clashes: list[int]      # indices into the crib where crib[i] == cipher[offset+i]

    @property
    def possible(self) -> bool:
        return not self.clashes


def alignments(ciphertext: str, crib: str) -> list[Alignment]:
    c, p = clean(ciphertext), clean(crib)
    out = []
    for off in range(len(c) - len(p) + 1):
        out.append(Alignment(off, [i for i, x in enumerate(p) if c[off + i] == x]))
    return out


def possible_offsets(ciphertext: str, crib: str) -> list[int]:
    return [a.offset for a in alignments(ciphertext, crib) if a.possible]
