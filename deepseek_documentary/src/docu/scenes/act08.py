"""ACT 8 — The memory wall: KV cache and Multi-head Latent Attention."""
import numpy as np
from manim import *  # noqa: F401,F403

from docu import style as S
from docu.base_scene import DocScene
from docu.components import (GPU, KVShelf, KVSlot, M, T, Token, TokenRow, WallsLegend, attention_arcs, bar_pair,
                             caption, chip, fit_width, question_banner, safe_right, safe_top, source_line)

GEN = ["The", "cat", "sat", "on", "the", "warm", "mat"]


def dial(name, value=1.0, color=S.MEMORY, r=0.9):
    c = Circle(r, color=color, stroke_width=3)
    ticks = VGroup(*[Line(c.point_at_angle(a) * 0.86 + c.get_center() * 0.14, c.point_at_angle(a), color=S.MUTED,
                          stroke_width=2) for a in np.linspace(-PI / 4, 5 * PI / 4, 7)])
    needle = Line(c.get_center(), c.get_center() + r * 0.8 * np.array([np.cos(PI * (1.25 - 1.5 * value)),
                                                                      np.sin(PI * (1.25 - 1.5 * value)), 0]),
                  color=color, stroke_width=5)
    hub = Dot(c.get_center(), color=color, radius=0.07)
    lab = T(name, S.SMALL, color, weight="BOLD").next_to(c, DOWN, buff=0.25)
    g = VGroup(c, ticks, needle, hub, lab)
    g.needle = needle
    g.center_pt = c.get_center()
    return g


class S0801WritingOneToken(DocScene):
    SCENE_ID = "s0801"

    def construct(self):
        leg = WallsLegend()
        self.add(leg)
        self.beat("b1")
        big = T("MEMORY", 110, S.MEMORY, weight="BOLD")
        self.play(ReplacementTransform(leg.item("MEMORY").copy(), big), run_time=self.dur(0.4))
        self.hold()

        self.beat("b2")
        self.play(FadeOut(big), run_time=0.4)
        row = TokenRow(GEN[:6], size=S.BODY, buff=0.25).move_to(UP * 1.2)
        self.play(FadeIn(row, lag_ratio=0.1), run_time=0.6)
        new = Token(GEN[6], S.BODY).next_to(row, RIGHT, buff=0.25)
        self.play(FadeIn(new, scale=1.3), run_time=0.5)
        w = np.array([0.05, 0.3, 0.25, 0.1, 0.05, 0.25])
        arcs = attention_arcs(new, list(row), w / w.max(), max_width=8)
        self.play(LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.1), run_time=self.dur(0.4))
        self.hold()

        self.beat("b3")
        slots = VGroup(*[KVSlot(0.42, 0.62).next_to(t, DOWN, buff=0.35) for t in row])
        kv = VGroup(M("K", 30, S.KCOL), M("V", 30, S.VCOL)).arrange(DOWN, buff=0.14).next_to(slots, LEFT, buff=0.3)
        self.play(FadeOut(arcs), LaggedStart(*[FadeIn(s, shift=DOWN * 0.1) for s in slots], lag_ratio=0.1),
                  FadeIn(kv), run_time=self.dur(0.35))
        frozen = T("these never change", S.SMALL, S.MUTED).next_to(slots, DOWN, buff=0.35)
        self.play(FadeIn(frozen), run_time=0.5)
        self.hold()

        self.beat("b4")
        shelf = KVShelf(n=6, slot_w=0.42, slot_h=0.62, gap=0.33).move_to(DOWN * 1.6)
        shelf.slots.align_to(row[0], LEFT)
        shelf.base.align_to(shelf.slots, LEFT).shift(LEFT * 0.15)
        shelf.label.next_to(shelf.base, DOWN, buff=0.14)
        self.play(FadeOut(frozen), FadeOut(kv), *[ReplacementTransform(a, b) for a, b in zip(slots, shelf.slots)],
                  FadeIn(shelf.base), FadeIn(shelf.label), run_time=self.dur(0.35))
        for k in range(2):
            s = KVSlot(0.42, 0.62).next_to(shelf.slots, RIGHT, buff=0.33)
            ext = shelf.base.copy().stretch_to_fit_width(shelf.base.width + 0.75).align_to(shelf.base, LEFT)
            self.play(FadeIn(s, shift=DOWN * 0.3), Transform(shelf.base, ext), run_time=self.dur(0.12, lo=0.5))
            shelf.slots.add(s)
        grows = T("+1 entry per token", S.SMALL, S.MEMORY).next_to(shelf.base, RIGHT, buff=0.3)
        self.play(FadeIn(grows), run_time=0.5)
        self.hold()
        self.play(FadeOut(Group(*[m for m in self.mobjects if m is not leg])), run_time=0.6)
        self.finish(tail=0.1)


