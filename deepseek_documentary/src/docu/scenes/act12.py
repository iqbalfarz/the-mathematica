"""ACT 12 — The whole machine, and the answer to the central question."""
import numpy as np
from manim import *  # noqa: F401,F403

from docu import style as S
from docu.base_scene import DocScene
from docu.components import (GPU, T, WallsLegend, chip, fit_width, gpu_wall, question_banner, source_line)

QUESTION = "What do you do when you can't buy your way out?"
FWD = [("DATA", S.MUTED), ("TOKENS", S.TOKEN), ("EMBEDDINGS", S.TOKEN), ("ATTENTION", S.ATTN), ("ROUTER", S.ROUTER),
       ("EXPERTS", S.EXPERT), ("OUTPUT", S.TOKEN)]
BWD = [("LOSS", S.LOSS), ("GRADIENTS", S.GRAD), ("UPDATE", S.PARAM)]


def node(name, color, w=1.55, h=0.8):
    box = RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color=color, stroke_width=2,
                           fill_color=color, fill_opacity=0.12)
    t = T(name, S.TINY, color, weight="BOLD")
    if t.width > w * 0.9:
        t.scale_to_fit_width(w * 0.9)
    return VGroup(box, t.move_to(box))


class S1201WholeMachine(DocScene):
    SCENE_ID = "s1201"

    def construct(self):
        self.beat("b1")
        stage = VGroup(*[Dot([x, y, 0], radius=0.025, color=S.DIM) for x in np.arange(-6.5, 6.6, 0.5)
                         for y in np.arange(-3.5, 3.6, 0.5)])
        self.play(FadeIn(stage, lag_ratio=0.002), self.camera.frame.animate.scale(1.08), run_time=self.dur(0.8))
        self.play(self.camera.frame.animate.scale(1 / 1.08), run_time=0.4)
        self.hold()

        self.beat("b2")
        fwd = VGroup(*[node(n, c) for n, c in FWD]).arrange(RIGHT, buff=0.3).move_to(UP * 1.2)
        fit_width(fwd)
        arrs = VGroup(*[Arrow(fwd[k].get_right(), fwd[k + 1].get_left(), buff=0.05, color=S.MUTED, stroke_width=2.5,
                              max_tip_length_to_length_ratio=0.35) for k in range(len(FWD) - 1)])
        self.play(FadeIn(fwd[0]), run_time=0.3)
        for k in range(1, len(FWD)):
            self.play(GrowArrow(arrs[k - 1]), FadeIn(fwd[k], shift=RIGHT * 0.15), run_time=self.dur(0.12, lo=0.4))
        self.hold()

        self.beat("b3")
        bwd = VGroup(*[node(n, c) for n, c in BWD]).arrange(LEFT, buff=0.9)
        bwd.move_to([fwd[-1].get_x() - bwd.width / 2 + fwd[-1].width / 2, -1.2, 0])
        down = Arrow(fwd[-1].get_bottom(), bwd[0].get_top(), buff=0.08, color=S.MUTED, stroke_width=2.5)
        barr = VGroup(*[Arrow(bwd[k].get_left(), bwd[k + 1].get_right(), buff=0.05, color=S.MUTED, stroke_width=2.5)
                        for k in range(2)])
        back = CurvedArrow(bwd[-1].get_left(), fwd[0].get_bottom() + DOWN * 0.05, angle=-PI / 3, color=S.PARAM,
                           stroke_width=3)
        self.play(GrowArrow(down), FadeIn(bwd[0]), run_time=self.dur(0.2))
        self.play(GrowArrow(barr[0]), FadeIn(bwd[1]), run_time=self.dur(0.15))
        self.play(GrowArrow(barr[1]), FadeIn(bwd[2]), run_time=self.dur(0.15))
        self.play(Create(back), run_time=self.dur(0.2))
        again = T("repeat", S.SMALL, S.PARAM).next_to(back, DOWN, buff=0.1)
        self.play(FadeIn(again), run_time=0.4)
        self.hold()

        self.beat("b4")
        glow = lambda m, c: SurroundingRectangle(m, color=c, buff=0.12, stroke_width=4, corner_radius=0.1)
        comp = VGroup(glow(fwd[3], S.COMPUTE), glow(fwd[5], S.COMPUTE), glow(bwd[1], S.COMPUTE))
        mem = VGroup(SurroundingRectangle(fwd[3], color=S.MEMORY, buff=0.22, stroke_width=4, corner_radius=0.1),
                     glow(bwd[2], S.MEMORY))
        comm = VGroup(Line(fwd[4].get_top() + UP * 0.35, fwd[5].get_top() + UP * 0.35, color=S.COMM, stroke_width=8),
                      Line(fwd[4].get_bottom() + DOWN * 0.35, fwd[5].get_bottom() + DOWN * 0.35, color=S.COMM,
                           stroke_width=8))
        cl = T("COMPUTE: where numbers multiply", S.SMALL, S.COMPUTE, weight="BOLD")
        ml = T("MEMORY: where numbers wait (KV cache, weights)", S.SMALL, S.MEMORY, weight="BOLD")
        vl = T("COMMUNICATION: where numbers travel (router → experts)", S.SMALL, S.COMM, weight="BOLD")
        legend = VGroup(cl, ml, vl).arrange(DOWN, buff=0.18, aligned_edge=LEFT).to_edge(DOWN, buff=0.5).to_edge(LEFT, buff=0.6)
        self.play(Create(comp), FadeIn(cl), run_time=self.dur(0.25))
        self.play(Create(mem), FadeIn(ml), run_time=self.dur(0.25))
        self.play(Create(comm), FadeIn(vl), run_time=self.dur(0.25))
        self.hold()
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.finish(tail=0.1)


