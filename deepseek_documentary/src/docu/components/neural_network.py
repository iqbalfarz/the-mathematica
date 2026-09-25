from __future__ import annotations

from manim import (DOWN, LEFT, RIGHT, UP, Arrow, Circle, Line, RoundedRectangle, VGroup)

from .. import style as S
from .typography import T

__all__ = ["Neuron", "LayerTower", "Block"]


class Neuron(VGroup):
    """Inputs -> weighted edges -> a summing neuron."""

    def __init__(self, inputs=("3", "1", "2"), weights=("4", "-2", "5"), spacing=1.1, **kw):
        super().__init__(**kw)
        self.inputs = VGroup(*[T(x, S.BODY, S.TOKEN, mono=True) for x in inputs]).arrange(DOWN, buff=spacing - 0.4)
        self.inputs.shift(LEFT * 3)
        self.node = Circle(0.45, color=S.TEXT, stroke_width=2.5).shift(RIGHT * 0.5)
        self.edges = VGroup()
        self.wlabels = VGroup()
        for inp, w in zip(self.inputs, weights):
            e = Line(inp.get_right() + RIGHT * 0.15, self.node.get_left(), color=S.PARAM, stroke_width=3)
            self.edges.add(e)
            wl = T(w, S.SMALL, S.PARAM, mono=True)
            wl.move_to(e.point_from_proportion(0.45) + UP * 0.28)
            self.wlabels.add(wl)
        self.sigma = T("Σ", S.BODY, S.TEXT).move_to(self.node)
        self.out = Arrow(self.node.get_right(), self.node.get_right() + RIGHT * 1.4, color=S.TEXT, buff=0.05,
                         stroke_width=3)
        self.add(self.inputs, self.edges, self.wlabels, self.node, self.sigma, self.out)
        self.move_to([0, 0, 0])


class Block(VGroup):
    """One Transformer block: [Attention] over [Feed-forward]."""

    def __init__(self, w=3.0, h=0.62, label_size=S.SMALL, attn_label="Attention", ffn_label="Feed-forward", **kw):
        super().__init__(**kw)
        self.attn = RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=S.ATTN,
                                     fill_color=S.ATTN, fill_opacity=0.14, stroke_width=2)
        self.ffn = RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=S.PARAM,
                                    fill_color=S.PARAM, fill_opacity=0.14, stroke_width=2)
        VGroup(self.ffn, self.attn).arrange(UP, buff=0.12)
        self.attn_t = T(attn_label, label_size).move_to(self.attn)
        self.ffn_t = T(ffn_label, label_size).move_to(self.ffn)
        self.add(self.ffn, self.attn, self.ffn_t, self.attn_t)


class LayerTower(VGroup):
    """A stack of thin layer slabs (used for 'the model')."""

    def __init__(self, n=12, w=2.6, h=0.16, gap=0.07, color=S.PARAM, opacity=0.25, **kw):
        super().__init__(**kw)
        self.slabs = VGroup(*[RoundedRectangle(corner_radius=0.03, width=w, height=h, stroke_color=color,
                                               stroke_width=1.2, fill_color=color, fill_opacity=opacity)
                              for _ in range(n)])
        self.slabs.arrange(UP, buff=gap)
        self.add(self.slabs)
