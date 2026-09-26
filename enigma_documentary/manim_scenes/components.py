"""Reusable Manim pieces for the cipher chapters."""
from __future__ import annotations

import numpy as np
from manim import (DOWN, LEFT, ORIGIN, RIGHT, UP, Arrow, Circle, Dot, Line, RoundedRectangle, Text, VGroup,
                   config)

from manim_scenes import style as S

ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def letter(ch, size=S.BODY, color=S.PAPER, mono=True):
    return Text(ch, font=S.MONO if mono else S.SANS, font_size=size, color=color)


def alphabet_row(letters=ALPHA, size=26, cell=0.46, color=S.PAPER):
    """A row of letters on a fixed grid (so cells line up between rows)."""
    row = VGroup(*[letter(c, size, color) for c in letters])
    for i, m in enumerate(row):
        m.move_to(RIGHT * (i - (len(letters) - 1) / 2) * cell)
    row.cell = cell
    return row


def cell_x(row, i):
    return (i - (len(row) - 1) / 2) * row.cell


def caption(text, size=S.SMALL, color=S.MUTED):
    return Text(text, font=S.SANS, font_size=size, color=color)


def label_illustrative():
    return caption("illustrative", S.LABEL).to_corner(DOWN + RIGHT, buff=0.35)


class Wheel(VGroup):
    """A flat 'rotor': fixed letters round the rim, a rotating bundle of 26 chords.

    Chord for core pin j runs from rim angle of j to rim angle of wiring[j].
    Letter k sits at angle 90deg - k*360/26 (clockwise from the top). Turning the
    rotor by p steps rotates the chords (not the letters) by +p*step, which puts
    core pin (c+p) under fixed letter c -- exactly enigma_core.rotor with ring A.
    """

    def __init__(self, wiring: str, radius=2.6, **kw):
        super().__init__(**kw)
        self.wiring = wiring
        self.radius = radius
        self.step = 2 * np.pi / 26
        self.rim = Circle(radius=radius, color=S.BRASS, stroke_width=3)
        self.labels = VGroup(*[letter(ALPHA[k], 22, S.PAPER).move_to(self.point(k, radius + 0.32))
                               for k in range(26)])
        self.contacts = VGroup(*[Dot(self.point(k, radius), radius=0.045, color=S.BRASS) for k in range(26)])
        self.chords = VGroup(*[self._chord(j, S.MUTED, 1.4, 0.55) for j in range(26)])
        self.position = 0
        self.add(self.rim, self.chords, self.contacts, self.labels)

    def angle(self, k):
        return np.pi / 2 - k * self.step

    def point(self, k, r=None):
        r = self.radius if r is None else r
        a = self.angle(k)
        return self.get_center_if_built() + r * np.array([np.cos(a), np.sin(a), 0])

    def get_center_if_built(self):
        return self.rim.get_center() if hasattr(self, "rim") else ORIGIN

    def _chord(self, j, color, width, opacity):
        o = ALPHA.index(self.wiring[j])
        return Line(self.point(j), self.point(o), color=color, stroke_width=width, stroke_opacity=opacity)

    def out_letter(self, key: str) -> str:
        """Which fixed letter a current entering at `key` leaves from, at the current position."""
        c = ALPHA.index(key)
        pin = (c + self.position) % 26
        return ALPHA[(ALPHA.index(self.wiring[pin]) - self.position) % 26]

    def path(self, key: str, color=S.SIGNAL):
        out = self.out_letter(key)
        return Line(self.point(ALPHA.index(key)), self.point(ALPHA.index(out)), color=color, stroke_width=6), out


def rotor_silhouette(width=0.9, height=2.6):
    """Side view of a rotor: body plus serrated thumbwheel edge."""
    body = RoundedRectangle(width=width, height=height, corner_radius=0.12, color=S.BRASS, fill_color="#1B1812",
                            fill_opacity=1, stroke_width=3)
    teeth = VGroup(*[Line(LEFT * 0.12, RIGHT * 0.12, color=S.BRASS, stroke_width=2)
                     .move_to(body.get_left() + UP * (height / 2 - 0.1 - i * (height - 0.2) / 17) + LEFT * 0.08)
                     for i in range(18)])
    return VGroup(body, teeth)


def arrow_down(a, b, color=S.MUTED):
    return Arrow(a.get_bottom(), b.get_top(), buff=0.08, color=color, stroke_width=3,
                 max_tip_length_to_length_ratio=0.25)
