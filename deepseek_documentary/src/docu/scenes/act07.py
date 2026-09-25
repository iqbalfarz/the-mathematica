"""ACT 7 — The communication problem."""
import numpy as np
from manim import *  # noqa: F401,F403

from docu import style as S
from docu.base_scene import DocScene
from docu.components import (GPU, ExpertGrid, Pipe, T, Token, WallsLegend, caption, chip, fit_width, source_line)

LEG = [("compute", S.COMPUTE), ("communication", S.COMM), ("idle", S.DIM)]


def islands():
    gs = VGroup(*[GPU(f"GPU {k+1}", w=2.9, h=2.0, cores=(2, 3), core_opacity=0.06, label_size=S.TINY)
                  for k in range(4)])
    gs.arrange_in_grid(2, 2, buff=(2.2, 0.9)).move_to(DOWN * 0.1)
    experts = VGroup()
    for g in gs:
        e = ExpertGrid(12, cols=4, size=0.36, gap=0.1).move_to(g.die)
        experts.add(e)
    return gs, experts


def gantt(pattern, unit=0.42, h=0.5):
    """pattern: list of (kind, length) with kind in c/m/i."""
    col = {"c": S.COMPUTE, "m": S.COMM, "i": S.DIM}
    g = VGroup()
    for kind, n in pattern:
        r = Rectangle(width=n * unit, height=h, stroke_color=S.BG, stroke_width=2, fill_color=col[kind],
                      fill_opacity=0.9 if kind != "i" else 0.5)
        g.add(r)
    g.arrange(RIGHT, buff=0)
    return g


def legend():
    items = VGroup()
    for name, c in LEG:
        items.add(VGroup(Square(0.22, stroke_width=0, fill_color=c, fill_opacity=0.9), T(name, S.SMALL, c))
                  .arrange(RIGHT, buff=0.15))
    return items.arrange(RIGHT, buff=0.6)


class S0701Islands(DocScene):
    SCENE_ID = "s0701"

    def construct(self):
        self.beat("b1")
        gs, ex = islands()
        self.play(LaggedStart(*[FadeIn(VGroup(g, e)) for g, e in zip(gs, ex)], lag_ratio=0.25), run_time=self.dur(0.6))
        self.hold()

        self.beat("b2")
        tok = Token("token", S.TINY).next_to(gs[0].die, UP, buff=0.1)
        targets = [ex[1].cells[5], ex[2].cells[2], ex[3].cells[9]]
        names = ["expert 12", "expert 97", "expert 200"]
        self.play(FadeIn(tok, scale=1.2), run_time=0.5)
        marks = VGroup(*[SurroundingRectangle(t, color=S.EXPERT, buff=0.05, stroke_width=3) for t in targets])
        nl = VGroup(*[T(n, S.TINY, S.EXPERT).next_to(m, UP, buff=0.08) for n, m in zip(names, marks)])
        paths = VGroup(*[DashedLine(tok.get_center(), t.get_center(), color=S.COMM, dash_length=0.12) for t in targets])
        self.play(LaggedStart(*[Create(m) for m in marks], lag_ratio=0.3), FadeIn(nl), run_time=self.dur(0.35))
        self.play(Create(paths), run_time=self.dur(0.3))
        self.hold()

        self.beat("b3")
        copies = VGroup(*[Square(0.2, stroke_width=0, fill_color=S.TOKEN, fill_opacity=1).move_to(tok) for _ in targets])
        self.add(copies)
        d = T("dispatch", S.SMALL, S.COMM, weight="BOLD").to_edge(UP, buff=0.35)
        self.play(FadeIn(d), *[c.animate.move_to(t) for c, t in zip(copies, targets)], run_time=self.dur(0.3))
        self.play(*[t.animate(rate_func=there_and_back).set_fill(S.EXPERT, opacity=1) for t in targets], run_time=0.6)
        c2 = T("combine", S.SMALL, S.COMM, weight="BOLD").to_edge(UP, buff=0.35)
        self.play(ReplacementTransform(d, c2), *[c.animate.move_to(tok).set_fill(S.EXPERT) for c in copies],
                  run_time=self.dur(0.3))
        self.play(FadeOut(copies), tok.animate.set_color(S.EXPERT), run_time=0.4)
        self.hold()

        self.beat("b4")
        self.play(FadeOut(VGroup(tok, marks, nl, paths, c2)), run_time=0.4)
        web = VGroup()
        rng = np.random.default_rng(4)
        for i in range(4):
            for j in range(4):
                if i == j:
                    continue
                for _ in range(3):
                    a = gs[i].die.get_center() + rng.uniform(-0.9, 0.9, 3) * [1, 0.6, 0]
                    b = gs[j].die.get_center() + rng.uniform(-0.9, 0.9, 3) * [1, 0.6, 0]
                    web.add(Line(a, b, color=S.COMM, stroke_width=1.4, stroke_opacity=0.6))
        self.play(LaggedStart(*[Create(l) for l in web], lag_ratio=0.02), run_time=self.dur(0.5))
        lab = T("all-to-all communication", S.BODY, S.COMM, weight="BOLD")
        box = BackgroundRectangle(lab, color=S.BG, fill_opacity=0.9, buff=0.2)
        self.play(FadeIn(box), FadeIn(lab), run_time=0.6)
        self.hold()
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.finish(tail=0.1)


