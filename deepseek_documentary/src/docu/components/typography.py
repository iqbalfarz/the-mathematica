from __future__ import annotations

from manim import (DOWN, LEFT, RIGHT, UP, UL, UR, DL, DR, MathTex, RoundedRectangle, Text,
                   VGroup, config, Line)

from .. import style as S

__all__ = ["T", "M", "title_text", "caption", "source_line", "chip", "question_banner",
           "frame_w", "frame_h", "safe_top", "safe_bottom", "safe_left", "safe_right", "fit_width",
           "big_number", "persistent_question", "strike"]


def frame_w() -> float:
    return config.frame_width


def frame_h() -> float:
    return config.frame_height


def safe_top() -> float:
    return frame_h() / 2 - S.SAFE


def safe_bottom() -> float:
    return -frame_h() / 2 + S.SAFE


def safe_left() -> float:
    return -frame_w() / 2 + S.SAFE


def safe_right() -> float:
    return frame_w() / 2 - S.SAFE


def fit_width(m, max_w: float | None = None):
    max_w = max_w or (frame_w() - 2 * S.SAFE)
    if m.width > max_w:
        m.scale_to_fit_width(max_w)
    return m


def T(text: str, size: int = S.BODY, color=S.TEXT, weight: str = "NORMAL", mono: bool = False, **kw) -> Text:
    """Text in the house font. Keeps font_size >= TINY for legibility."""
    size = max(size, S.TINY)
    # Pango hints glyph positions at small sizes, which produces uneven gaps
    # ("20 22"). Shaping at >=120 and scaling down gives clean kerning.
    base = max(size, 120)
    t = Text(text, font=S.MONO if mono else S.FONT, font_size=base, color=color, weight=weight, **kw)
    if base != size:
        t.scale(size / base)
    return t


def M(tex: str, size: int = 40, color=S.TEXT, **kw) -> MathTex:
    return MathTex(tex, font_size=max(size, 24), color=color, **kw)


def title_text(text: str, sub: str | None = None) -> VGroup:
    t = T(text, S.H2, weight="BOLD")
    g = VGroup(t)
    if sub:
        g.add(T(sub, S.SMALL, S.MUTED))
    g.arrange(DOWN, buff=0.18, aligned_edge=LEFT)
    return fit_width(g)


def caption(text: str, color=S.MUTED, size: int = S.SMALL) -> Text:
    c = T(text, size, color)
    fit_width(c)
    c.move_to([0, safe_bottom() + c.height / 2 + 0.05, 0])
    return c


def source_line(text: str) -> Text:
    """Small attribution line, bottom-right, always inside the safe frame."""
    s = T(text, S.TINY, S.MUTED)
    fit_width(s, frame_w() * 0.62)
    s.move_to([safe_right() - s.width / 2, safe_bottom() + s.height / 2, 0])
    return s


def chip(text: str, color=S.MUTED, size: int = S.TINY, fill_opacity: float = 0.12) -> VGroup:
    t = T(text, size, color, weight="BOLD")
    box = RoundedRectangle(corner_radius=0.08, width=t.width + 0.3, height=t.height + 0.2,
                           stroke_color=color, stroke_width=1.5, fill_color=color, fill_opacity=fill_opacity)
    return VGroup(box, t.move_to(box))


def question_banner(text: str, size: int = S.H2) -> VGroup:
    t = T(text, size, S.TEXT, weight="BOLD")
    fit_width(t, frame_w() - 2 * S.SAFE - 0.6)
    bar = Line(LEFT, RIGHT, color=S.PARAM, stroke_width=4).set_width(t.width * 0.35)
    return VGroup(t, bar).arrange(DOWN, buff=0.25)


def persistent_question(text: str = "What do you do when you can't buy your way out?") -> VGroup:
    """The central loop, pinned small at the top-left."""
    g = VGroup(T("?", S.SMALL, S.PARAM, weight="BOLD"), T(text, S.TINY, S.MUTED))
    g.arrange(RIGHT, buff=0.15)
    g.move_to([safe_left() + g.width / 2, safe_top() - g.height / 2, 0])
    return g


def big_number(text: str, color=S.TEXT, size: int = 96) -> Text:
    return T(text, size, color, weight="BOLD")


def strike(m, color=S.LOSS) -> Line:
    return Line(m.get_corner(DL) + LEFT * 0.1, m.get_corner(UR) + RIGHT * 0.1, color=color, stroke_width=6)
