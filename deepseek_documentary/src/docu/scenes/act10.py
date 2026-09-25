"""ACT 10 — How a model learns: loss, gradients, the loop, and V3's training numbers."""
import numpy as np
from manim import *  # noqa: F401,F403

from docu import style as S
from docu.base_scene import DocScene
from docu.components import (LayerTower, M, T, TokenRow, WallsLegend, chip, fit_width, prob_bars, source_line)


class S1001Loss(DocScene):
    SCENE_ID = "s1001"

    def construct(self):
        self.beat("b1")
        tower = LayerTower(n=12, w=3.0, h=0.18, gap=0.08).move_to([-3.6, 0, 0])
        rng = np.random.default_rng(0)
        nums = VGroup(*[T(f"{v:+.2f}", S.TINY, S.PARAM, mono=True) for v in rng.normal(0, 0.5, 12)])
        nums.arrange_in_grid(4, 3, buff=(0.4, 0.3)).move_to([2.6, 0.3, 0])
        wl = T("weights start as random numbers", S.SMALL, S.MUTED).next_to(nums, DOWN, buff=0.4)
        self.play(FadeIn(tower), FadeIn(nums, lag_ratio=0.05), run_time=self.dur(0.4))
        self.play(FadeIn(wl), run_time=0.5)
        self.hold()

        self.beat("b2")
        self.play(FadeOut(VGroup(nums, wl)), tower.animate.move_to([-4.6, 0, 0]).scale(0.8), run_time=0.5)
        prompt = TokenRow(["the", "cat", "sat", "on", "the"], size=S.SMALL).move_to([1.2, 2.6, 0])
        self.play(FadeIn(prompt), run_time=0.5)
        cands = ["moon", "idea", "mat", "piano", "cheese", "roof"]
        ps = [0.03, 0.02, 0.02, 0.03, 0.04, 0.03]
        bars = prob_bars(cands, ps, color=S.TOKEN, max_h=6.0).move_to([1.2, -0.4, 0])
        bl = T("random model: nearly flat guesses", S.SMALL, S.MUTED).next_to(bars, DOWN, buff=0.35)
        self.play(FadeIn(bars, lag_ratio=0.1), FadeIn(bl), run_time=self.dur(0.4))
        self.hold()

        self.beat("b3")
        tgt = SurroundingRectangle(bars[2], color=S.EXPERT, buff=0.08)
        tl = T("right answer", S.SMALL, S.EXPERT).next_to(tgt, UP, buff=0.1)
        self.play(Create(tgt), FadeIn(tl), run_time=0.6)
        f = M(r"L = -\log p(\text{mat}) = -\log 0.02 \approx 3.9", 44, S.LOSS).to_edge(UP, buff=0.4).shift(RIGHT * 1.2)
        fit_width(f, 9.0)
        self.play(FadeOut(prompt), Write(f), run_time=self.dur(0.45))
        lname = T("the loss", S.SMALL, S.LOSS).next_to(f, DOWN, buff=0.15)
        self.play(FadeIn(lname), run_time=0.4)
        self.hold()

        self.beat("b4")
        self.play(FadeOut(VGroup(bars, bl, tgt, tl, tower, lname)), f.animate.scale(0.8).to_edge(UP, buff=0.4),
                  run_time=0.5)
        ax = Axes(x_range=[0, 1, 0.25], y_range=[0, 5, 1], x_length=7.5, y_length=4.2,
                  axis_config={"color": S.MUTED, "include_ticks": False}).move_to(DOWN * 0.5)
        xl = T("probability given to the right answer", S.SMALL, S.MUTED).next_to(ax, DOWN, buff=0.25)
        yl = T("loss", S.SMALL, S.LOSS).next_to(ax, LEFT, buff=0.25)
        curve = ax.plot(lambda p: -np.log(p), x_range=[0.007, 1], color=S.LOSS, stroke_width=5)
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), Create(curve), run_time=self.dur(0.3))
        t = ValueTracker(0.02)
        dot = always_redraw(lambda: Dot(ax.c2p(t.get_value(), -np.log(t.get_value())), color=S.TEXT, radius=0.1))
        self.add(dot)
        self.play(t.animate.set_value(0.97), run_time=self.dur(0.4))
        goal = T("goal: make this number smaller", S.BODY, S.TEXT, weight="BOLD").move_to([2.0, 1.2, 0])
        self.play(FadeIn(goal), run_time=0.6)
        self.hold()
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.finish(tail=0.1)


