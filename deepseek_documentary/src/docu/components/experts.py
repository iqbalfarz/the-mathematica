from __future__ import annotations

from manim import (DOWN, LEFT, RIGHT, UP, Polygon, RoundedRectangle, Square, VGroup)

from .. import style as S
from .typography import T

__all__ = ["Expert", "ExpertGrid", "Router", "SharedExpert"]


class Expert(VGroup):
    def __init__(self, label: str | None = None, w=0.8, h=0.8, **kw):
        super().__init__(**kw)
        self.box = RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=S.EXPERT, stroke_width=2,
                                    fill_color=S.EXPERT, fill_opacity=0.08)
        self.add(self.box)
        if label:
            t = T(label, S.SMALL, S.TEXT)
            if t.width > w * 0.85:
                t.scale_to_fit_width(w * 0.85)
            self.add(t.move_to(self.box))

    def on(self, opacity=0.75):
        return self.box.animate.set_fill(S.EXPERT, opacity=opacity).set_stroke(width=3)

    def off(self):
        return self.box.animate.set_fill(S.EXPERT, opacity=0.08).set_stroke(width=2)


class ExpertGrid(VGroup):
    """Many small experts (DeepSeekMoE style fine-grained experts)."""

    def __init__(self, n=64, cols=16, size=0.22, gap=0.06, **kw):
        super().__init__(**kw)
        self.cells = VGroup(*[Square(size, stroke_color=S.EXPERT, stroke_width=0.8, fill_color=S.EXPERT,
                                     fill_opacity=0.08) for _ in range(n)])
        self.cells.arrange_in_grid(rows=(n + cols - 1) // cols, cols=cols, buff=gap)
        self.add(self.cells)


class SharedExpert(VGroup):
    def __init__(self, w=0.9, h=2.0, **kw):
        super().__init__(**kw)
        self.box = RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color=S.EXPERT, stroke_width=3,
                                    fill_color=S.EXPERT, fill_opacity=0.35)
        self.t = T("shared", S.TINY, S.TEXT, weight="BOLD").rotate(1.5708).move_to(self.box)
        self.add(self.box, self.t)


class Router(VGroup):
    def __init__(self, r=0.42, **kw):
        super().__init__(**kw)
        self.diamond = Polygon([0, r, 0], [r, 0, 0], [0, -r, 0], [-r, 0, 0], color=S.ROUTER, stroke_width=2.5,
                               fill_color=S.ROUTER, fill_opacity=0.12)
        self.t = T("router", S.TINY, S.ROUTER).next_to(self.diamond, DOWN, buff=0.1)
        self.add(self.diamond, self.t)
