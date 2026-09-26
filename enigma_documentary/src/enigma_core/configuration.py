"""Machine settings: exactly what an operator read off the daily key sheet."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path

import yaml

from .alphabet import idx
from .wiring import REFLECTORS, ROTORS


def _letter_or_number(v) -> int:
    """Accept ring/position as 'B', 2 (1-based, as on key sheets) or '02'."""
    if isinstance(v, int):
        if not 1 <= v <= 26:
            raise ValueError(f"ring/position number must be 1..26, got {v}")
        return v - 1
    s = str(v).strip().upper()
    if s.isdigit():
        return _letter_or_number(int(s))
    return idx(s)


@dataclass
class MachineConfig:
    """Rotor order is written left-to-right, as on a key sheet (e.g. II IV V)."""
    rotors: list[str] = field(default_factory=lambda: ["I", "II", "III"])
    reflector: str = "B"
    rings: list[int] = field(default_factory=lambda: [0, 0, 0])      # 0-based
    positions: list[int] = field(default_factory=lambda: [0, 0, 0])  # 0-based
    plugboard: list[tuple[str, str]] = field(default_factory=list)
    variant: str = "Enigma I"
    name: str = ""
    note: str = ""

    def __post_init__(self):
        if len(self.rotors) != 3 or len(self.rings) != 3 or len(self.positions) != 3:
            raise ValueError("Enigma I uses exactly three rotors")
        if len(set(self.rotors)) != 3:
            raise ValueError("a rotor cannot be used twice")
        for r in self.rotors:
            if r not in ROTORS:
                raise ValueError(f"unknown rotor {r}")
            if self.variant not in ROTORS[r]["variants"]:
                raise ValueError(f"rotor {r} did not exist on {self.variant}")
        if self.reflector not in REFLECTORS or self.variant not in REFLECTORS[self.reflector]["variants"]:
            raise ValueError(f"reflector {self.reflector} not valid for {self.variant}")
        self.plugboard = [(a.upper(), b.upper()) for a, b in self.plugboard]

    @classmethod
    def from_dict(cls, d: dict, name: str = "") -> "MachineConfig":
        def trip(v):
            if isinstance(v, str):
                v = v.split() if " " in v.strip() else list(v.strip())
            return [_letter_or_number(x) for x in v]
        plug = d.get("plugboard") or []
        if isinstance(plug, str):
            plug = plug.split()
        plug = [(p[0], p[1]) if isinstance(p, str) else tuple(p) for p in plug]
        rotors = d.get("rotors", ["I", "II", "III"])
        if isinstance(rotors, str):
            rotors = rotors.split()
        return cls(rotors=list(rotors), reflector=str(d.get("reflector", "B")),
                   rings=trip(d.get("rings", "AAA")), positions=trip(d.get("positions", "AAA")),
                   plugboard=plug, variant=d.get("variant", "Enigma I"),
                   name=name or d.get("name", ""), note=d.get("note", ""))

    def to_dict(self) -> dict:
        d = asdict(self)
        d["rings"] = "".join(chr(65 + r) for r in self.rings)
        d["positions"] = "".join(chr(65 + p) for p in self.positions)
        d["plugboard"] = " ".join(a + b for a, b in self.plugboard)
        return d


def load_configs(path: str | Path) -> dict[str, MachineConfig]:
    data = yaml.safe_load(Path(path).read_text())
    return {k: MachineConfig.from_dict(v, name=k) for k, v in data["machines"].items()}
