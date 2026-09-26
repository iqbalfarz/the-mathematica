"""A rotor: a scrambled bundle of 26 wires inside a wheel that can turn.

Two frames of reference matter for the animation:

* **fixed frame** ("pos"): the 26 contacts of the machine body, labelled A..Z.
  The wires in Blender run between fixed-frame contacts of neighbouring parts.
* **core frame** ("pin"): the 26 contacts on the rotor's own wiring core. They
  turn with the rotor.

With window letter p and ring setting r the core is turned by shift = p - r, so
a current arriving at fixed contact c meets core pin (c + shift).
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .alphabet import N, ch, idx
from .wiring import ROTORS


@dataclass
class Rotor:
    name: str
    wiring: str
    notches: str
    ring: int = 0          # Ringstellung, 0 = A (or 01)
    position: int = 0      # letter visible in the window, 0 = A
    _fwd: list[int] = field(init=False, repr=False)
    _bwd: list[int] = field(init=False, repr=False)

    def __post_init__(self):
        if sorted(self.wiring) != sorted("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            raise ValueError(f"rotor {self.name}: wiring is not a permutation")
        self._fwd = [idx(c) for c in self.wiring]
        self._bwd = [0] * N
        for i, o in enumerate(self._fwd):
            self._bwd[o] = i

    @classmethod
    def from_name(cls, name: str, ring: int = 0, position: int = 0) -> "Rotor":
        spec = ROTORS[name]
        return cls(name=name, wiring=spec["wiring"], notches=spec["notches"], ring=ring, position=position)

    @property
    def shift(self) -> int:
        return (self.position - self.ring) % N

    @property
    def window(self) -> str:
        return ch(self.position)

    def at_notch(self) -> bool:
        return self.window in self.notches

    def step(self) -> None:
        self.position = (self.position + 1) % N

    # Each pass returns (out_pos, in_pin, out_pin) so animation can draw the exact wire.
    def forward(self, pos: int) -> tuple[int, int, int]:
        pin = (pos + self.shift) % N
        out_pin = self._fwd[pin]
        return (out_pin - self.shift) % N, pin, out_pin

    def backward(self, pos: int) -> tuple[int, int, int]:
        pin = (pos + self.shift) % N
        out_pin = self._bwd[pin]
        return (out_pin - self.shift) % N, pin, out_pin
