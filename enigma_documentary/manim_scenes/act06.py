"""Act VI — the machine's state, and what the double step does to it (s0604).

The table, the pawls that caught teeth, the middle rotor's dwell on each letter and
the period are all computed from enigma_core while rendering (never typed in).
"""
from __future__ import annotations

import sys
from collections import Counter

from manim import (DOWN, LEFT, RIGHT, UP, FadeIn, FadeOut, LaggedStart, Line, Rectangle, SurroundingRectangle,
                   Text, VGroup, Write)

from manim_scenes import style as S
from manim_scenes.base import ROOT, EnigmaScene
from manim_scenes.components import ALPHA, caption

sys.path.insert(0, str(ROOT / "src"))
from enigma_core import EnigmaMachine  # noqa: E402
from enigma_core.configuration import load_configs  # noqa: E402
from enigma_core.keyspace import fmt  # noqa: E402

MACHINE = "double_step_demo"


def _machine():
    return EnigmaMachine(load_configs(ROOT / "config" / "machines.yaml")[MACHINE])


def state_rows(n=3):
    """[(state, pawls that caught teeth)] for the start and n presses."""
    presses = _machine().press_keys("A" * n)
    rows = [(presses[0].positions_before, "")]
    for p in presses:
        pawls = sorted({s.pawl for s in p.steps})
        rows.append((p.positions_after, " + ".join(str(k) for k in pawls)))
    return rows