class S0802CacheGrowth(DocScene):
    SCENE_ID = "s0802"

    def construct(self):
        leg = WallsLegend()
        self.add(leg)
        self.beat("b1")
        f = M(r"\text{bytes per token} = 2 \times \text{layers} \times \text{heads} \times \text{head dim} \times \text{bytes per number}", 34)
        fit_width(f)
        f.move_to(UP * 2.2)
        lab = VGroup(T("2 = one key + one value", S.TINY, S.MUTED)).next_to(f, DOWN, buff=0.25)
        self.play(Write(f), FadeIn(lab), run_time=self.dur(0.6))
        self.hold()

        self.beat("b2")
        g = M(r"2 \times 61 \times 128 \times 128 \times 2 \text{ bytes} \;\approx\; 4.0\text{ MB}", 44, S.MEMORY)
        g.next_to(lab, DOWN, buff=0.5)
        tag = chip("hypothetical · our arithmetic from V3's published shape", S.MUTED).next_to(g, DOWN, buff=0.35)
        self.play(Write(g), run_time=self.dur(0.45))
        self.play(FadeIn(tag), run_time=0.5)
        self.hold()

        self.beat("b3")
        self.play(FadeOut(VGroup(f, lab)), VGroup(g, tag).animate.scale(0.75).to_edge(UP, buff=0.45), run_time=0.6)
        unit = 5.0 / 560  # height per GB
        base_y = -2.8
        lines = VGroup()
        for k in range(1, 7):
            y = base_y + 80 * k * unit
            lines.add(VGroup(DashedLine([-1.8, y, 0], [1.8, y, 0], color=S.MUTED, stroke_width=1.2),
                             T(f"{80*k} GB", S.TINY, S.MUTED).move_to([-2.6, y, 0])))
        bar = Rectangle(width=1.4, height=524 * unit, stroke_width=0, fill_color=S.MEMORY, fill_opacity=0.85)
        bar.move_to([0, base_y, 0], aligned_edge=DOWN)
        gl = T("one GPU = 80 GB", S.TINY, S.MUTED).move_to([2.9, base_y + 80 * unit, 0])
        top = T("128K tokens ≈ 524 GB", S.BODY, S.MEMORY, weight="BOLD").move_to([4.3, base_y + 524 * unit - 0.3, 0])
        self.play(FadeIn(lines), FadeIn(gl), run_time=0.5)
        self.play(GrowFromEdge(bar, DOWN), run_time=self.dur(0.5))
        self.play(FadeIn(top), run_time=0.5)
        one = T("for one conversation", S.SMALL, S.TEXT).next_to(top, DOWN, buff=0.2)
        self.play(FadeIn(one), run_time=0.5)
        self.hold()

        self.beat("b4")
        self.play(FadeOut(VGroup(lines, bar, gl, top, one, g, tag)), run_time=0.5)
        box = RoundedRectangle(corner_radius=0.15, width=6.0, height=3.4, stroke_color=S.MEMORY, stroke_width=3)
        box.move_to(DOWN * 0.2)
        bl = T("one GPU's memory", S.SMALL, S.MEMORY).next_to(box, DOWN, buff=0.2)
        weights = Rectangle(width=5.6, height=1.0, stroke_width=0, fill_color=S.PARAM, fill_opacity=0.6)
        weights.move_to(box.get_bottom() + UP * 0.7)
        wl = T("weights (shared by everyone)", S.SMALL, S.TEXT).move_to(weights)
        self.play(Create(box), FadeIn(bl), FadeIn(weights), FadeIn(wl), run_time=0.6)
        shelves = VGroup()
        for k in range(5):
            s = KVShelf(n=6, slot_w=0.18, slot_h=0.3, gap=0.05, label=False)
            u = T(f"user {k+1}", S.TINY, S.MUTED).next_to(s, UP, buff=0.05)
            shelves.add(VGroup(s, u))
        shelves.arrange(RIGHT, buff=0.35).to_edge(UP, buff=0.6)
        fit_width(shelves)
        self.play(FadeIn(shelves, lag_ratio=0.2), run_time=self.dur(0.3))
        targets = [box.get_center() + UP * 0.7 + RIGHT * x for x in (-2.0, -0.5, 1.0, 2.4, 3.8)]
        self.play(*[s.animate.move_to(t) for s, t in zip(shelves, targets)], run_time=self.dur(0.35))
        over = T("doesn't fit", S.BODY, S.LOSS, weight="BOLD").next_to(box, RIGHT, buff=0.3).shift(DOWN * 0.6)
        over.set_x(min(over.get_x(), safe_right() - over.width / 2))
        self.play(box.animate.set_stroke(S.LOSS), FadeIn(over), run_time=0.6)
        self.hold()

        self.beat("b5")
        self.play(FadeOut(VGroup(box, bl, weights, wl, shelves, over)), run_time=0.5)
        q = question_banner("How small can a memory of the past be?", S.H2)
        self.play(AddTextLetterByLetter(q[0]), run_time=self.dur(0.5, hi=2.6))
        self.play(GrowFromCenter(q[1]), run_time=0.4)
        self.hold()
        small = T("How small can the memory be?", S.SMALL, S.MEMORY, weight="BOLD")
        small.move_to([safe_right() - small.width / 2, safe_top() - small.height / 2, 0])
        self.play(ReplacementTransform(q, small), run_time=0.8)
        self.finish(tail=0.2)


