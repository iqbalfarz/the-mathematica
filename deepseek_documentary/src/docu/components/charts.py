from __future__ import annotations

import math

from manim import (DOWN, LEFT, RIGHT, UP, Line, Rectangle, RoundedRectangle, VGroup, Axes)

from .. import style as S
from .typography import T

__all__ = ["HBarChart", "prob_bars", "bar_pair"]


class HBarChart(VGroup):
    """Horizontal bars with name + value labels. `log=True` uses log10 lengths
    (always labelled on screen, never silently)."""

    def __init__(self, items, max_len=7.0, bar_h=0.42, gap=0.42, color=S.MEMORY, log=False,
                 name_size=S.SMALL, value_size=S.SMALL, highlight=None, **kw):
        super().__init__(**kw)
        vals = [v for _, v, *_ in items]
        if log:
            lo = 0.0
            hi = math.log10(max(vals))
            L = lambda v: max(0.06, max_len * (math.log10(v) - lo) / (hi - lo))
        else:
            L = lambda v: max(0.04, max_len * v / max(vals))
        self.rows = VGroup()
        self.bars = VGroup()
        self.names = VGroup()
        self.values = VGroup()
        for k, (name, v, *rest) in enumerate(items):
            sub = rest[0] if rest else None
            col = S.TOKEN if highlight is not None and k == highlight else color
            name_g = VGroup(T(name, name_size, S.TEXT, weight="BOLD"))
            if sub:
                name_g.add(T(sub, S.TINY, S.MUTED))
            name_g.arrange(DOWN, aligned_edge=RIGHT, buff=0.06)
            bar = Rectangle(width=L(v), height=bar_h, stroke_width=0, fill_color=col, fill_opacity=0.85)
            self.names.add(name_g)
            self.bars.add(bar)
            self.values.add(T(f"{v:,}", value_size, S.TEXT, mono=True))
        name_w = max(n.width for n in self.names)
        for k in range(len(items)):
            y = -k * (bar_h + gap)
            self.names[k].move_to([-name_w / 2 - 0.25, y, 0], aligned_edge=RIGHT).shift(RIGHT * (name_w / 2))
            self.names[k].align_to([-0.25, 0, 0], RIGHT)
            self.bars[k].move_to([0, y, 0], aligned_edge=LEFT).align_to([0, 0, 0], LEFT)
            self.values[k].next_to(self.bars[k], RIGHT, buff=0.15)
            self.rows.add(VGroup(self.names[k], self.bars[k], self.values[k]))
        self.axis = Line([0, 0.4, 0], [0, -(len(items) - 1) * (bar_h + gap) - 0.4, 0], color=S.MUTED,
                         stroke_width=1.5)
        self.add(self.axis, self.rows)
        self.move_to([0, 0, 0])


def prob_bars(labels, probs, color=S.TOKEN, max_h=2.2, w=0.6, label_size=S.SMALL, show_values=True):
    g = VGroup()
    for lab, p in zip(labels, probs):
        bar = Rectangle(width=w, height=max(0.02, max_h * p), stroke_width=0, fill_color=color, fill_opacity=0.8)
        name = T(lab, label_size, S.TEXT)
        col = VGroup(bar, name).arrange(DOWN, buff=0.12)
        if show_values:
            val = T(f"{p:.2f}", S.TINY, S.MUTED, mono=True).next_to(bar, UP, buff=0.08)
            col.add(val)
        g.add(col)
    g.arrange(RIGHT, buff=0.3, aligned_edge=DOWN)
    return g


def bar_pair(a_label, a_val, b_label, b_val, color_a=S.MUTED, color_b=S.MEMORY, max_len=8.0, bar_h=0.5):
    top = max(a_val, b_val)
    ra = Rectangle(width=max(0.03, max_len * a_val / top), height=bar_h, stroke_width=0, fill_color=color_a,
                   fill_opacity=0.85)
    rb = Rectangle(width=max(0.03, max_len * b_val / top), height=bar_h, stroke_width=0, fill_color=color_b,
                   fill_opacity=0.85)
    la = T(a_label, S.SMALL, S.TEXT)
    lb = T(b_label, S.SMALL, S.TEXT)
    g = VGroup(VGroup(ra, la), VGroup(rb, lb))
    for bar, lab in ((ra, la), (rb, lb)):
        lab.next_to(bar, UP, buff=0.1, aligned_edge=LEFT)
    g.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
    return g
