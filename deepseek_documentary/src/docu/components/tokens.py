from __future__ import annotations

from manim import DOWN, RIGHT, RoundedRectangle, VGroup

from .. import style as S
from .typography import T, fit_width

__all__ = ["Token", "TokenRow"]


class Token(VGroup):
    """A token: rounded blue tile with its text. Same look in every act."""

    def __init__(self, word: str, size: int = S.BODY, color=S.TOKEN, fill_opacity: float = 0.16, **kw):
        label = T(word, size, S.TEXT)
        box = RoundedRectangle(corner_radius=0.1, width=max(label.width + 0.32, 0.55),
                               height=label.height + 0.34 if label.height > 0.2 else 0.62,
                               stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=fill_opacity)
        box.height = max(box.height, 0.62)
        label.move_to(box)
        super().__init__(box, label, **kw)
        self.word = word
        self.box = box
        self.label = label

    def glow(self, color=None, opacity=0.45):
        return self.box.animate.set_fill(color or self.box.get_stroke_color(), opacity=opacity)


class TokenRow(VGroup):
    def __init__(self, words, size: int = S.BODY, buff: float = 0.14, max_width: float | None = None, **kw):
        toks = [Token(w, size) for w in words]
        super().__init__(*toks, **kw)
        self.arrange(RIGHT, buff=buff)
        fit_width(self, max_width)
        self.tokens = toks

    def __getitem__(self, i):
        return self.tokens[i] if isinstance(i, int) else super().__getitem__(i)

    def find(self, word: str) -> Token:
        for t in self.tokens:
            if t.word == word:
                return t
        raise KeyError(word)
