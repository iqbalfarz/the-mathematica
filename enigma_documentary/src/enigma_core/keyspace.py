"""How many ways can the machine be set up? Exact integers, named factors.

Every factor carries a ledger id (research/claim_ledger.csv) so on-screen
numbers can be traced. Figures are only valid for the variant named.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import comb, factorial, perm


def plugboard_settings(cables: int, letters: int = 26) -> int:
    """Ways to plug `cables` cables into `letters` sockets (pairs are unordered).

    Choose 2n letters, then pair them up: letters! / ((letters-2n)! * n! * 2^n).
    """
    if not 0 <= 2 * cables <= letters:
        raise ValueError("too many cables")
    return factorial(letters) // (factorial(letters - 2 * cables) * factorial(cables) * 2 ** cables)


@dataclass(frozen=True)
class Factor:
    name: str
    value: int
    formula: str
    ledger: str


def enigma_i_factors(rotors_in_box: int = 5, cables: int = 10, include_rings: bool = False) -> list[Factor]:
    """Enigma I, 3 rotors in the machine chosen from `rotors_in_box`, reflector B fixed."""
    f = [
        Factor("rotor order", perm(rotors_in_box, 3), f"{rotors_in_box}×{rotors_in_box-1}×{rotors_in_box-2}", "KEY-ORDER"),
        Factor("starting positions", 26 ** 3, "26×26×26", "KEY-POS"),
    ]
    if include_rings:
        # Only the middle and right rings change the stepping; the left ring is
        # indistinguishable from a different left starting position.
        f.append(Factor("ring settings (effective)", 26 ** 2, "26×26", "KEY-RINGS"))
    f.append(Factor(f"plugboard ({cables} cables)", plugboard_settings(cables), "26!/(6!·10!·2¹⁰)" if cables == 10 else f"n={cables}", "KEY-PLUG"))
    return f


def total(factors: list[Factor]) -> int:
    out = 1
    for x in factors:
        out *= x.value
    return out


def commercial_factors() -> list[Factor]:
    """Commercial Enigma (no plugboard): 3 fixed rotors in any order, 26³ positions."""
    return [Factor("rotor order", factorial(3), "3×2×1", "KEY-COMM-ORDER"),
            Factor("starting positions", 26 ** 3, "26×26×26", "KEY-POS")]


def rotor_wirings(contacts: int = 26) -> int:
    """How many different ways one rotor could be wired: every wiring is a
    permutation of the alphabet, so 26! (ledger KEY-WIRINGS)."""
    return factorial(contacts)


def fmt(n: int) -> str:
    return f"{n:,}"


def summary() -> dict[str, int]:
    return {
        "commercial": total(commercial_factors()),
        "enigma_i_5rotors_10cables": total(enigma_i_factors()),
        "enigma_i_5rotors_10cables_rings": total(enigma_i_factors(include_rings=True)),
        "plugboard_10": plugboard_settings(10),
        "plugboard_6": plugboard_settings(6),
        "plugboard_max": max(plugboard_settings(n) for n in range(14)),
        "plugboard_argmax": max(range(14), key=plugboard_settings),
        "pairs_of_letters": comb(26, 2),
        "rotor_wirings": rotor_wirings(),
    }
