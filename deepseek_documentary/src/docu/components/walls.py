from __future__ import annotations

from manim import (DOWN, LEFT, RIGHT, UP, RoundedRectangle, VGroup)

from .. import style as S
from .typography import T, safe_bottom, safe_left

__all__ = ["Pillar", "WallsLegend", "WALLS"]

WALLS = [("COMPUTE", S.COMPUTE), ("MEMORY", S.MEMORY), ("COMMUNICATION", S.COMM)]


class Pillar(VGroup):
    def __init__(self, name, color, w=2.3, h=3.2, label_size=S.SMALL, **kw):
        super().__init__(**kw)
        self.col = RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color=color, stroke_width=2.5,
                                    fill_color=color, fill_opacity=0.18)
        self.t = T(name, label_size, color, weight="BOLD")
        if self.t.width > w * 1.25:
            self.t.scale_to_fit_width(w * 1.25)
        self.t.next_to(self.col, DOWN, buff=0.15)
        self.add(self.col, self.t)
        self.color = color


class WallsLegend(VGroup):
    """The three walls, small, bottom-left. Recreated identically in every scene that shows it."""

    def __init__(self, **kw):
        super().__init__(**kw)
        self.items = VGroup()
        for name, color in WALLS:
            sw = RoundedRectangle(corner_radius=0.03, width=0.16, height=0.3, stroke_width=0, fill_color=color,
                                  fill_opacity=0.9)
            self.items.add(VGroup(sw, T(name, S.TINY, color, weight="BOLD")).arrange(RIGHT, buff=0.1))
        self.items.arrange(RIGHT, buff=0.3)
        self.add(self.items)
        self.move_to([safe_left() + self.width / 2, safe_bottom() + self.height / 2, 0])

    def item(self, name):
        return self.items[[w for w, _ in WALLS].index(name)]
