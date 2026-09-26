"""Act II — Forget Enigma: fixed substitution, its weakness, and the moving wheel.

Letters that the narration says out loud are computed here from enigma_core
(the same simulator the Blender shots use), then asserted against the script's
sim_check in tests/test_script.py.
"""
from __future__ import annotations

import sys
from collections import Counter

import numpy as np
from manim import (DOWN, LEFT, RIGHT, UP, Arrow, Brace, Create, FadeIn, FadeOut, GrowFromEdge, Indicate,
                   LaggedStart, Rectangle, ReplacementTransform, Rotate, ShowPassingFlash, SurroundingRectangle,
                   Text, Transform, VGroup, Write, AnimationGroup, Line)

from manim_scenes import style as S
from manim_scenes.base import ROOT, EnigmaScene
from manim_scenes.components import ALPHA, Wheel, alphabet_row, arrow_down, caption, label_illustrative, letter, rotor_silhouette

sys.path.insert(0, str(ROOT / "src"))
from enigma_core.rotor import Rotor  # noqa: E402
from enigma_core.wiring import ROTORS  # noqa: E402


def caesar(text, k=3):
    return "".join(ALPHA[(ALPHA.index(c) + k) % 26] for c in text)


class S0201Caesar(EnigmaScene):
    SCENE_ID = "s0201"

    def construct(self):
        top = alphabet_row().shift(UP * 1.6)
        bottom = alphabet_row(color=S.BRASS).shift(UP * 0.6)
        self.until("b1")
        self.play(LaggedStart(FadeIn(top, lag_ratio=0.03), FadeIn(bottom, lag_ratio=0.03), lag_ratio=0.4), run_time=2)

        self.until("b2")
        # Slide the bottom row 3 cells left; A B C wrap round to the end.
        cell = bottom.cell
        moves = []
        for i, m in enumerate(bottom):
            if i < 3:
                target = m.copy().move_to(np.array([(26 - 3 + i - 12.5) * cell, m.get_y(), 0]))
                moves.append(m.animate(path_arc=-1.2).move_to(target))
            else:
                moves.append(m.animate.shift(LEFT * 3 * cell))
        self.play(*moves, run_time=1.8)
        shifted = VGroup(*sorted(bottom, key=lambda m: m.get_x()))
        arrows = VGroup(*[arrow_down(top[i], shifted[i], S.SIGNAL) for i in (0, 1)])
        self.play(Create(arrows), run_time=1.0)

        self.until("b3")
        tag = caption("Caesar shift  +3").next_to(bottom, DOWN, buff=0.5)
        self.play(FadeIn(tag, shift=UP * 0.1), run_time=0.8)

        self.until("b4")
        plain, cipher = "HELLO", caesar("HELLO")
        pw = VGroup(*[letter(c, S.H2) for c in plain]).arrange(RIGHT, buff=0.35).shift(DOWN * 1.6)
        cw = VGroup(*[letter(c, S.H2, S.SIGNAL) for c in cipher]).arrange(RIGHT, buff=0.35).shift(DOWN * 2.8)
        self.play(FadeOut(tag), Write(pw), run_time=1.0)
        for p, c in zip(pw, cw):
            i = ALPHA.index(p.text)
            self.play(Indicate(top[i], color=S.SIGNAL, scale_factor=1.3),
                      Indicate(shifted[i], color=S.SIGNAL, scale_factor=1.3),
                      ReplacementTransform(p.copy(), c), run_time=0.45)
        self.until_end()


