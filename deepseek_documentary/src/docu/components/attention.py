from __future__ import annotations

import numpy as np
from manim import (DOWN, UP, ArcBetweenPoints, VGroup)

from .. import style as S

__all__ = ["attention_arcs", "softmax"]


def softmax(x):
    x = np.asarray(x, dtype=float)
    e = np.exp(x - x.max())
    return e / e.sum()


def attention_arcs(src, targets, weights, color=S.ATTN, max_width=10, up=True, min_op=0.15):
    """Arcs from `src` token to each target token, thickness = weight."""
    g = VGroup()
    for t, w in zip(targets, weights):
        if t is src:
            continue
        a = src.get_top() if up else src.get_bottom()
        b = t.get_top() if up else t.get_bottom()
        ang = -1.2 if (b[0] > a[0]) == up else 1.2
        arc = ArcBetweenPoints(a + (UP if up else DOWN) * 0.05, b + (UP if up else DOWN) * 0.05, angle=ang,
                               color=color, stroke_width=max(1.0, max_width * float(w)),
                               stroke_opacity=max(min_op, min(1.0, 0.25 + float(w))))
        g.add(arc)
    return g
