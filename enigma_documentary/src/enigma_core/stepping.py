"""The stepping mechanism of a 3-rotor Enigma I.

Physically there are three pawls, one per rotor, all pushed forward by every key
press. A pawl can only move a rotor if it drops into a slot:

* pawl 1 (right) always engages the right rotor's ratchet -> right rotor steps.
* pawl 2 (middle) rides on the right rotor's notch ring. When the right rotor
  shows its notch letter, pawl 2 drops in and pushes the middle rotor.
* pawl 3 (left) rides on the middle rotor's notch ring. When the middle rotor
  shows its notch letter, pawl 3 drops in and pushes the left rotor. Because a
  pawl pushes the *notch* as well as the ratchet in front of it, pawl 3 also
  drags the middle rotor forward: the famous double step.

Stepping happens *before* the current flows (the key must be pressed down far
enough to step the rotors before the contact under it closes).
"""
from __future__ import annotations

from dataclasses import asdict, dataclass

from .rotor import Rotor


@dataclass
class StepEvent:
    pawl: int            # 1 = right, 2 = middle, 3 = left
    rotor: str           # "right" | "middle" | "left"
    reason: str          # "every_keypress" | "right_notch" | "middle_notch" | "double_step"
    from_letter: str
    to_letter: str

    def to_dict(self) -> dict:
        return asdict(self)


def step(left: Rotor, middle: Rotor, right: Rotor) -> list[StepEvent]:
    """Advance the rotors for one key press and describe which pawls did what."""
    events: list[StepEvent] = []
    right_notch = right.at_notch()
    middle_notch = middle.at_notch()
    moves: list[tuple[int, Rotor, str, str]] = []
    if middle_notch:
        moves.append((3, left, "left", "middle_notch"))
        moves.append((3, middle, "middle", "double_step"))
    elif right_notch:
        moves.append((2, middle, "middle", "right_notch"))
    moves.append((1, right, "right", "every_keypress"))
    # When both notches line up, pawl 2 also pushes the middle rotor, but it is
    # the same single step pawl 3 is already making, so the middle moves once.
    for pawl, rotor, which, reason in moves:
        before = rotor.window
        rotor.step()
        events.append(StepEvent(pawl, which, reason, before, rotor.window))
    return events