class S0803LatentAttention(DocScene):
    SCENE_ID = "s0803"

    def construct(self):
        leg = WallsLegend()
        self.add(leg)
        self.beat("b1")
        title = T("Multi-head Latent Attention (MLA)", S.H2, S.MEMORY, weight="BOLD").to_edge(UP, buff=0.6)
        sub = T("introduced in DeepSeek-V2", S.SMALL, S.MUTED).next_to(title, DOWN, buff=0.15)
        self.play(FadeIn(title), FadeIn(sub), run_time=self.dur(0.5))
        self.hold()

        self.beat("b2")
        strips = VGroup()
        for k in range(16):
            c = S.KCOL if k % 2 == 0 else S.VCOL
            strips.add(Rectangle(width=0.22, height=2.4, stroke_width=0, fill_color=c, fill_opacity=0.75))
        strips.arrange(RIGHT, buff=0.06).move_to([-4.3, -0.5, 0])
        sl = T("K and V for every head", S.SMALL, S.TEXT).next_to(strips, DOWN, buff=0.25)
        self.play(FadeIn(strips, lag_ratio=0.05), FadeIn(sl), run_time=self.dur(0.2))
        funnel = Polygon([-2.2, 0.9, 0], [-2.2, -1.9, 0], [-0.9, -0.75, 0], [-0.9, -0.25, 0], color=S.MEMORY,
                         stroke_width=2, fill_color=S.MEMORY, fill_opacity=0.08)
        latent = Rectangle(width=1.2, height=0.3, stroke_width=0, fill_color=S.MEMORY, fill_opacity=1).move_to([0.0, -0.5, 0])
        ll = T("latent c", S.SMALL, S.MEMORY, weight="BOLD").next_to(latent, UP, buff=0.2)
        self.play(Create(funnel), run_time=0.5)
        self.play(ReplacementTransform(strips.copy(), latent), FadeIn(ll), run_time=self.dur(0.3))
        out = strips.copy().move_to([4.2, -0.5, 0])
        fun2 = Polygon([0.9, -0.25, 0], [0.9, -0.75, 0], [2.2, -1.9, 0], [2.2, 0.9, 0], color=S.COMPUTE,
                       stroke_width=2, fill_color=S.COMPUTE, fill_opacity=0.08)
        self.play(Create(fun2), run_time=0.4)
        self.play(TransformFromCopy(latent, out), run_time=self.dur(0.3))
        self.hold()

        self.beat("b3")
        st = T("stored  (memory)", S.SMALL, S.MEMORY).next_to(latent, DOWN, buff=0.9)
        up = M(r"W_{\text{up}}\, c", 36, S.COMPUTE).next_to(fun2, UP, buff=0.15)
        upl = T("rebuilt when needed (compute)", S.SMALL, S.COMPUTE).next_to(out, DOWN, buff=0.25)
        self.play(FadeIn(st), Write(up), FadeIn(upl), run_time=self.dur(0.4))
        trade = T("trade cheap compute for expensive memory", S.BODY, S.TEXT, weight="BOLD").move_to(DOWN * 2.8)
        self.play(FadeIn(trade), run_time=0.6)
        self.hold()

        self.beat("b4")
        self.play(FadeOut(VGroup(strips, sl, funnel, latent, ll, fun2, out, st, up, upl, trade)), run_time=0.5)
        bp = bar_pair("ordinary attention (V3 shape, hypothetical): 32,768 numbers / token / layer", 32768,
                      "MLA in DeepSeek-V3: 512 + 64 = 576 numbers", 576, max_len=10.0)
        fit_width(bp)
        bp.move_to(DOWN * 0.3)
        self.play(FadeIn(bp[0]), run_time=self.dur(0.35))
        self.play(FadeIn(bp[1]), run_time=self.dur(0.3))
        x57 = T("≈ 57× fewer numbers (our arithmetic)", S.SMALL, S.MEMORY, weight="BOLD").next_to(bp, DOWN, buff=0.4)
        src = source_line("DeepSeek-V3 config_671B.json")
        self.play(FadeIn(x57), FadeIn(src), run_time=0.6)
        self.hold()

        self.beat("b5")
        self.play(FadeOut(VGroup(bp, x57, src)), run_time=0.4)
        card = RoundedRectangle(corner_radius=0.15, width=10.4, height=2.4, stroke_color=S.MEMORY, stroke_width=2,
                                fill_color=S.PANEL, fill_opacity=1).move_to(DOWN * 0.3)
        big = T("−93.3% KV cache", 72, S.MEMORY, weight="BOLD")
        fit_width(big, 9.4)
        big.move_to(card).shift(UP * 0.3)
        who = T("DeepSeek-V2 vs DeepSeek 67B, as reported by DeepSeek", S.SMALL, S.MUTED).next_to(big, DOWN, buff=0.2)
        self.play(FadeIn(card), FadeIn(big, scale=1.1), FadeIn(who), run_time=self.dur(0.4))
        self.hold()
        self.play(FadeOut(VGroup(card, big, who, title, sub)), run_time=0.6)
        self.finish(tail=0.1)