def loss_fn(w):
    return 0.35 * (w - 1.2) ** 2 + 0.35 * np.sin(1.6 * w) + 1.2


def dloss(w):
    return 0.7 * (w - 1.2) + 0.56 * np.cos(1.6 * w)


class S1002GradientDescent(DocScene):
    SCENE_ID = "s1002"

    def construct(self):
        self.beat("b1")
        ax = Axes(x_range=[-3, 4, 1], y_range=[0, 6, 1], x_length=9, y_length=4.6,
                  axis_config={"color": S.MUTED, "include_ticks": False}).move_to(DOWN * 0.4)
        xl = T("one weight  w", S.SMALL, S.PARAM).next_to(ax, DOWN, buff=0.25)
        yl = T("loss", S.SMALL, S.LOSS).next_to(ax, LEFT, buff=0.2)
        curve = ax.plot(loss_fn, x_range=[-3, 4], color=S.LOSS, stroke_width=5)
        w = ValueTracker(-2.3)
        ball = always_redraw(lambda: Dot(ax.c2p(w.get_value(), loss_fn(w.get_value())), radius=0.14, color=S.PARAM))
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), Create(curve), run_time=self.dur(0.5))
        self.add(ball)
        self.hold()

        self.beat("b2")
        def tangent():
            x0 = w.get_value()
            y0 = loss_fn(x0)
            d = dloss(x0)
            return Line(ax.c2p(x0 - 0.8, y0 - 0.8 * d), ax.c2p(x0 + 0.8, y0 + 0.8 * d), color=S.GRAD, stroke_width=3)
        tan = always_redraw(tangent)
        def garrow():
            x0 = w.get_value()
            d = dloss(x0)
            step = -np.sign(d) * 0.9
            return Arrow(ax.c2p(x0, loss_fn(x0)) + UP * 0.35, ax.c2p(x0 + step, loss_fn(x0)) + UP * 0.35, buff=0,
                         color=S.GRAD, stroke_width=4)
        ga = always_redraw(garrow)
        gl = T("gradient = slope", S.SMALL, S.GRAD).to_edge(UP, buff=0.7)
        self.play(Create(tan), run_time=self.dur(0.3))
        self.play(FadeIn(ga), FadeIn(gl), run_time=self.dur(0.3))
        self.hold()

        self.beat("b3")
        f = M(r"w \leftarrow w - \eta\, \nabla L", 48, S.TEXT).next_to(gl, DOWN, buff=0.25)
        self.play(Write(f), run_time=0.8)
        eta = 0.6
        steps = 7
        for _ in range(steps):
            nw = w.get_value() - eta * dloss(w.get_value())
            self.play(w.animate.set_value(nw), run_time=self.dur(0.07, lo=0.35))
        self.hold()

        self.beat("b4")
        self.play(FadeOut(VGroup(ax, xl, yl, curve, f, gl)), FadeOut(tan), FadeOut(ga), FadeOut(ball), run_time=0.5)
        ells = VGroup(*[Ellipse(width=1.2 * k, height=0.75 * k, color=S.LOSS, stroke_width=2,
                                stroke_opacity=1 - 0.1 * k) for k in range(1, 8)]).move_to([-2.4, -0.2, 0])
        path_pts = [[-5.6, 1.9, 0], [-4.4, 1.2, 0], [-3.6, 0.6, 0], [-3.0, 0.2, 0], [-2.6, 0.0, 0], [-2.4, -0.2, 0]]
        path = VMobject(color=S.PARAM, stroke_width=4).set_points_smoothly(path_pts)
        ml = T("billions of dimensions (2 shown)", S.SMALL, S.MUTED).next_to(ells, DOWN, buff=0.3)
        self.play(Create(ells, lag_ratio=0.1), FadeIn(ml), run_time=self.dur(0.25))
        self.play(Create(path), run_time=self.dur(0.2))
        tower = LayerTower(n=10, w=2.6, h=0.2, gap=0.1).move_to([3.6, -0.1, 0])
        arrs = VGroup(*[Arrow(s.get_right() + RIGHT * 0.5, s.get_right() + RIGHT * 0.05 + DOWN * 0.0, buff=0,
                              color=S.GRAD, stroke_width=3, max_tip_length_to_length_ratio=0.3)
                        for s in tower.slabs[::-1]])
        bp = T("backpropagation: gradients flow backwards", S.SMALL, S.GRAD).next_to(tower, UP, buff=0.3)
        self.play(FadeIn(tower), FadeIn(bp), run_time=0.5)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrs], lag_ratio=0.12), run_time=self.dur(0.3))
        self.hold()

        self.beat("b5")
        self.play(FadeOut(VGroup(ells, path, ml, tower, arrs, bp)), run_time=0.5)
        fw = VGroup(Arrow(LEFT * 2.5, RIGHT * 2.5, color=S.COMPUTE, stroke_width=6), T("forward ≈ 2", S.BODY, S.COMPUTE))
        bw = VGroup(Arrow(RIGHT * 2.5, LEFT * 2.5, color=S.GRAD, stroke_width=6), T("backward ≈ 4", S.BODY, S.GRAD))
        for g in (fw, bw):
            g[1].next_to(g[0], UP, buff=0.15)
        VGroup(fw, bw).arrange(DOWN, buff=0.6).move_to(UP * 0.7)
        tot = M(r"\text{training FLOPs} \approx 6 \times \text{active parameters} \times \text{tokens}", 40)
        fit_width(tot)
        tot.next_to(VGroup(fw, bw), DOWN, buff=0.6)
        rt = T("rule of thumb", S.TINY, S.MUTED).next_to(tot, DOWN, buff=0.2)
        self.play(FadeIn(fw), run_time=0.5)
        self.play(FadeIn(bw), run_time=self.dur(0.25))
        self.play(Write(tot), FadeIn(rt), run_time=self.dur(0.4))
        self.hold()
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.finish(tail=0.1)