class S0202FixedRuleLeaks(EnigmaScene):
    SCENE_ID = "s0202"

    def construct(self):
        plain, cipher = "HELLO", caesar("HELLO")
        pw = VGroup(*[letter(c, S.H1) for c in plain]).arrange(RIGHT, buff=0.45).shift(UP * 1.2)
        cw = VGroup(*[letter(c, S.H1, S.SIGNAL) for c in cipher]).arrange(RIGHT, buff=0.45).shift(DOWN * 0.2)
        self.add(pw, cw)
        self.until("b1")
        boxes = VGroup(*[SurroundingRectangle(m, color=S.UNKNOWN, buff=0.08) for m in (pw[2], pw[3], cw[2], cw[3])])
        self.play(Create(boxes), run_time=1.0)
        self.play(Indicate(VGroup(cw[2], cw[3]), color=S.UNKNOWN), run_time=1.0)

        self.until("b2")
        self.play(FadeOut(boxes), VGroup(pw, cw).animate.scale(0.6).to_edge(UP, buff=0.5), run_time=0.8)
        rows = VGroup(*[VGroup(letter("H", S.H2), Text("→", font=S.SANS, font_size=S.H2, color=S.MUTED),
                               letter("K", S.H2, S.SIGNAL)).arrange(RIGHT, buff=0.3) for _ in range(3)])
        rows.arrange(DOWN, buff=0.35).shift(DOWN * 0.3)
        self.play(LaggedStart(*[FadeIn(r, shift=DOWN * 0.1) for r in rows], lag_ratio=0.35), run_time=1.4)
        same = caption("same letter in  →  same letter out", S.BODY, S.PAPER).next_to(rows, DOWN, buff=0.5)
        self.play(FadeIn(same), run_time=0.6)

        self.until("b3")
        self.play(FadeOut(VGroup(rows, same, pw, cw)), run_time=0.5)
        # A scrambled (but still fixed) alphabet: the wiring of rotor I, used as a plain substitution.
        scrambled = ROTORS["I"]["wiring"]
        top = alphabet_row().shift(UP * 1.2)
        bot = alphabet_row(color=S.BRASS).shift(UP * 0.2)
        self.play(FadeIn(top), FadeIn(bot), run_time=0.6)
        self.play(*[m.animate(path_arc=0.8).move_to(np.array([(scrambled.index(ALPHA[i]) - 12.5) * bot.cell,
                                                              bot.get_y(), 0])) for i, m in enumerate(bot)],
                  run_time=1.6)
        note = caption("scrambled — but still one fixed rule").next_to(bot, DOWN, buff=0.4)
        self.play(FadeIn(note), run_time=0.5)

        self.until("b4")
        self.play(FadeOut(VGroup(top, bot, note)), run_time=0.5)
        german = ("DIEDEUTSCHESPRACHEHATVIELEBUCHSTABENABEREINERKOMMTVIELHAEUFIGERVORALSALLEANDERENUND"
                  "DASISTDASEDERBRIEFWIRDBEIMLESENVERRATEN")
        sub = "".join(scrambled[ALPHA.index(c)] for c in german)
        chart_p = self._bars(german, S.PAPER).shift(LEFT * 3.4 + DOWN * 0.3)
        chart_c = self._bars(sub, S.SIGNAL).shift(RIGHT * 3.4 + DOWN * 0.3)
        tp = caption("German plaintext", S.SMALL, S.PAPER).next_to(chart_p, UP, buff=0.3)
        tc = caption("after a fixed substitution", S.SMALL, S.SIGNAL).next_to(chart_c, UP, buff=0.3)
        self.play(FadeIn(tp), *[GrowFromEdge(b, DOWN) for b in chart_p.bars], FadeIn(chart_p.labels), run_time=1.4)
        self.play(FadeIn(tc), *[GrowFromEdge(b, DOWN) for b in chart_c.bars], FadeIn(chart_c.labels), run_time=1.4)
        self.play(Indicate(chart_p.bars[0], color=S.UNKNOWN), Indicate(chart_c.bars[0], color=S.UNKNOWN), run_time=1)
        self.add(label_illustrative())
        self.until_end()

    def _bars(self, text, color, n=8):
        counts = Counter(text).most_common(n)
        top = counts[0][1]
        bars = VGroup(*[Rectangle(width=0.42, height=2.6 * c / top, fill_color=color, fill_opacity=0.85,
                                  stroke_width=0) for _, c in counts]).arrange(RIGHT, buff=0.14, aligned_edge=DOWN)
        labels = VGroup(*[letter(ch, S.SMALL, color).next_to(b, DOWN, buff=0.12) for (ch, _), b in zip(counts, bars)])
        g = VGroup(bars, labels)
        g.bars, g.labels = bars, labels
        return g


