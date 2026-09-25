"""ACT 11 — The numbers, honestly."""
from manim import *  # noqa: F401,F403

from docu import style as S
from docu.base_scene import DocScene
from docu.components import (M, T, WALLS, chip, fit_width, source_line, strike)


class S1101TheLedger(DocScene):
    SCENE_ID = "s1101"

    def construct(self):
        self.beat("b1")
        big = T("$5.576M", 120, S.PARAM, weight="BOLD", mono=True)
        self.play(FadeIn(big, scale=0.9), run_time=self.dur(0.5))
        self.hold()

        self.beat("b2")
        self.play(big.animate.scale(0.45).to_edge(UP, buff=0.6), run_time=0.6)
        eq = M(r"2.788\text{M GPU-hours} \times \$2 \,/\, \text{GPU-hour} = \$5.576\text{M}", 46)
        fit_width(eq)
        note = T("$2/hour is an assumed rental price", S.SMALL, S.MUTED).next_to(eq, DOWN, buff=0.3)
        self.play(Write(eq), run_time=self.dur(0.5))
        self.play(FadeIn(note), run_time=0.5)
        self.hold()

        self.beat("b3")
        self.play(FadeOut(VGroup(eq, note)), run_time=0.4)
        inc = VGroup(T("INCLUDED", S.BODY, S.EXPERT, weight="BOLD"),
                     T("GPU time of the final, official training run", S.SMALL, S.TEXT)).arrange(DOWN, buff=0.3,
                                                                                              aligned_edge=LEFT)
        exc_items = ["prior research", "ablation experiments", "buying the GPUs", "salaries", "failed attempts"]
        exc = VGroup(T("NOT INCLUDED", S.BODY, S.LOSS, weight="BOLD"),
                     *[T("· " + e, S.SMALL, S.TEXT) for e in exc_items]).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        cols = VGroup(inc, exc).arrange(RIGHT, buff=1.4, aligned_edge=UP).move_to(DOWN * 0.3)
        fit_width(cols)
        self.play(FadeIn(inc, shift=UP * 0.2), run_time=self.dur(0.25))
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in exc], lag_ratio=0.2), run_time=self.dur(0.5))
        src = source_line("DeepSeek-V3 Technical Report: costs 'exclude prior research and ablation experiments'")
        self.add(src)
        self.hold()

        self.beat("b4")
        self.play(FadeOut(VGroup(cols, src, big)), run_time=0.4)
        wrong = T("“DeepSeek built its AI for $5.6M”", S.H2, S.TEXT)
        fit_width(wrong)
        wrong.move_to(UP * 0.9)
        st = strike(wrong)
        right = T("final training run ≈ $5.6M of GPU time (reported)", S.H2, S.EXPERT, weight="BOLD")
        fit_width(right)
        right.move_to(DOWN * 0.8)
        self.play(FadeIn(wrong), run_time=0.6)
        self.play(Create(st), run_time=0.5)
        self.play(FadeIn(right, shift=UP * 0.2), run_time=self.dur(0.35))
        self.hold()

        self.beat("b5")
        self.play(FadeOut(VGroup(wrong, st, right)), run_time=0.4)
        rows = VGroup(
            VGroup(T("DeepSeek-V4.1-Flash", S.BODY, S.TEXT, weight="BOLD")),
            VGroup(T("training hardware:", S.BODY, S.MUTED), T("not reported", S.BODY, S.PARAM, weight="BOLD")),
            VGroup(T("training cost:", S.BODY, S.MUTED), T("not reported", S.BODY, S.PARAM, weight="BOLD")))
        for r in rows[1:]:
            r.arrange(RIGHT, buff=0.3)
        rows.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        box = SurroundingRectangle(rows, color=S.MUTED, buff=0.4, corner_radius=0.12)
        self.play(Create(box), FadeIn(rows, lag_ratio=0.3), run_time=self.dur(0.5))
        guess = T("so we won't guess", S.SMALL, S.MUTED).next_to(box, DOWN, buff=0.3)
        self.play(FadeIn(guess), run_time=0.5)
        self.hold()
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.finish(tail=0.1)


class S1102WhatWasSurprising(DocScene):
    SCENE_ID = "s1102"

    def construct(self):
        self.beat("b1")
        ideas = [("Mixture of Experts", S.EXPERT, "1991 / 2017"), ("Attention", S.ATTN, "2014 / 2017"),
                 ("Low-precision numbers", S.PARAM, "2018")]
        cards = VGroup()
        for n, c, y in ideas:
            box = RoundedRectangle(corner_radius=0.12, width=3.6, height=1.6, stroke_color=c, stroke_width=2,
                                   fill_color=S.PANEL, fill_opacity=1)
            t = T(n, S.BODY, c, weight="BOLD")
            fit_width(t, 3.3)
            p = chip(f"prior art · {y}", S.MUTED)
            VGroup(t, p).arrange(DOWN, buff=0.25).move_to(box)
            cards.add(VGroup(box, t, p))
        cards.arrange(RIGHT, buff=0.4).move_to(UP * 0.2)
        fit_width(cards)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cards], lag_ratio=0.3), run_time=self.dur(0.6))
        self.hold()

        self.beat("b2")
        self.play(FadeOut(cards, shift=UP * 0.3), run_time=self.dur(0.4))
        hdr = VGroup(T("WALL", S.SMALL, S.MUTED, weight="BOLD"), T("WHAT DEEPSEEK AIMED AT IT", S.SMALL, S.MUTED,
                                                                   weight="BOLD"))
        hdr[0].move_to([-4.3, 1.3, 0])
        hdr[1].move_to([1.3, 1.3, 0])
        line = Line([-6.2, 1.0, 0], [6.2, 1.0, 0], color=S.DIM)
        self.play(FadeIn(hdr), Create(line), run_time=0.6)
        self.hold()

        self.beat("b3")
        rows = [("COMPUTE", S.COMPUTE, "MoE: 37B of 671B active (V3)"),
                ("COMMUNICATION", S.COMM, "DualPipe overlap + FP8 numbers (V3)"),
                ("MEMORY", S.MEMORY, "MLA → CSA2 + FP4: 890 B/token (V4.1-Flash)")]
        rg = VGroup()
        for k, (w, c, txt) in enumerate(rows):
            y = 0.35 - k * 1.0
            a = T(w, S.BODY, c, weight="BOLD").move_to([-4.3, y, 0])
            b = T(txt, S.BODY, S.TEXT)
            fit_width(b, 7.8)
            b.move_to([1.6, y, 0])
            rg.add(VGroup(a, b))
            self.play(FadeIn(a, shift=RIGHT * 0.2), FadeIn(b, shift=LEFT * 0.2), run_time=self.dur(0.25, lo=0.6))
        self.hold()

        self.beat("b4")
        cap = T("shaped around its bottlenecks, not its budget", S.H2, S.PARAM, weight="BOLD").move_to(DOWN * 2.8)
        fit_width(cap)
        self.play(FadeIn(cap, shift=UP * 0.2), run_time=self.dur(0.4))
        self.hold()
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.finish(tail=0.1)
