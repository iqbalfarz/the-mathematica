from __future__ import annotations

import numpy as np
from manim import DOWN, LEFT, RIGHT, UP, Rectangle, Square, VGroup, Brace

from .. import style as S
from .typography import T

__all__ = ["MatrixGrid", "cell_grid", "vec_column", "vec_row", "Heatmap"]


class MatrixGrid(VGroup):
    """A matrix drawn as a grid of cells with optional numbers.

    rows/cols addressable via .cell(i, j), .row(i), .col(j)."""

    def __init__(self, values=None, rows=3, cols=3, cell=0.62, color=S.PARAM, show_numbers=True,
                 num_size=S.SMALL, fill_opacity=0.1, **kw):
        super().__init__(**kw)
        if values is not None:
            values = np.asarray(values)
            rows, cols = values.shape
        self.rows, self.cols = rows, cols
        self.cells = VGroup()
        self.nums = VGroup()
        for i in range(rows):
            for j in range(cols):
                sq = Square(cell, stroke_color=color, stroke_width=1.6, fill_color=color, fill_opacity=fill_opacity)
                sq.move_to([j * cell, -i * cell, 0])
                self.cells.add(sq)
                if values is not None and show_numbers:
                    v = values[i, j]
                    txt = f"{v:g}" if isinstance(v, (int, float, np.integer, np.floating)) else str(v)
                    n = T(txt, num_size, S.TEXT, mono=True)
                    if n.width > cell * 0.84:
                        n.scale_to_fit_width(cell * 0.84)
                    self.nums.add(n.move_to(sq))
        self.add(self.cells, self.nums)
        self.move_to([0, 0, 0])

    def cell(self, i, j):
        return self.cells[i * self.cols + j]

    def num(self, i, j):
        return self.nums[i * self.cols + j]

    def row(self, i) -> VGroup:
        return VGroup(*[self.cell(i, j) for j in range(self.cols)])

    def col(self, j) -> VGroup:
        return VGroup(*[self.cell(i, j) for i in range(self.rows)])

    def row_nums(self, i) -> VGroup:
        return VGroup(*[self.num(i, j) for j in range(self.cols)])

    def col_nums(self, j) -> VGroup:
        return VGroup(*[self.num(i, j) for i in range(self.rows)])


def cell_grid(rows, cols, size, color=S.PARAM, stroke=0.6, fill_opacity=0.15, gap=0.0) -> VGroup:
    g = VGroup()
    for i in range(rows):
        for j in range(cols):
            g.add(Square(size, stroke_color=color, stroke_width=stroke, fill_color=color,
                         fill_opacity=fill_opacity).move_to([j * (size + gap), -i * (size + gap), 0]))
    return g.move_to([0, 0, 0])


def vec_column(values, color=S.TOKEN, cell=0.6, num_size=S.SMALL):
    return MatrixGrid(np.array(values, dtype=object).reshape(-1, 1), cell=cell, color=color, num_size=num_size)


def vec_row(values, color=S.PARAM, cell=0.6, num_size=S.SMALL):
    return MatrixGrid(np.array(values, dtype=object).reshape(1, -1), cell=cell, color=color, num_size=num_size)


class Heatmap(VGroup):
    """n x n attention-style heatmap; values in [0,1] map to opacity of ATTN."""

    def __init__(self, values, cell=0.4, color=S.ATTN, **kw):
        super().__init__(**kw)
        values = np.asarray(values, dtype=float)
        self.n, self.m = values.shape
        self.cells = VGroup()
        for i in range(self.n):
            for j in range(self.m):
                v = float(values[i, j])
                sq = Square(cell, stroke_color=S.GRID, stroke_width=0.8, fill_color=color,
                            fill_opacity=0.06 + 0.9 * v)
                sq.move_to([j * cell, -i * cell, 0])
                self.cells.add(sq)
        self.add(self.cells)
        self.move_to([0, 0, 0])