class S0203MovingAlphabet(EnigmaScene):
    SCENE_ID = "s0203"
    KEY = "H"

    def construct(self):
        wiring = ROTORS["I"]["wiring"]
        wheel = Wheel(wiring, radius=2.5).shift(LEFT * 2.2 + DOWN * 0.2)
        rotor = Rotor.from_name("I")       # the truth the wheel must agree with
        results = VGroup().to_edge(RIGHT, buff=1.0)
        self.until("b1")
        self.play(Create(wheel.rim), FadeIn(wheel.labels, lag_ratio=0.02), run_time=1.4)
        self.play(FadeIn(wheel.contacts), Create(wheel.chords, lag_ratio=0.03), run_time=1.6)

        steps = [("b2+1.2", 0), ("b3+1.0", 1), ("b4", 2), ("b4+1.3", 3)]
        prev_path = None
        rows = []
        for ref, p in steps:
            self.until(ref)
            if p > 0:
                self.play(Rotate(wheel.chords, angle=wheel.step, about_point=wheel.rim.get_center()),
                          run_time=0.3)
                wheel.position = p
            rotor.position = p
            expected = ALPHA[rotor.forward(ALPHA.index(self.KEY))[0]]
            path, out = wheel.path(self.KEY)
            assert out == expected, f"wheel geometry disagrees with enigma_core at position {p}"
            anims = [Create(path), Indicate(wheel.labels[ALPHA.index(self.KEY)], color=S.SIGNAL),
                     Indicate(wheel.labels[ALPHA.index(out)], color=S.SIGNAL)]
            if prev_path is not None:
                anims.append(FadeOut(prev_path))
            self.play(*anims, run_time=0.45)
            prev_path = path
            row = VGroup(letter(self.KEY, S.H2), Text("→", font=S.SANS, font_size=S.H2, color=S.MUTED),
                         letter(out, S.H2, S.SIGNAL), caption(f"turn {p}", S.LABEL)).arrange(RIGHT, buff=0.3)
            row.move_to(RIGHT * 3.6 + UP * (1.6 - 0.9 * p))
            rows.append(row)
            self.play(FadeIn(row, shift=LEFT * 0.2), run_time=0.3)

        self.until("b5")
        rows_g = VGroup(*rows)
        self.play(FadeOut(prev_path), rows_g.animate.shift(UP * 0.2), run_time=0.5)
        eq = VGroup(caption("same input", S.SMALL, S.PAPER), caption("+", S.SMALL),
                    caption("different wheel position", S.SMALL, S.BRASS), caption("=", S.SMALL),
                    caption("different output", S.SMALL, S.SIGNAL)).arrange(RIGHT, buff=0.18)
        eq.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(eq, lag_ratio=0.2), run_time=1.2)

        self.until("b6")
        sil = [rotor_silhouette() for _ in range(3)]
        sil[1].move_to(wheel.rim.get_center())
        self.play(FadeOut(rows_g), FadeOut(eq), ReplacementTransform(wheel, sil[1]), run_time=1.2)
        sil[0].next_to(sil[1], LEFT, buff=0.25)
        sil[2].next_to(sil[1], RIGHT, buff=0.25)
        name = caption("rotor", S.BODY, S.BRASS).next_to(sil[1], DOWN, buff=0.4)
        self.play(FadeIn(sil[0], shift=RIGHT * 0.6), FadeIn(sil[2], shift=LEFT * 0.6), FadeIn(name), run_time=1.0)
        self.play(VGroup(*sil, name).animate.move_to(DOWN * 0.1), run_time=0.8)
        self.until_end()
