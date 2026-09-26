"""ACT 5 — The computational explosion."""
import numpy as np
from manim import *  # noqa: F401,F403

from docu import style as S
from docu.base_scene import DocScene
from docu.components import (LayerTower, T, Token, TokenRow, chip, fit_width, question_banner)

REGIONS = ["poetry", "history", "code", "biology", "maths", "French", "law", "music"]


def region_model(w=6.4, h=3.4):
    frame = RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=S.PARAM, stroke_width=2,
                             fill_color=S.PARAM, fill_opacity=0.05)
    boxes = VGroup()
    for name in REGIONS:
        b = RoundedRectangle(corner_radius=0.1, width=1.35, height=1.2, stroke_color=S.PARAM, stroke_width=1.5,
                             fill_color=S.PARAM, fill_opacity=0.12)
        t = T(name, S.SMALL, S.TEXT).move_to(b)
        boxes.add(VGroup(b, t))
    boxes.arrange_in_grid(2, 4, buff=0.2).move_to(frame)
    return VGroup(frame, boxes)


class S0501Scaling(DocScene):
    SCENE_ID = "s0501"

    def construct(self):
        self.beat("b1")
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 10, 1], x_length=8, y_length=4.4,
                  axis_config={"color": S.MUTED, "include_ticks": False}).move_to(DOWN * 0.2)
        xl = T("scale: parameters · data · compute", S.SMALL, S.MUTED).next_to(ax, DOWN, buff=0.25)
        yl = T("capability", S.SMALL, S.MUTED).rotate(PI / 2).next_to(ax, LEFT, buff=0.25)
        curve = ax.plot(lambda x: 9 * (1 - np.exp(-0.28 * x)) + 0.3, x_range=[0, 10], color=S.TOKEN, stroke_width=5)
        tag = chip("schematic", S.MUTED).next_to(ax, UP, buff=0.1).align_to(ax, RIGHT)
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(tag), run_time=self.dur(0.3))
        self.play(Create(curve), run_time=self.dur(0.5))
        self.hold()

        self.beat("b2")
        self.play(FadeOut(VGroup(ax, xl, yl, curve, tag)), run_time=0.5)
        tower = LayerTower(n=8, w=1.6, h=0.16, gap=0.06).move_to(DOWN * 0.3)
        self.play(FadeIn(tower), run_time=0.4)
        big = LayerTower(n=22, w=4.4, h=0.14, gap=0.05).move_to(DOWN * 0.2)
        pl = T("parameters", S.SMALL, S.PARAM).next_to(big, RIGHT, buff=0.5)
        arr = Arrow(pl.get_bottom() + DOWN * 0.4, pl.get_top() + UP * 1.4, color=S.PARAM, buff=0).next_to(pl, RIGHT)
        self.play(Transform(tower, big), FadeIn(pl), GrowArrow(arr), run_time=self.dur(0.6))
        self.hold()

        self.beat("b3")
        rule = T("≈ 2 FLOPs × parameters × tokens", S.SMALL, S.COMPUTE).to_edge(UP, buff=0.8)
        tok = Token("token", S.SMALL).next_to(tower, DOWN, buff=0.3)
        self.play(FadeIn(rule), FadeIn(tok), run_time=0.6)
        slabs = tower.slabs
        self.play(tok.animate.move_to(tower.get_top() + UP * 0.45),
                  LaggedStart(*[s.animate.set_fill(S.COMPUTE, opacity=0.85) for s in slabs], lag_ratio=0.12),
                  run_time=self.dur(0.55))
        every = T("every weight, every token", S.SMALL, S.TEXT, weight="BOLD").next_to(tower, LEFT, buff=0.5)
        self.play(FadeIn(every), run_time=0.6)
        self.hold()

        self.beat("b4")
        self.play(FadeOut(VGroup(rule, tok, every, pl, arr)), run_time=0.4)
        small = LayerTower(n=10, w=1.6, h=0.14, gap=0.05).move_to([-2.6, 0.6, 0])
        large = LayerTower(n=20, w=3.2, h=0.14, gap=0.05).move_to([2.4, 0.6, 0])
        self.play(ReplacementTransform(tower, VGroup(small, large)), run_time=0.8)
        m1 = Rectangle(width=0.6, height=0.8, stroke_width=0, fill_color=S.COMPUTE, fill_opacity=0.85)
        m2 = Rectangle(width=0.6, height=1.6, stroke_width=0, fill_color=S.COMPUTE, fill_opacity=0.85)
        m1.next_to(small, DOWN, buff=0.4).align_to([0, -3.0, 0], DOWN)
        m2.next_to(large, DOWN, buff=0.4).align_to([0, -3.0, 0], DOWN)
        m1.set_x(small.get_x() + 1.4)
        m2.set_x(large.get_x() + 2.2)
        c1 = T("cost / token", S.TINY, S.COMPUTE).next_to(m1, LEFT, buff=0.2)
        c2 = T("× 2", S.BODY, S.COMPUTE, weight="BOLD").next_to(m2, LEFT, buff=0.2)
        self.play(GrowFromEdge(m1, DOWN), FadeIn(c1), run_time=0.5)
        self.play(GrowFromEdge(m2, DOWN), FadeIn(c2), run_time=self.dur(0.3))
        forever = T("for every word, for every user", S.SMALL, S.TEXT).to_edge(UP, buff=0.8)
        self.play(FadeIn(forever), run_time=0.6)
        self.hold()
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.finish(tail=0.1)