def period_and_middle_dwell():
    """Presses until the start state returns, and how many presses the middle rotor
    spends on each letter per turn of the left rotor, over that whole cycle."""
    m = _machine()
    start = m.positions
    dwell = Counter()
    n = 0
    while True:
        p = m.press_keys("A")[0]
        dwell[p.positions_before[1]] += 1
        n += 1
        if p.positions_after == start:
            return n, {c: dwell[c] // 26 for c in ALPHA}


def window(ch, size=0.9, color=S.PAPER):
    box = Rectangle(width=size, height=size, color=S.MUTED, stroke_width=2)
    t = Text(ch, font=S.MONO, font_size=S.H2, color=color).move_to(box)
    return VGroup(box, t)


class S0604CountTheSteps(EnigmaScene):
    SCENE_ID = "s0604"

    def construct(self):
        rows = state_rows()
        assert [r[0] for r in rows] == ["ADU", "ADV", "AEW", "BFX"]
        period, dwell = period_and_middle_dwell()
        assert period == 26 * 25 * 26 == 16900

        # b1: the three windows, and the word "state"
        self.until("b1")
        wins = VGroup(*[window(c) for c in rows[0][0]]).arrange(RIGHT, buff=0.2).shift(UP * 1.2)
        self.play(LaggedStart(*[FadeIn(w, shift=DOWN * 0.1) for w in wins], lag_ratio=0.2), run_time=1.2)
        word = Text("state", font=S.SANS, font_size=S.H1, color=S.BRASS).next_to(wins, DOWN, buff=0.6)
        note = caption("where every rotor is, right now", S.SMALL).next_to(word, DOWN, buff=0.2)
        self.wait(1.8)
        self.play(Write(word), FadeIn(note), run_time=1.2)

        # b2: the table, one row per spoken state
        self.until("b2")
        head = VGroup(*[caption(h, S.LABEL) for h in ("L", "M", "R")])
        cells = []
        y0 = 2.2
        for r, (state, pawls) in enumerate(rows):
            row = VGroup(*[Text(c, font=S.MONO, font_size=S.H2, color=S.PAPER) for c in state])
            for i, t in enumerate(row):
                t.move_to(LEFT * (2.2 - i * 1.1) + UP * (y0 - 0.95 * (r + 1)))
                if r and c_changed(rows, r, i):
                    t.set_color(S.SIGNAL)
            tag = caption(f"pawl {pawls}" if pawls and "+" not in pawls else (f"pawls {pawls}" if pawls else "start"),
                          S.SMALL, S.MUTED if r == 0 else S.PAPER)
            tag.move_to(RIGHT * 1.9 + UP * (y0 - 0.95 * (r + 1)))
            if "3" in pawls:
                tag.set_color(S.BRASS)
            cells.append((row, tag))
        for i, h in enumerate(head):
            h.move_to(LEFT * (2.2 - i * 1.1) + UP * y0)
        self.play(FadeOut(VGroup(wins, word, note)), FadeIn(head), run_time=0.5)
        spoken = self.slot("b2", "b3") - 1.1
        for row, tag in cells:
            self.play(FadeIn(row, shift=DOWN * 0.1), FadeIn(tag), run_time=0.35)
            self.wait(max(0.1, spoken / len(cells) - 0.35))
        dbl = caption("double step", S.LABEL, S.BRASS).next_to(cells[-1][1], RIGHT, buff=0.3)
        self.play(FadeIn(dbl), run_time=0.3)

        # b3: which columns move how often
        self.until("b3")
        col = lambda i: VGroup(*[cells[r][0][i] for r in range(len(cells))])   # noqa: E731
        boxes = [SurroundingRectangle(col(i), color=c, buff=0.12, stroke_width=2)
                 for i, c in ((2, S.SIGNAL), (1, S.BRASS), (0, S.MUTED))]
        for b in boxes:
            self.play(FadeIn(b), run_time=0.5)
            self.wait(1.2)

        # b4: the middle rotor's dwell on each letter, per turn of the left rotor
        self.until("b4")
        table = VGroup(head, *[VGroup(r, t) for r, t in cells], dbl, *boxes)
        self.play(table.animate.scale(0.55).to_edge(UP, buff=0.3).shift(LEFT * 3.6), run_time=0.8)
        width = 11.5
        total = sum(dwell.values())
        assert dwell["E"] == 1 and dwell["A"] == 26, dwell
        x = -width / 2
        bars, labels = VGroup(), VGroup()
        for c in ALPHA:
            w = width * dwell[c] / total
            bar = Rectangle(width=max(w - 0.02, 0.02), height=0.6, stroke_width=0,
                            fill_color=S.SIGNAL if c == "E" else S.BRASS, fill_opacity=1 if c == "E" else 0.55)
            bar.move_to(RIGHT * (x + w / 2) + DOWN * 0.6)
            lab = Text(c, font=S.MONO, font_size=S.LABEL, color=S.SIGNAL if c == "E" else S.MUTED)
            lab.next_to(bar, DOWN, buff=0.12)
            bars.add(bar)
            labels.add(lab)
            x += w
        title = caption("key presses the middle rotor spends on each letter, per turn of the left rotor",
                        S.LABEL).next_to(bars, UP, buff=0.35)
        self.play(FadeIn(title), LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.04), FadeIn(labels), run_time=2.2)
        e_note = caption(f"E: {dwell['E']} press", S.SMALL, S.SIGNAL).next_to(labels[4], DOWN, buff=0.25)
        a_note = caption(f"most letters: {dwell['A']}", S.SMALL).next_to(labels[12], DOWN, buff=0.25)
        self.play(FadeIn(e_note), FadeIn(a_note), run_time=0.6)

        # b5: the period
        self.until("b5")
        self.play(FadeOut(VGroup(bars, labels, title, e_note, a_note)), run_time=0.5)
        got = Text(f"26 × 25 × 26 = {fmt(period)}", font=S.MONO, font_size=S.H2, color=S.SIGNAL).shift(DOWN * 0.4)
        naive = Text(f"26 × 26 × 26 = {fmt(26 ** 3)}", font=S.MONO, font_size=S.BODY, color=S.MUTED)
        naive.next_to(got, DOWN, buff=0.5)
        strike = Line(naive.get_left(), naive.get_right(), color=S.REJECT, stroke_width=3)
        lab = caption("key presses before the rotors are back where they started", S.SMALL).next_to(got, UP, buff=0.35)
        self.play(FadeIn(lab), Write(got), run_time=1.6)
        self.wait(1.5)
        self.play(FadeIn(naive), run_time=0.6)
        self.play(Write(strike), run_time=0.5)
        self.until_end()


def c_changed(rows, r, i):
    return rows[r][0][i] != rows[r - 1][0][i]
