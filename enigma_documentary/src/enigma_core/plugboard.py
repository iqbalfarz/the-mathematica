"""The plugboard (Steckerbrett): cables that swap pairs of letters, both ways."""
from __future__ import annotations

from dataclasses import dataclass, field

from .alphabet import N, ch, idx


@dataclass
class Plugboard:
    pairs: list[tuple[str, str]] = field(default_factory=list)
    _map: list[int] = field(init=False, repr=False)

    def __post_init__(self):
        self._map = list(range(N))
        seen: set[str] = set()
        norm: list[tuple[str, str]] = []
        for a, b in self.pairs:
            a, b = a.upper(), b.upper()
            if a == b:
                raise ValueError(f"plugboard cable joins {a} to itself")
            for x in (a, b):
                if x in seen:
                    raise ValueError(f"plugboard letter {x} used twice")
                seen.add(x)
            self._map[idx(a)], self._map[idx(b)] = idx(b), idx(a)
            norm.append((a, b))
        if len(norm) > 13:
            raise ValueError("at most 13 cables fit on 26 sockets")
        self.pairs = norm

    @classmethod
    def parse(cls, spec: str | list | None) -> "Plugboard":
        if not spec:
            return cls([])
        if isinstance(spec, str):
            spec = spec.split()
        return cls([(p[0], p[1]) if isinstance(p, str) else tuple(p) for p in spec])

    def swap(self, pos: int) -> int:
        return self._map[pos]

    def spec(self) -> str:
        return " ".join(a + b for a, b in self.pairs)

    def partner(self, letter: str) -> str:
        return ch(self._map[idx(letter)])