class S1202TheAnswer(DocScene):
    SCENE_ID = "s1202"

    def construct(self):
        self.beat("b1")
        q = question_banner(QUESTION, S.H2)
        self.play(FadeIn(q, shift=UP * 0.2), run_time=self.dur(0.5))
        self.hold()

        self.beat("b2")
        self.play(q.animate.scale(0.7).to_edge(UP, buff=0.5), run_time=0.6)
        qs = [("Where do the numbers go?", S.COMPUTE), ("How long do they wait?", S.MEMORY),
              ("How far do they travel?", S.COMM), ("How many bits do they need?", S.PARAM)]
        grid = VGroup(*[T(t, S.BODY, c, weight="BOLD") for t, c in qs]).arrange_in_grid(2, 2, buff=(1.0, 0.7))
        grid.move_to(DOWN * 0.4)
        fit_width(grid)
        self.play(LaggedStart(*[FadeIn(g, shift=UP * 0.2) for g in grid], lag_ratio=0.5), run_time=self.dur(0.8))
        self.hold()

        self.beat("b3")
        self.play(FadeOut(VGroup(grid)), run_time=0.5)
        wall = gpu_wall(8, 16, unit=0.5, opacity=0.9).move_to(DOWN * 0.5)
        fit_width(wall)
        self.play(FadeIn(wall, lag_ratio=0.005), run_time=self.dur(0.3))
        self.play(LaggedStart(*[t.animate(rate_func=there_and_back).set_fill(S.COMPUTE, opacity=0.95) for t in wall],
                              lag_ratio=0.004), run_time=self.dur(0.4))
        tag = T("add less · waste less", S.BODY, S.TEXT, weight="BOLD").next_to(wall, DOWN, buff=0.35)
        self.play(FadeIn(tag), run_time=0.5)
        self.hold()

        self.beat("b4")
        self.play(FadeOut(VGroup(wall, tag, q)), run_time=0.5)
        chip_ = GPU("hardware", w=2.6, h=2.0, cores=(6, 8)).move_to([-3.2, 0, 0])
        eqn = VGroup(RoundedRectangle(corner_radius=0.15, width=2.8, height=2.0, stroke_color=S.TOKEN, stroke_width=2,
                                      fill_color=S.PANEL, fill_opacity=1),
                     MathTex(r"\mathrm{softmax}\!\left(\tfrac{QK^\top}{\sqrt d}\right)V", color=S.TOKEN))
        eqn[1].scale_to_fit_width(2.4).move_to(eqn[0])
        el = T("algorithms", S.SMALL, S.TOKEN, weight="BOLD").next_to(eqn[0], DOWN, buff=0.12)
        eqn.add(el)
        eqn.move_to([3.2, 0, 0])
        self.play(FadeIn(chip_), FadeIn(eqn), run_time=self.dur(0.4))
        fmt = chip("V4.1-Flash chose number formats that work across hardware platforms", S.MUTED)
        fit_width(fmt)
        fmt.to_edge(DOWN, buff=0.9)
        self.play(FadeIn(fmt), run_time=0.6)
        self.hold()

        self.beat("b5")
        self.play(FadeOut(fmt), chip_.animate.move_to([-1.35, 0, 0]), eqn.animate.move_to([1.45, 0, 0]),
                  run_time=self.dur(0.5))
        codesign = T("co-design?", S.H2, S.PARAM, weight="BOLD").to_edge(UP, buff=1.0)
        self.play(FadeIn(codesign), run_time=0.6)
        self.hold()

        self.beat("b6")
        self.play(FadeOut(VGroup(chip_, eqn, codesign)), run_time=0.8)
        t1 = T("DeepSeek Did the Impossible", S.H1, S.TEXT, weight="BOLD")
        t2 = T("The First-Principles Story of How", S.BODY, S.MUTED)
        tt = VGroup(t1, t2).arrange(DOWN, buff=0.25).move_to(UP * 0.4)
        fit_width(tt)
        srcs = T("Sources: DeepSeek-V3 Technical Report · DeepSeek-V2 · DeepSeek-V4.1-Flash (arXiv:2609.19969)\n"
                 "BIS / CSET / CSIS · NVIDIA 8-K · full claim ledger in the project repository", S.TINY, S.MUTED)
        fit_width(srcs)
        srcs.to_edge(DOWN, buff=0.6)
        self.play(FadeIn(tt, shift=UP * 0.2), run_time=1.0)
        self.play(FadeIn(srcs), run_time=0.8)
        self.hold()
        self.finish(tail=1.5)