LOOP = [("BATCH", S.TOKEN), ("FORWARD", S.COMPUTE), ("LOSS", S.LOSS), ("BACKWARD", S.GRAD), ("UPDATE", S.PARAM)]


def loop_nodes(r=2.3, center=(0, 0, 0)):
    nodes = VGroup()
    for k, (n, c) in enumerate(LOOP):
        a = PI / 2 - k * TAU / 5
        box = RoundedRectangle(corner_radius=0.12, width=2.2, height=0.75, stroke_color=c, stroke_width=2,
                               fill_color=c, fill_opacity=0.14)
        nodes.add(VGroup(box, T(n, S.SMALL, c, weight="BOLD").move_to(box)).move_to(
            np.array(center) + [r * 1.25 * np.cos(a), r * np.sin(a), 0]))
    arrows = VGroup(*[Arrow(nodes[k].get_center(), nodes[(k + 1) % 5].get_center(), buff=0.55, color=S.MUTED,
                            stroke_width=2.5) for k in range(5)])
    return nodes, arrows


class S1003TheLoop(DocScene):
    SCENE_ID = "s1003"

    def construct(self):
        self.beat("b1")
        nodes, arrows = loop_nodes(center=(-2.6, -0.2, 0))
        for k in range(5):
            self.play(FadeIn(nodes[k], scale=0.9), GrowArrow(arrows[k]), run_time=self.dur(0.12, lo=0.4))
        self.play(LaggedStart(*[n[0].animate(rate_func=there_and_back).set_fill(opacity=0.6) for n in nodes],
                              lag_ratio=0.3), run_time=self.dur(0.25))
        self.hold()

        self.beat("b2")
        card = VGroup(T("100.6M", S.H2, S.TOKEN, weight="BOLD", mono=True), T("tokens per step", S.SMALL, S.TEXT),
                      T("DeepSeek-V4.1-Flash", S.TINY, S.MUTED)).arrange(DOWN, buff=0.12).move_to([4.0, 1.4, 0])
        self.play(Indicate(nodes[0], color=S.TOKEN), FadeIn(card, shift=LEFT * 0.2), run_time=self.dur(0.5))
        self.hold()

        self.beat("b3")
        tot = VGroup(T("45T tokens total", S.BODY, S.TEXT), T("÷ 100.6M per step", S.BODY, S.TEXT))
        tot.arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to([4.0, -0.6, 0])
        steps = Integer(0, font_size=64, color=S.PARAM, group_with_commas=True).move_to([4.0, -2.2, 0])
        sl = T("≈ steps (our arithmetic)", S.TINY, S.MUTED).next_to(steps, DOWN, buff=0.15)
        self.play(FadeIn(tot), run_time=self.dur(0.3))
        self.play(FadeIn(steps), FadeIn(sl), run_time=0.3)
        cycle = [n[0].animate(rate_func=there_and_back).set_fill(opacity=0.7) for _ in range(3) for n in nodes]
        self.play(ChangeDecimalToValue(steps, 447316), LaggedStart(*cycle, lag_ratio=0.35), run_time=self.dur(0.45))
        self.hold()

        self.beat("b4")
        self.play(FadeOut(VGroup(card, tot, steps, sl)), run_time=0.4)
        leg = WallsLegend().scale(1.5).move_to([3.6, 0.2, 0])
        leg.items.arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to([3.8, 0.2, 0])
        self.play(FadeIn(leg), run_time=0.5)
        for it in leg.items:
            self.play(it.animate(rate_func=there_and_back).scale(1.3), run_time=self.dur(0.15, lo=0.5))
        self.hold()
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.finish(tail=0.1)


