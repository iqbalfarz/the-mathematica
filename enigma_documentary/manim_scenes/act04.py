"""Act IV — the rotor as a permutation (s0404).

Every table is computed from enigma_core and asserted while rendering, so the
maths on screen is the same wiring the Blender rotor carries.
"""
from __future__ import annotations

import sys

from manim import (DOWN, LEFT, RIGHT, UP, FadeIn, FadeOut, LaggedStart, ReplacementTransform, Text, Transform,
                   VGroup, Write, AnimationGroup, Line)

from manim_scenes import style as S
from manim_scenes.base import ROOT, EnigmaScene
from manim_scenes.components import ALPHA, alphabet_row, caption, rotor_silhouette

sys.path.insert(0, str(ROOT / "src"))
from enigma_core.keyspace import fmt, rotor_wirings  # noqa: E402
from enigma_core.rotor import Rotor  # noqa: E402

ROTOR = "I"


def table_for(position: int) -> str:
    r = Rotor.from_name(ROTOR, position=position)
    out = "".join(ALPHA[r.forward(c)[0]] for c in range(26))
    assert sorted(out) == list(ALPHA), "a rotor must be a permutation"
    return out


class S0404Permutation(EnigmaScene):
    SCENE_ID = "s0404"

    def construct(self):
        cell = 0.48
        top = alphabet_row(size=26, cell=cell).shift(UP * 1.3)
        tin = caption("in", S.LABEL).next_to(top, LEFT, buff=0.35)
        self.until("b1")
        self.play(FadeIn(top, lag_ratio=0.03), FadeIn(tin), run_time=1.4)

        self.until("b2")
        perm_a = table_for(0)
        bottom = alphabet_row(perm_a, size=26, cell=cell, color=S.BRASS).shift(UP * 0.4)
        tout = caption("out", S.LABEL).next_to(bottom, LEFT, buff=0.35)
        ticks = VGroup(*[Line(top[i].get_bottom() + DOWN * 0.06, bottom[i].get_top() + UP * 0.06,
                              color=S.MUTED, stroke_width=1.5) for i in range(26)])
        pos = caption(f"rotor {ROTOR} at position A", S.SMALL).next_to(bottom, DOWN, buff=0.35)
        self.play(LaggedStart(*[FadeIn(VGroup(ticks[i], bottom[i]), shift=DOWN * 0.1) for i in range(26)],
                              lag_ratio=0.08), FadeIn(tout), run_time=2.6)
        self.play(FadeIn(pos), run_time=0.4)

        self.until("b3")
        check = alphabet_row(size=22, cell=cell, color=S.MUTED).shift(DOWN * 1.4)
        self.play(FadeIn(check), run_time=0.5)
        anims = []
        for i, c in enumerate(perm_a):
            j = ALPHA.index(c)
            anims.append(AnimationGroup(bottom[i].animate.set_color(S.CORRECT),
                                        check[j].animate.set_color(S.CORRECT)))
        self.play(LaggedStart(*anims, lag_ratio=0.12), run_time=2.8)
        once = caption("every letter exactly once", S.SMALL, S.CORRECT).next_to(check, DOWN, buff=0.3)
        self.play(FadeIn(once), run_time=0.4)

        self.until("b4")
        word = Text("permutation", font=S.SANS, font_size=S.H1, color=S.PAPER).to_edge(UP, buff=0.45)
        self.play(FadeOut(check), FadeOut(once), bottom.animate.set_color(S.BRASS), Write(word), run_time=1.4)

        self.until("b5")
        perm_b = table_for(1)
        new_bottom = alphabet_row(perm_b, size=26, cell=cell, color=S.BRASS).move_to(bottom)
        pos_b = caption(f"rotor {ROTOR} at position B", S.SMALL).move_to(pos)
        self.play(*[Transform(bottom[i], new_bottom[i]) for i in range(26)], Transform(pos, pos_b), run_time=1.6)
        self.play(*[bottom[i].animate.set_color(S.SIGNAL) for i in range(26) if perm_a[i] != perm_b[i]],
                  run_time=0.6)
        self.play(bottom.animate.set_color(S.BRASS), run_time=0.4)

        self.until("b6")
        n = rotor_wirings()
        product = Text("26 × 25 × 24 × … × 3 × 2 × 1", font=S.MONO, font_size=S.BODY, color=S.PAPER)
        product.shift(DOWN * 1.6)
        self.play(FadeIn(product, shift=UP * 0.1), run_time=0.9)
        value = Text(f"= {fmt(n)}", font=S.MONO, font_size=S.BODY, color=S.SIGNAL).next_to(product, DOWN, buff=0.3)
        note = caption("possible wirings for one rotor  (26!, our arithmetic)", S.LABEL).next_to(value, DOWN, buff=0.25)
        self.play(Write(value), FadeIn(note), run_time=1.6)

        self.until("b7")
        table = VGroup(top, bottom, ticks, tin, tout, pos, word, product, value, note)
        sil = [rotor_silhouette(width=0.7, height=2.0) for _ in range(3)]
        sil[1].move_to(DOWN * 0.1)
        self.play(ReplacementTransform(table, sil[1]), run_time=1.3)
        sil[0].next_to(sil[1], LEFT, buff=0.25)
        sil[2].next_to(sil[1], RIGHT, buff=0.25)
        self.play(FadeIn(sil[0], shift=RIGHT * 0.6), FadeIn(sil[2], shift=LEFT * 0.6), run_time=1.0)
        self.until_end()