class S0702WaitingGPUs(DocScene):
    SCENE_ID = "s0702"

    def construct(self):
        self.beat("b1")
        lg = legend().to_edge(UP, buff=0.8)
        row = gantt([("c", 3), ("m", 1), ("i", 1), ("c", 3), ("m", 1), ("i", 1), ("c", 3), ("m", 1), ("i", 1)])
        row.move_to(UP * 0.4)
        gl = T("one GPU's time →", S.SMALL, S.MUTED).next_to(row, DOWN, buff=0.3).align_to(row, LEFT)
        self.play(FadeIn(lg), run_time=0.5)
        self.play(LaggedStart(*[GrowFromEdge(r, LEFT) for r in row], lag_ratio=0.5), FadeIn(gl),
                  run_time=self.dur(0.7))
        self.hold()

        self.beat("b2")
        row2 = gantt([("c", 3), ("m", 2), ("i", 2), ("c", 3), ("m", 2), ("i", 2), ("c", 3)])
        row2.move_to(UP * 0.4).align_to(row, LEFT)
        self.play(Transform(row, row2), run_time=self.dur(0.5))
        self.hold()

        self.beat("b3")
        h8 = T("H800: narrower links between chips", S.SMALL, S.COMM, weight="BOLD").next_to(row, DOWN, buff=0.9)
        row3 = gantt([("c", 3), ("m", 3), ("i", 2), ("c", 3), ("m", 3), ("i", 2)]).move_to(UP * 0.4).align_to(row, LEFT)
        fit_width(row3)
        self.play(FadeIn(h8), Transform(row, row3), run_time=self.dur(0.4))
        trade = T("MoE saves compute… but spends communication", S.BODY, S.TEXT).next_to(h8, DOWN, buff=0.45)
        fit_width(trade)
        self.play(FadeIn(trade), run_time=self.dur(0.2))
        self.hold()

        self.beat("b4")
        self.play(FadeOut(VGroup(row, gl, h8, trade, lg)), run_time=0.5)
        few = VGroup(*[GPU(w=1.1, h=0.8, cores=(3, 4)) for _ in range(4)]).arrange_in_grid(2, 2, buff=0.6)
        few.move_to([-2.5, 0, 0])
        self.play(FadeIn(few), run_time=0.5)
        many = VGroup(*[GPU(w=0.8, h=0.56, cores=(2, 3)) for _ in range(16)]).arrange_in_grid(4, 4, buff=0.3)
        many.move_to([-2.5, 0, 0])
        rng = np.random.default_rng(2)
        web = VGroup()
        for _ in range(90):
            i, j = rng.choice(16, 2, replace=False)
            web.add(Line(many[i].get_center(), many[j].get_center(), color=S.COMM, stroke_width=1, stroke_opacity=0.5))
        meter_bg = Rectangle(width=0.7, height=3.6, stroke_color=S.MUTED, stroke_width=1.5).move_to([3.3, 0, 0])
        meter = Rectangle(width=0.7, height=3.0, stroke_width=0, fill_color=S.COMPUTE, fill_opacity=0.85)
        meter.move_to(meter_bg, aligned_edge=DOWN)
        ml = T("time spent computing", S.SMALL, S.COMPUTE).next_to(meter_bg, DOWN, buff=0.2)
        sch = T("schematic", S.TINY, S.MUTED).next_to(meter_bg, UP, buff=0.15)
        self.play(FadeIn(meter_bg), FadeIn(meter), FadeIn(ml), FadeIn(sch), run_time=0.5)
        self.play(ReplacementTransform(few, many), Create(web),
                  meter.animate.stretch_to_fit_height(1.2).move_to(meter_bg, aligned_edge=DOWN), run_time=self.dur(0.4))
        tag = T("limited by how fast you can talk", S.BODY, S.COMM, weight="BOLD").to_edge(UP, buff=0.7)
        self.play(FadeIn(tag), run_time=0.6)
        self.hold()
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.finish(tail=0.1)