class S0502DoWeNeedAll(DocScene):
    SCENE_ID = "s0502"

    def construct(self):
        self.beat("b1")
        model = region_model().move_to(DOWN * 0.3)
        inp = TokenRow(["2", "+", "2", "="], size=S.BODY).next_to(model, UP, buff=0.5)
        self.play(FadeIn(model[0]), FadeIn(model[1]), run_time=0.6)
        self.play(FadeIn(inp, shift=DOWN * 0.3), run_time=self.dur(0.4))
        self.play(inp.animate.scale(0.6).move_to(model[0].get_top() + DOWN * 0.1).set_opacity(0.0),
                  run_time=self.dur(0.3))
        self.hold()

        self.beat("b2")
        self.play(LaggedStart(*[b[0].animate.set_fill(S.COMPUTE, opacity=0.7) for b in model[1]], lag_ratio=0.12),
                  run_time=self.dur(0.6))
        lbl = T("all of it fires", S.SMALL, S.COMPUTE).next_to(model, DOWN, buff=0.3)
        self.play(FadeIn(lbl), run_time=0.5)
        self.hold()

        self.beat("b3")
        maths = model[1][4]
        self.play(*[b[0].animate.set_fill(S.PARAM, opacity=0.06) for b in model[1] if b is not maths],
                  *[b[1].animate.set_opacity(0.35) for b in model[1] if b is not maths],
                  FadeOut(lbl), run_time=self.dur(0.5))
        need = T("what 2 + 2 actually needs", S.SMALL, S.COMPUTE).next_to(model, DOWN, buff=0.3)
        self.play(FadeIn(need), run_time=0.5)
        self.hold()

        self.beat("b4")
        self.play(FadeOut(need), model.animate.set_opacity(0.18).scale(0.72).move_to(DOWN * 1.5), run_time=0.6)
        q = question_banner("What if a model didn't need all of itself, every time?", S.H2).to_edge(UP, buff=1.0)
        self.play(AddTextLetterByLetter(q[0]), run_time=self.dur(0.45, hi=3.0))
        self.play(GrowFromCenter(q[1]), model[1].animate.arrange_in_grid(2, 4, buff=0.4).move_to(DOWN * 1.5),
                  run_time=self.dur(0.3))
        self.hold()
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.finish(tail=0.1)
