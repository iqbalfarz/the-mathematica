from __future__ import annotations

from manim import (DOWN, LEFT, RIGHT, UP, RoundedRectangle, VGroup)

from .. import style as S
from .typography import T

__all__ = ["KVSlot", "KVShelf"]


class KVSlot(VGroup):
    """One cached entry: a K half and a V half."""

    def __init__(self, w=0.34, h=0.5, **kw):
        super().__init__(**kw)
        k = RoundedRectangle(corner_radius=0.04, width=w, height=h / 2 - 0.02, stroke_width=0,
                             fill_color=S.KCOL, fill_opacity=0.8)
        v = RoundedRectangle(corner_radius=0.04, width=w, height=h / 2 - 0.02, stroke_width=0,
                             fill_color=S.VCOL, fill_opacity=0.8)
        VGroup(k, v).arrange(DOWN, buff=0.04)
        self.k, self.v = k, v
        self.add(k, v)


class KVShelf(VGroup):
    def __init__(self, n=8, slot_w=0.34, slot_h=0.5, gap=0.08, label=True, **kw):
        super().__init__(**kw)
        self.slots = VGroup(*[KVSlot(slot_w, slot_h) for _ in range(n)]).arrange(RIGHT, buff=gap)
        self.base = RoundedRectangle(corner_radius=0.05, width=self.slots.width + 0.3, height=0.08, stroke_width=0,
                                     fill_color=S.MEMORY, fill_opacity=0.9).next_to(self.slots, DOWN, buff=0.06)
        self.add(self.slots, self.base)
        if label:
            self.label = T("KV cache", S.SMALL, S.MEMORY, weight="BOLD").next_to(self.base, DOWN, buff=0.14)
            self.add(self.label)