class S0703Overlap(DocScene):
    SCENE_ID = "s0703"

    def construct(self):
        self.beat("b1")
        lg = legend().to_edge(UP, buff=0.8)
        serial = gantt([("c", 3), ("m", 2), ("i", 1), ("c", 3), ("m", 2), ("i", 1), ("c", 3)]).move_to(UP * 0.8)
        sl = T("serial", S.SMALL, S.MUTED).next_to(serial, LEFT, buff=0.3)
        self.play(FadeIn(lg), FadeIn(serial), FadeIn(sl), run_time=self.dur(0.5))
        self.hold()

        self.beat("b2")
        a = gantt([("c", 3), ("c", 3), ("c", 3), ("c", 3)]).move_to(DOWN * 0.8)
        b = gantt([("m", 3), ("m", 3), ("m", 3)], h=0.3).next_to(a, DOWN, buff=0.08).align_to(a, LEFT).shift(RIGHT * 3 * 0.42)
        al = T("compute: batch A, B, A, B…", S.TINY, S.COMPUTE).next_to(a, LEFT, buff=0.3)
        bl = T("in flight meanwhile", S.TINY, S.COMM).next_to(b, LEFT, buff=0.3)
        self.play(FadeIn(a, shift=UP * 0.3), run_time=self.dur(0.25))
        self.play(FadeIn(b, shift=UP * 0.3), FadeIn(al), FadeIn(bl), run_time=self.dur(0.25))
        nogap = T("no idle gaps", S.SMALL, S.COMPUTE, weight="BOLD").next_to(b, DOWN, buff=0.4)
        self.play(FadeIn(nogap), run_time=0.5)
        self.hold()

        self.beat("b3")
        dp = T("DualPipe  (DeepSeek-V3)", S.BODY, S.TEXT, weight="BOLD").next_to(nogap, DOWN, buff=0.4)
        src = source_line("DeepSeek-V3 Technical Report §3.2")
        self.play(FadeIn(dp), FadeIn(src), run_time=self.dur(0.3))
        self.hold()

        self.beat("b4")
        self.play(FadeOut(VGroup(serial, sl, a, b, al, bl, nogap, dp, lg, src)), run_time=0.5)
        bits16 = VGroup(*[Square(0.4, stroke_color=S.TEXT, stroke_width=1.5, fill_color=S.PARAM, fill_opacity=0.5)
                          for _ in range(16)]).arrange(RIGHT, buff=0.05).move_to(UP * 1.0)
        l16 = T("16 bits per number (a common format)", S.SMALL, S.TEXT).next_to(bits16, UP, buff=0.25)
        self.play(FadeIn(bits16, lag_ratio=0.05), FadeIn(l16), run_time=self.dur(0.35))
        bits8 = VGroup(*[Square(0.4, stroke_color=S.TEXT, stroke_width=1.5, fill_color=S.PARAM, fill_opacity=0.9)
                         for _ in range(8)]).arrange(RIGHT, buff=0.05).move_to(DOWN * 0.6)
        l8 = T("FP8: 8 bits", S.BODY, S.PARAM, weight="BOLD").next_to(bits8, DOWN, buff=0.3)
        self.play(TransformFromCopy(VGroup(*bits16[:8]), bits8), FadeIn(l8), run_time=self.dur(0.35))
        self.hold()

        self.beat("b5")
        self.play(FadeOut(VGroup(bits16, l16, bits8, l8)), run_time=0.5)
        p1 = Pipe(LEFT * 5.5 + UP * 1.2, RIGHT * 5.5 + UP * 1.2, width=0.35)
        p2 = Pipe(LEFT * 5.5 + DOWN * 1.0, RIGHT * 5.5 + DOWN * 1.0, width=0.35)
        t1 = T("16-bit numbers", S.SMALL, S.TEXT).next_to(p1, UP, buff=0.35)
        t2 = T("8-bit numbers: twice as many through the same pipe", S.SMALL, S.PARAM).next_to(p2, UP, buff=0.35)
        self.play(FadeIn(p1), FadeIn(p2), FadeIn(t1), FadeIn(t2), run_time=0.5)
        d1 = VGroup(*[Square(0.24, stroke_width=0, fill_color=S.PARAM, fill_opacity=0.9).move_to(p1.start) for _ in range(8)])
        d2 = VGroup(*[Square(0.17, stroke_width=0, fill_color=S.PARAM, fill_opacity=0.9).move_to(p2.start) for _ in range(16)])
        self.add(d1, d2)
        self.play(LaggedStart(*[d.animate(rate_func=linear).move_to(p1.end) for d in d1], lag_ratio=0.25),
                  LaggedStart(*[d.animate(rate_func=linear).move_to(p2.end) for d in d2], lag_ratio=0.125),
                  run_time=self.dur(0.7))
        self.remove(d1, d2)
        src = source_line("DeepSeek-V3: FP8 mixed-precision training (official README)")
        self.play(FadeIn(src), run_time=0.4)
        self.hold()

        self.beat("b6")
        self.play(FadeOut(VGroup(p1, p2, t1, t2, src)), run_time=0.5)
        leg = WallsLegend().move_to(ORIGIN).scale(1.8)
        self.play(FadeIn(leg), run_time=0.6)
        ticks = VGroup(*[T("✓", S.H2, c, weight="BOLD").next_to(leg.item(n), UP, buff=0.25)
                         for n, c in (("COMPUTE", S.COMPUTE), ("COMMUNICATION", S.COMM))])
        self.play(LaggedStart(*[FadeIn(t, scale=1.5) for t in ticks], lag_ratio=0.4), run_time=self.dur(0.4))
        msg = T("not more hardware: a better understanding of where the time goes", S.SMALL, S.TEXT)
        fit_width(msg)
        msg.next_to(leg, DOWN, buff=0.8)
        self.play(FadeIn(msg), run_time=0.6)
        self.hold()
        self.play(FadeOut(VGroup(ticks, msg)), leg.animate.scale(1 / 1.8).move_to(WallsLegend().get_center()),
                  run_time=0.8)
        self.finish(tail=0.1)