class S1004TrainingV3(DocScene):
    SCENE_ID = "s1004"

    def construct(self):
        self.beat("b1")
        title = T("DeepSeek-V3 training", S.H2, S.TEXT, weight="BOLD").to_edge(UP, buff=0.6)
        rep = chip("reported by DeepSeek, unless marked", S.MUTED).next_to(title, DOWN, buff=0.2)
        self.play(FadeIn(title), FadeIn(rep), run_time=self.dur(0.5))
        self.hold()

        self.beat("b2")
        facts = VGroup(T("37B active parameters", S.BODY, S.EXPERT), T("14.8T tokens", S.BODY, S.TOKEN)).arrange(
            RIGHT, buff=1.2).next_to(rep, DOWN, buff=0.5)
        self.play(FadeIn(facts, lag_ratio=0.4), run_time=self.dur(0.3))
        f = M(r"6 \times 37{\times}10^{9} \times 14.8{\times}10^{12} \;\approx\; 3.3 \times 10^{24} \text{ FLOPs}", 42,
              S.COMPUTE).next_to(facts, DOWN, buff=0.5)
        fit_width(f)
        est = chip("our estimate, not DeepSeek's figure", S.PARAM).next_to(f, DOWN, buff=0.3)
        self.play(Write(f), run_time=self.dur(0.35))
        self.play(FadeIn(est), run_time=0.5)
        self.hold()

        self.beat("b3")
        self.play(FadeOut(VGroup(f, est)), run_time=0.4)
        row = VGroup(T("180K", S.H2, S.PARAM, weight="BOLD", mono=True), T("H800 GPU-hours per trillion tokens", S.BODY,
                                                                             S.TEXT)).arrange(RIGHT, buff=0.3)
        row2 = T("≈ 3.7 days on 2,048 H800s", S.BODY, S.COMPUTE)
        VGroup(row, row2).arrange(DOWN, buff=0.3).next_to(facts, DOWN, buff=0.6)
        fit_width(row)
        self.play(FadeIn(row, shift=UP * 0.2), run_time=self.dur(0.4))
        self.play(FadeIn(row2), run_time=self.dur(0.25))
        self.hold()

        self.beat("b4")
        self.play(FadeOut(VGroup(row, row2)), run_time=0.4)
        total = 2788.0
        L = 11.0
        segs = [("pre-training", 2664, S.COMPUTE), ("context extension", 119, S.MEMORY), ("post-training", 5, S.EXPERT)]
        bar = VGroup(*[Rectangle(width=max(0.03, L * v / total), height=0.7, stroke_width=0, fill_color=c,
                                 fill_opacity=0.9) for _, v, c in segs]).arrange(RIGHT, buff=0).move_to(DOWN * 0.6)
        labs = VGroup(T("pre-training 2.664M", S.SMALL, S.COMPUTE).next_to(bar[0], DOWN, buff=0.2),
                      T("+ context extension 119K + post-training 5K", S.SMALL, S.MEMORY))
        labs[1].next_to(bar, DOWN, buff=0.7).align_to(bar, RIGHT)
        tot = T("= 2.788M H800 GPU-hours", S.H2, S.TEXT, weight="BOLD").next_to(labs, DOWN, buff=0.35)
        self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in bar], lag_ratio=0.5), run_time=self.dur(0.35))
        self.play(FadeIn(labs), run_time=0.5)
        self.play(FadeIn(tot, shift=UP * 0.2), run_time=self.dur(0.25))
        src = source_line("DeepSeek-V3 Technical Report (arXiv:2412.19437), Table 1; official README")
        self.add(src)
        self.hold()
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.finish(tail=0.1)
