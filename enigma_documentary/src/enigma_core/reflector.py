"""The reflector (Umkehrwalze): pairs the 26 contacts, sending current back."""
from __future__ import annotations

from dataclasses import dataclass, field

from .alphabet import N, idx
from .wiring import REFLECTORS


@dataclass
class Reflector:
    name: str
    wiring: str
    _map: list[int] = field(init=False, repr=False)

    def __post_init__(self):
        self._map = [idx(c) for c in self.wiring]
        for i, o in enumerate(self._map):
            if o == i:
                raise ValueError(f"reflector {self.name}: contact {i} wired to itself")
            if self._map[o] != i:
                raise ValueError(f"reflector {self.name}: not reciprocal at {i}")

    @classmethod
    def from_name(cls, name: str) -> "Reflector":
        return cls(name=name, wiring=REFLECTORS[name]["wiring"])

    def reflect(self, pos: int) -> int:
        return self._map[pos]

    def pairs(self) -> list[tuple[int, int]]:
        return [(i, o) for i, o in enumerate(self._map) if i < o]

    def __len__(self) -> int:  # pragma: no cover - convenience
        return N
