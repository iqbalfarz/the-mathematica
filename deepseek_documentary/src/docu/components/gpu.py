from __future__ import annotations

from manim import (DOWN, LEFT, RIGHT, UP, Line, Rectangle, RoundedRectangle, Square, VGroup, Circle)

from .. import style as S
from .typography import T

__all__ = ["GPU", "gpu_wall", "MemoryBank", "Pipe", "CPUChip"]


class GPU(VGroup):
    """GPU icon: rounded die with a grid of tiny cores and an optional label.
    Used identically from Act 1 (the wall) to Act 7 (the islands)."""

    def __init__(self, label: str | None = None, w: float = 1.6, h: float = 1.1, cores=(6, 9),
                 color=S.COMPUTE, core_opacity=0.35, label_size=S.SMALL, **kw):
        super().__init__(**kw)
        self.die = RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=color, stroke_width=2,
                                    fill_color=S.PANEL, fill_opacity=1)
        r, c = cores
        pad = 0.12
        cs = min((w - 2 * pad) / c, (h - 2 * pad) / r) * 0.78
        self.cores = VGroup()
        for i in range(r):
            for j in range(c):
                self.cores.add(Square(cs, stroke_width=0, fill_color=color, fill_opacity=core_opacity))
        self.cores.arrange_in_grid(r, c, buff=cs * 0.28).move_to(self.die)
        self.add(self.die, self.cores)
        self.label = None
        if label:
            self.label = T(label, label_size, S.TEXT, weight="BOLD")
            if self.label.width > w * 1.3:
                self.label.scale_to_fit_width(w * 1.3)
            self.label.next_to(self.die, DOWN, buff=0.12)
            self.add(self.label)


def gpu_wall(rows: int, cols: int, unit: float = 0.34, color=S.COMPUTE, opacity=0.5) -> VGroup:
    """A field of tiny GPU tiles for 'scale' shots (cheap to render)."""
    g = VGroup()
    for i in range(rows):
        for j in range(cols):
            g.add(RoundedRectangle(corner_radius=unit * 0.12, width=unit, height=unit * 0.7,
                                   stroke_color=color, stroke_width=0.8, fill_color=color, fill_opacity=opacity * 0.3))
    g.arrange_in_grid(rows, cols, buff=unit * 0.18)
    return g


class MemoryBank(VGroup):
    def __init__(self, label="HBM", w=1.4, h=2.6, rows=8, color=S.MEMORY, **kw):
        super().__init__(**kw)
        self.box = RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=color, stroke_width=2,
                                    fill_color=S.PANEL, fill_opacity=1)
        self.rows = VGroup(*[Rectangle(width=w * 0.72, height=h / rows * 0.55, stroke_width=0,
                                       fill_color=color, fill_opacity=0.35) for _ in range(rows)])
        self.rows.arrange(DOWN, buff=h / rows * 0.4).move_to(self.box)
        self.label = T(label, S.SMALL, S.TEXT, weight="BOLD").next_to(self.box, DOWN, buff=0.12)
        self.add(self.box, self.rows, self.label)


class Pipe(VGroup):
    """A horizontal pipe whose thickness encodes bandwidth."""

    def __init__(self, start, end, width=0.35, color=S.COMM, **kw):
        super().__init__(**kw)
        self.start, self.end = start, end
        self.body = Line(start, end, stroke_width=width * 110, color=color, stroke_opacity=0.35)
        self.core = Line(start, end, stroke_width=2, color=color)
        self.add(self.body, self.core)

    def set_bandwidth(self, width):
        return self.body.animate.set_stroke(width=width * 110)


class CPUChip(VGroup):
    def __init__(self, n_cores=8, w=1.9, h=1.9, color=S.GRAD, **kw):
        super().__init__(**kw)
        self.die = RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color=color, stroke_width=2,
                                    fill_color=S.PANEL, fill_opacity=1)
        cs = w * 0.36
        self.cores = VGroup(*[RoundedRectangle(corner_radius=0.05, width=cs, height=cs * 0.8, stroke_width=0,
                                               fill_color=color, fill_opacity=0.45) for _ in range(n_cores)])
        cols = 2 if n_cores <= 4 else 4
        self.cores.arrange_in_grid(rows=(n_cores + cols - 1) // cols, cols=cols, buff=0.08)
        self.cores.scale_to_fit_width(w * 0.8).move_to(self.die)
        self.add(self.die, self.cores)


class ChipCard(VGroup):
    """A named chip (A100, H800...) with an optional status bar underneath."""

    def __init__(self, name: str, sub: str | None = None, w=1.45, h=0.9, color=S.COMPUTE, **kw):
        super().__init__(**kw)
        self.box = RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=color, stroke_width=2,
                                    fill_color=S.PANEL, fill_opacity=1)
        self.name = T(name, S.BODY, S.TEXT, weight="BOLD")
        g = VGroup(self.name)
        if sub:
            g.add(T(sub, S.TINY, S.MUTED))
        g.arrange(DOWN, buff=0.06).move_to(self.box)
        if g.width > w * 0.9:
            g.scale_to_fit_width(w * 0.9)
        self.add(self.box, g)

    def status(self, text: str, color=S.LOSS):
        from .typography import chip
        c = chip(text, color, fill_opacity=0.25)
        if c.width > self.box.width * 1.05:
            c.scale_to_fit_width(self.box.width * 1.05)
        c.next_to(self.box, DOWN, buff=0.08)
        return c


__all__.append("ChipCard")
