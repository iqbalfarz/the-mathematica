"""EnigmaMachine: wires the parts together and records what happened."""
from __future__ import annotations

import copy

from .alphabet import ch, clean, idx
from .configuration import MachineConfig
from .events import Hop, KeyPress
from .plugboard import Plugboard
from .reflector import Reflector
from .rotor import Rotor
from .stepping import step


class EnigmaMachine:
    def __init__(self, config: MachineConfig | None = None):
        self.config = copy.deepcopy(config or MachineConfig())
        c = self.config
        self.left, self.middle, self.right = (
            Rotor.from_name(n, ring=r, position=p) for n, r, p in zip(c.rotors, c.rings, c.positions))
        self.reflector = Reflector.from_name(c.reflector)
        self.plugboard = Plugboard(list(c.plugboard))
        self.count = 0

    # ------------------------------------------------------------------ state
    @property
    def positions(self) -> str:
        return self.left.window + self.middle.window + self.right.window

    def set_positions(self, letters: str) -> None:
        for r, l in zip((self.left, self.middle, self.right), letters):
            r.position = idx(l)

    def reset(self) -> None:
        self.__init__(self.config)

    # ------------------------------------------------------------------ core
    def _rotor_hop(self, stage: str, rotor: Rotor, pos: int, forward: bool) -> tuple[int, Hop]:
        out, pin, out_pin = (rotor.forward if forward else rotor.backward)(pos)
        # Name core pins by the ring-alphabet letter engraved next to them.
        return out, Hop(stage, ch(pos), ch(out), ch(pin + rotor.ring), ch(out_pin + rotor.ring), rotor.name)

    def press_key(self, letter: str) -> KeyPress:
        key = idx(letter)
        before = self.positions
        steps = step(self.left, self.middle, self.right)
        path: list[Hop] = [Hop("keyboard", ch(key), ch(key))]

        s = self.plugboard.swap(key)
        path.append(Hop("plugboard_in", ch(key), ch(s)))
        path.append(Hop("entry_in", ch(s), ch(s)))  # Enigma I entry wheel is the identity
        for stage, rotor in (("rotor_right_in", self.right), ("rotor_middle_in", self.middle),
                             ("rotor_left_in", self.left)):
            s2, hop = self._rotor_hop(stage, rotor, s, True)
            path.append(hop)
            s = s2
        r = self.reflector.reflect(s)
        path.append(Hop("reflector", ch(s), ch(r)))
        s = r
        for stage, rotor in (("rotor_left_out", self.left), ("rotor_middle_out", self.middle),
                             ("rotor_right_out", self.right)):
            s2, hop = self._rotor_hop(stage, rotor, s, False)
            path.append(hop)
            s = s2
        path.append(Hop("entry_out", ch(s), ch(s)))
        out = self.plugboard.swap(s)
        path.append(Hop("plugboard_out", ch(s), ch(out)))
        path.append(Hop("lamp", ch(out), ch(out)))

        kp = KeyPress(self.count, ch(key), ch(out), before, self.positions, steps, path)
        self.count += 1
        return kp

    def press_keys(self, text: str) -> list[KeyPress]:
        return [self.press_key(c) for c in clean(text)]

    def encrypt(self, text: str) -> str:
        return "".join(p.lamp for p in self.press_keys(text))