class S0804ThreeDials(DocScene):
    SCENE_ID = "s0804"

    def construct(self):
        leg = WallsLegend()
        self.add(leg)
        self.beat("b1")
        f = M(r"\text{cache} = \text{entry size} \times \text{entries along the sequence} \times \text{layers keeping one}", 34)
        fit_width(f)
        f.to_edge(UP, buff=0.8)
        src = source_line("framing from the DeepSeek-V4.1-Flash paper §2.3")
        self.play(Write(f), FadeIn(src), run_time=self.dur(0.6))
        self.hold()

        self.beat("b2")
        dials = VGroup(dial("ENTRY SIZE"), dial("SEQUENCE"), dial("LAYERS")).arrange(RIGHT, buff=1.6).move_to(DOWN * 0.4)
        self.play(LaggedStart(*[FadeIn(d, scale=0.9) for d in dials], lag_ratio=0.3), run_time=self.dur(0.6))
        self.hold()

        self.beat("b3")
        d0 = dials[0]
        self.play(Rotate(d0.needle, angle=1.3 * PI / 1.0 * 0.9, about_point=d0.center_pt), run_time=self.dur(0.4))
        mla = T("MLA", S.BODY, S.MEMORY, weight="BOLD").next_to(d0, UP, buff=0.3)
        self.play(FadeIn(mla), run_time=0.5)
        self.hold()

        self.beat("b4")
        self.play(*[d[0].animate(rate_func=there_and_back).set_stroke(width=8) for d in dials[1:]],
                  *[d.animate(rate_func=there_and_back).scale(1.08) for d in dials[1:]], run_time=self.dur(0.6))
        y26 = T("2026 →", S.BODY, S.PARAM, weight="BOLD").next_to(VGroup(dials[1], dials[2]), UP, buff=0.3)
        self.play(FadeIn(y26), run_time=0.6)
        self.hold()
        self.play(FadeOut(Group(*[m for m in self.mobjects if m is not leg])), run_time=0.6)
        self.finish(tail=0.1)
