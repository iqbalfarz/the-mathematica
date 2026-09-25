"""ACT 9 — DeepSeek-V4.1-Flash: pushing the memory wall (primary source: the supplied paper)."""
import numpy as np
from manim import *  # noqa: F401,F403

from docu import style as S
from docu.base_scene import DocScene
from docu.components import (HBarChart, Heatmap, KVShelf, LayerTower, M, T, Token, WallsLegend, chip, fit_width,
                             safe_right, safe_top, source_line)

PAPER = "DeepSeek-V4.1-Flash paper (arXiv:2609.19969)"


class S0901Agents(DocScene):
    SCENE_ID = "s0901"

    def construct(self):
        self.beat("b1")
        names = ["model", "tool call", "result", "context grows"]
        cols = [S.TOKEN, S.COMM, S.PARAM, S.MEMORY]
        nodes = VGroup()
        for k, (n, c) in enumerate(zip(names, cols)):
            a = PI / 2 - k * TAU / 4
            box = RoundedRectangle(corner_radius=0.12, width=2.3, height=0.8, stroke_color=c, stroke_width=2,
                                   fill_color=c, fill_opacity=0.12)
            t = T(n, S.SMALL, S.TEXT).move_to(box)
            nodes.add(VGroup(box, t).move_to([2.2 * np.cos(a) - 2.4, 1.6 * np.sin(a) + 0.4, 0]))
        arrows = VGroup(*[CurvedArrow(nodes[k].get_center() + 0.55 * (nodes[(k + 1) % 4].get_center() - nodes[k].get_center()) / 1.0 * 0.5,
                                      nodes[(k + 1) % 4].get_center() + 0.25 * (nodes[k].get_center() - nodes[(k + 1) % 4].get_center()),
                                      angle=-PI / 4, color=S.MUTED, stroke_width=2) for k in range(4)])
        self.play(FadeIn(nodes, lag_ratio=0.2), run_time=self.dur(0.3))
        self.play(Create(arrows), run_time=0.8)
        cb = Rectangle(width=0.4, height=0.5, stroke_width=0, fill_color=S.MEMORY, fill_opacity=0.85)
        cb.move_to([2.2, -2.2, 0], aligned_edge=LEFT)
        cl = T("context", S.SMALL, S.MEMORY).next_to(cb, UP, buff=0.2).align_to(cb, LEFT)
        self.play(FadeIn(cb), FadeIn(cl), run_time=0.4)
        lap = self.dur(0.12, lo=0.6)
        for k in range(3):
            self.play(*[n[0].animate(rate_func=there_and_back).set_fill(opacity=0.5) for n in nodes],
                      cb.animate.stretch_to_fit_width(0.4 + 1.3 * (k + 1)).move_to([2.2, -2.2, 0], aligned_edge=LEFT),
                      run_time=lap)
        self.hold()

        self.beat("b2")
        self.play(FadeOut(VGroup(nodes, arrows, cb, cl)), run_time=0.5)
        inb = Rectangle(width=10.0, height=0.9, stroke_width=0, fill_color=S.TOKEN, fill_opacity=0.8)
        outb = Rectangle(width=0.5, height=0.9, stroke_width=0, fill_color=S.PARAM, fill_opacity=0.9)
        inl = T("input (prompt + tool results)", S.SMALL, S.TEXT)
        outl = T("output", S.SMALL, S.TEXT)
        r1 = VGroup(inl, inb).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        r2 = VGroup(outl, outb).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        VGroup(r1, r2).arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to(UP * 0.3)
        self.play(FadeIn(inl), GrowFromEdge(inb, LEFT), run_time=self.dur(0.35))
        self.play(FadeIn(outl), GrowFromEdge(outb, LEFT), run_time=0.6)
        ih = T("“increasingly input-heavy”", S.BODY, S.TOKEN, weight="BOLD").next_to(VGroup(r1, r2), DOWN, buff=0.6)
        src = source_line(PAPER + ", Abstract")
        self.play(FadeIn(ih), FadeIn(src), run_time=0.6)
        self.hold()

        self.beat("b3")
        self.play(FadeOut(VGroup(r1, r2, ih, src)), run_time=0.5)
        card = RoundedRectangle(corner_radius=0.15, width=10.4, height=4.4, stroke_color=S.MEMORY, stroke_width=2,
                                fill_color=S.PANEL, fill_opacity=1).move_to(DOWN * 0.1)
        t1 = T("DeepSeek-V4.1-Flash:", S.H2, S.TEXT, weight="BOLD")
        t2 = T("Pushing the Limits of KV Cache Compression", S.BODY, S.TEXT)
        t3 = T("DeepSeek-AI · arXiv:2609.19969 · 17 Sep 2026", S.SMALL, S.MUTED)
        head = VGroup(t1, t2, t3).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        head.move_to(card.get_top() + DOWN * (0.35 + head.height / 2)).align_to(card.get_left() + RIGHT * 0.45, LEFT)
        stats = VGroup(
            VGroup(T("552B", S.H2, S.PARAM, weight="BOLD", mono=True), T("backbone parameters", S.SMALL, S.TEXT)),
            VGroup(T("1M", S.H2, S.MEMORY, weight="BOLD", mono=True), T("token context", S.SMALL, S.TEXT)),
            VGroup(T("MoE", S.H2, S.EXPERT, weight="BOLD"), T("multimodal", S.SMALL, S.TEXT)))
        for s_ in stats:
            s_.arrange(DOWN, buff=0.1)
        stats.arrange(RIGHT, buff=1.1).next_to(head, DOWN, buff=0.55).set_x(card.get_x())
        self.play(FadeIn(card), FadeIn(head, shift=UP * 0.2), run_time=self.dur(0.35))
        self.play(LaggedStart(*[FadeIn(s_, shift=UP * 0.2) for s_ in stats], lag_ratio=0.3), run_time=self.dur(0.4))
        self.hold()

        self.beat("b4")
        self.play(FadeOut(VGroup(card, head, stats)), run_time=0.5)
        leg = WallsLegend().scale(1.8).move_to(UP * 0.4)
        self.play(FadeIn(leg), run_time=0.5)
        tamed = T("tamed by sparse attention", S.SMALL, S.MUTED).next_to(leg.item("COMPUTE"), DOWN, buff=0.35)
        self.play(leg.item("COMPUTE").animate.set_opacity(0.3), FadeIn(tamed), run_time=self.dur(0.3))
        self.play(leg.item("MEMORY").animate.scale(1.25), leg.item("COMMUNICATION").animate.scale(1.25),
                  run_time=self.dur(0.25))
        quote = T("storage and data movement: the prominent bottlenecks", S.BODY, S.TEXT).move_to(DOWN * 1.6)
        fit_width(quote)
        src = source_line(PAPER + " §1")
        self.play(FadeIn(quote), FadeIn(src), run_time=0.6)
        self.hold()
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.finish(tail=0.1)


def strip(n=48, w=0.2, h=0.5, color=S.MEMORY):
    return VGroup(*[Rectangle(width=w, height=h, stroke_color=S.BG, stroke_width=1, fill_color=color,
                              fill_opacity=0.35) for _ in range(n)]).arrange(RIGHT, buff=0.02)


class S0902SparseAttention(DocScene):
    SCENE_ID = "s0902"

    def construct(self):
        self.beat("b1")
        past = strip(48).move_to([-0.8, -0.6, 0])
        pl = T("past entries (up to a million)", S.SMALL, S.MEMORY).next_to(past, DOWN, buff=0.3)
        tok = Token("new", S.SMALL).next_to(past, RIGHT, buff=0.5).shift(UP * 1.8)
        self.play(FadeIn(past, lag_ratio=0.01), FadeIn(pl), FadeIn(tok), run_time=self.dur(0.35))
        lines = VGroup(*[Line(tok.get_bottom(), c.get_top(), color=S.ATTN, stroke_width=1, stroke_opacity=0.5)
                         for c in past])
        self.play(Create(lines, lag_ratio=0.01), run_time=self.dur(0.4))
        self.hold()

        self.beat("b2")
        scan = Rectangle(width=0.6, height=0.9, stroke_color=S.ROUTER, stroke_width=2).move_to(past[0])
        il = T("indexer", S.SMALL, S.ROUTER).next_to(scan, UP, buff=0.1)
        self.play(FadeOut(lines), FadeIn(scan), FadeIn(il), run_time=0.5)
        self.play(scan.animate.move_to(past[-1]), il.animate.next_to(past[-1], UP, buff=0.55), run_time=self.dur(0.3),
                  rate_func=linear)
        rng = np.random.default_rng(5)
        pick = sorted(rng.choice(48, 8, replace=False))
        self.play(FadeOut(scan), FadeOut(il), *[past[k].animate.set_fill(S.ATTN, opacity=0.95) for k in pick],
                  run_time=0.6)
        sel = VGroup(*[Line(tok.get_bottom(), past[k].get_top(), color=S.ATTN, stroke_width=3) for k in pick])
        self.play(Create(sel), run_time=self.dur(0.2))
        tk = chip("attend properly to the top 512 only", S.ATTN).to_edge(UP, buff=0.5)
        self.play(FadeIn(tk), run_time=0.5)
        self.hold()

        self.beat("b3")
        self.play(FadeOut(VGroup(sel, tk)), *[c.animate.set_fill(S.MEMORY, opacity=0.35) for c in past], run_time=0.5)
        comp = strip(24, w=0.42).move_to(past)
        ml = T("early layers: 2 neighbouring tokens → 1 entry", S.SMALL, S.MEMORY).next_to(comp, UP, buff=0.35)
        self.play(ReplacementTransform(past, comp), FadeIn(ml), run_time=self.dur(0.35))
        win = SurroundingRectangle(VGroup(*comp[-3:]), color=S.PARAM, buff=0.06, stroke_width=3)
        wl = T("sliding window: last 128 tokens, kept precisely", S.SMALL, S.PARAM).next_to(pl, DOWN, buff=0.2)
        self.play(Create(win), *[c.animate.set_fill(S.PARAM, opacity=0.8) for c in comp[-3:]], FadeIn(wl),
                  run_time=self.dur(0.35))
        self.hold()

        self.beat("b4")
        self.play(FadeOut(VGroup(comp, ml, win, wl, pl, tok)), run_time=0.5)
        n = 14
        m = np.tril(np.ones((n, n))) * 0.45
        hm = Heatmap(m, cell=0.3).move_to([-3.0, -0.3, 0])
        rngx = np.random.default_rng(9)
        sp = np.zeros((n, n))
        for i in range(n):
            ks = rngx.choice(i + 1, min(i + 1, 3), replace=False)
            sp[i, ks] = 0.9
        hs = Heatmap(sp, cell=0.3).move_to([3.0, -0.3, 0])
        l1 = T("every pair: grows as length²", S.SMALL, S.TEXT).next_to(hm, UP, buff=0.3)
        l2 = T("fixed picks per token", S.SMALL, S.ATTN).next_to(hs, UP, buff=0.3)
        ar = Arrow(hm.get_right(), hs.get_left(), buff=0.3, color=S.MUTED)
        self.play(FadeIn(hm), FadeIn(l1), run_time=self.dur(0.3))
        self.play(GrowArrow(ar), TransformFromCopy(hm, hs), FadeIn(l2), run_time=self.dur(0.4))
        src = source_line(PAPER + " §2.3, §4.2.1")
        self.add(src)
        self.hold()
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.finish(tail=0.1)


def badge(text, color):
    return chip(text, color, size=S.SMALL, fill_opacity=0.2)


class S0903LayerReuse(DocScene):
    SCENE_ID = "s0903"

    def construct(self):
        self.beat("b1")
        layers = VGroup(*[RoundedRectangle(corner_radius=0.04, width=3.0, height=0.26, stroke_color=S.PARAM,
                                           stroke_width=1.2, fill_color=S.PARAM, fill_opacity=0.2) for _ in range(10)])
        layers.arrange(UP, buff=0.14).move_to([-3.2, -0.2, 0])
        shelves = VGroup(*[KVShelf(n=6, slot_w=0.14, slot_h=0.22, gap=0.04, label=False).next_to(l, RIGHT, buff=0.6)
                           for l in layers])
        ll = T("each layer keeps its own cache", S.SMALL, S.MEMORY).next_to(shelves, RIGHT, buff=0.4)
        rep = T("(10 shown for 40 layers)", S.TINY, S.MUTED).next_to(layers, DOWN, buff=0.2)
        self.play(FadeIn(layers, lag_ratio=0.1), FadeIn(rep), run_time=self.dur(0.3))
        self.play(FadeIn(shelves, lag_ratio=0.1), FadeIn(ll), run_time=self.dur(0.4))
        self.hold()

        self.beat("b2")
        badges = VGroup(badge("FULL", S.MEMORY), badge("REINDEX", S.ATTN), badge("REUSE", S.EXPERT))
        badges.arrange(RIGHT, buff=0.5).to_edge(UP, buff=0.45)
        title = T("Compressed Sparse Attention 2 (CSA2)", S.SMALL, S.TEXT, weight="BOLD").next_to(badges, DOWN, buff=0.2)
        self.play(FadeIn(badges, lag_ratio=0.3), FadeIn(title), run_time=self.dur(0.6))
        self.hold()

        self.beat("b3")
        self.play(FadeOut(VGroup(ll, rep)), run_time=0.3)
        modes = ["FULL"] + ["REUSE"] * 2 + ["REINDEX"] + ["REUSE"] * 2 + ["FULL"] + ["REUSE"] * 3
        colors = {"FULL": S.MEMORY, "REINDEX": S.ATTN, "REUSE": S.EXPERT}
        tags = VGroup(*[T(m.lower(), S.TINY, colors[m]).next_to(l, LEFT, buff=0.2) for m, l in zip(modes, layers)])
        self.play(FadeIn(tags, lag_ratio=0.05), *[l.animate.set_stroke(colors[m], width=2) for m, l in zip(modes, layers)],
                  run_time=self.dur(0.3))
        exp = VGroup(T("full: builds the shared memory + picks entries", S.SMALL, S.MEMORY),
                     T("reindex: borrows memory, re-picks with its own query", S.SMALL, S.ATTN),
                     T("reuse: borrows memory and picks; keeps only its query", S.SMALL, S.EXPERT))
        exp.arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([3.4, -2.3, 0])
        fit_width(exp, 6.6)
        exp.set_x(safe_right() - exp.width / 2)
        for e in exp:
            self.play(FadeIn(e, shift=LEFT * 0.2), run_time=self.dur(0.12, lo=0.5))
        self.hold()

        self.beat("b4")
        keep = [k for k, m in enumerate(modes) if m == "FULL"]
        self.play(*[FadeOut(shelves[k]) for k in range(10) if k not in keep],
                  *[shelves[k].animate.set_opacity(1) for k in keep], run_time=self.dur(0.4))
        borrow = VGroup(*[Arrow(shelves[max(j for j in keep if j <= k)].get_left(), layers[k].get_right(), buff=0.1,
                                color=colors[modes[k]], stroke_width=2, max_tip_length_to_length_ratio=0.1)
                          for k in range(10) if k not in keep])
        self.play(LaggedStart(*[Create(a) for a in borrow], lag_ratio=0.1), run_time=self.dur(0.3))
        grp = T("encoder: groups of 6 (1 full + 5 reuse) · decoder: groups of 4", S.SMALL, S.TEXT)
        fit_width(grp)
        grp.next_to(title, DOWN, buff=0.25)
        self.play(FadeIn(grp), run_time=0.6)
        self.hold()

        self.beat("b5")
        warn = chip("⚠ shared selection can occasionally pick the wrong entries (paper §6)", S.PARAM)
        fit_width(warn)
        warn.move_to([0, -3.1, 0])
        self.play(FadeOut(exp), FadeIn(warn), run_time=self.dur(0.4))
        self.hold()
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.finish(tail=0.1)


E2M1 = [0, 0.5, 1, 1.5, 2, 3, 4, 6]


class S0904FourBits(DocScene):
    SCENE_ID = "s0904"

    def construct(self):
        self.beat("b1")
        b8 = VGroup(*[Square(0.5, stroke_color=S.TEXT, stroke_width=1.5, fill_color=S.MEMORY, fill_opacity=0.6)
                      for _ in range(8)]).arrange(RIGHT, buff=0.06).move_to(UP * 0.6)
        l8 = T("8 bits", S.BODY, S.TEXT).next_to(b8, UP, buff=0.3)
        self.play(FadeIn(b8), FadeIn(l8), run_time=0.6)
        b4 = VGroup(*[Square(0.5, stroke_color=S.TEXT, stroke_width=1.5, fill_color=S.MEMORY, fill_opacity=0.95)
                      for _ in range(4)]).arrange(RIGHT, buff=0.06).move_to(DOWN * 0.8)
        l4 = T("4 bits (FP4)", S.BODY, S.MEMORY, weight="BOLD").next_to(b4, DOWN, buff=0.3)
        self.play(TransformFromCopy(VGroup(*b8[:4]), b4), FadeIn(l4), run_time=self.dur(0.4))
        self.hold()

        self.beat("b2")
        self.play(FadeOut(VGroup(b8, l8)), VGroup(b4, l4).animate.scale(0.7).to_edge(UP, buff=0.5), run_time=0.6)
        nl = NumberLine(x_range=[-6.5, 6.5, 1], length=12.4, color=S.MUTED, include_ticks=False).move_to(DOWN * 0.4)
        vals = sorted(set([-v for v in E2M1] + E2M1))
        ticks = VGroup(*[Line(nl.n2p(v) + DOWN * 0.22, nl.n2p(v) + UP * 0.22, color=S.MEMORY, stroke_width=4)
                         for v in vals])
        labs = VGroup(*[T(("−" if v < 0 else "") + f"{abs(v):g}", S.TINY, S.TEXT).next_to(nl.n2p(v), DOWN, buff=0.3)
                        for v in vals if abs(v) not in (0.5, 1.5)])
        halfs = VGroup(*[T(("−" if v < 0 else "") + f"{abs(v):g}", S.TINY, S.MUTED).next_to(nl.n2p(v), UP, buff=0.3)
                         for v in vals if abs(v) in (0.5, 1.5)])
        self.play(Create(nl), run_time=0.5)
        self.play(LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.08), FadeIn(labs), FadeIn(halfs),
                  run_time=self.dur(0.55))
        fmt = T("E2M1: every value a 4-bit code can mean", S.SMALL, S.MEMORY).next_to(nl, DOWN, buff=0.9)
        self.play(FadeIn(fmt), run_time=0.5)
        self.hold()

        self.beat("b3")
        rng = np.random.default_rng(11)
        raw = rng.normal(0, 0.9, 16)
        scale = 6 / np.abs(raw).max()
        dots = VGroup(*[Dot(nl.n2p(v), radius=0.07, color=S.PARAM) for v in raw]).shift(UP * 1.1)
        dl = T("16 real values from the cache", S.SMALL, S.PARAM).next_to(dots, UP, buff=0.35)
        self.play(FadeIn(dots, lag_ratio=0.1), FadeIn(dl), run_time=self.dur(0.25))
        sc = T(f"shared scale for this group (E4M3): ÷ {1/scale:.2f}", S.SMALL, S.TEXT).next_to(fmt, DOWN, buff=0.25)
        self.play(*[d.animate.move_to(nl.n2p(v * scale) + UP * 1.1) for d, v in zip(dots, raw)], FadeIn(sc),
                  run_time=self.dur(0.25))
        snapped = [min(vals, key=lambda t: abs(t - v * scale)) for v in raw]
        self.play(*[d.animate.move_to(nl.n2p(s)).set_color(S.MEMORY) for d, s in zip(dots, snapped)],
                  run_time=self.dur(0.25))
        self.hold()

        self.beat("b4")
        self.play(FadeOut(VGroup(nl, ticks, labs, halfs, dots, dl, fmt, sc, b4, l4)), run_time=0.5)
        s8 = Rectangle(width=2.2, height=3.0, stroke_width=0, fill_color=S.MEMORY, fill_opacity=0.5)
        s4 = Rectangle(width=2.2, height=1.5, stroke_width=0, fill_color=S.MEMORY, fill_opacity=0.95)
        VGroup(s8, s4).arrange(RIGHT, buff=2.0, aligned_edge=DOWN).move_to(DOWN * 0.3)
        a = T("V4: FP8 main cache", S.SMALL, S.TEXT).next_to(s8, DOWN, buff=0.25)
        b = T("V4.1-Flash: FP4 main cache", S.SMALL, S.MEMORY, weight="BOLD").next_to(s4, DOWN, buff=0.25)
        self.play(GrowFromEdge(s8, DOWN), FadeIn(a), run_time=0.6)
        self.play(GrowFromEdge(s4, DOWN), FadeIn(b), run_time=self.dur(0.3))
        swa = T("local window stays FP8 (sensitive to quantisation)", S.SMALL, S.MUTED).to_edge(UP, buff=0.8)
        src = source_line(PAPER + " §2.4.4")
        self.play(FadeIn(swa), FadeIn(src), run_time=0.6)
        self.hold()
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.finish(tail=0.1)


class S0905EncoderDecoder(DocScene):
    SCENE_ID = "s0905"

    def construct(self):
        self.beat("b1")
        pre = VGroup(*[Square(0.2, stroke_width=0, fill_color=S.TOKEN, fill_opacity=0.8) for _ in range(60)])
        pre.arrange_in_grid(6, 10, buff=0.05).move_to([-3.4, 0.2, 0])
        pl = T("PREFILL: read the whole input", S.SMALL, S.TOKEN, weight="BOLD").next_to(pre, DOWN, buff=0.3)
        dec = VGroup(*[Square(0.2, stroke_width=0, fill_color=S.PARAM, fill_opacity=0.9) for _ in range(5)])
        dec.arrange(RIGHT, buff=0.12).move_to([3.4, 0.2, 0])
        dl = T("DECODE: write one token at a time", S.SMALL, S.PARAM, weight="BOLD").next_to(dec, DOWN, buff=0.3)
        self.play(FadeIn(pre, lag_ratio=0.01), FadeIn(pl), run_time=self.dur(0.4))
        self.play(LaggedStart(*[FadeIn(d, shift=RIGHT * 0.2) for d in dec], lag_ratio=0.4), FadeIn(dl),
                  run_time=self.dur(0.4))
        self.hold()

        self.beat("b2")
        self.play(FadeOut(VGroup(pre, pl, dec, dl)), run_time=0.4)
        enc = LayerTower(n=10, w=3.0, h=0.2, gap=0.08, color=S.TOKEN).move_to([-2.2, -1.7, 0])
        decd = LayerTower(n=10, w=3.0, h=0.2, gap=0.08, color=S.PARAM).next_to(enc, UP, buff=0.35)
        el = T("encoder · 20 layers", S.SMALL, S.TOKEN).next_to(enc, LEFT, buff=0.3)
        dl2 = T("decoder · 20 layers", S.SMALL, S.PARAM).next_to(decd, LEFT, buff=0.3)
        self.play(FadeIn(enc), FadeIn(decd), FadeIn(el), FadeIn(dl2), run_time=self.dur(0.3))
        top = enc.slabs[-1]
        mems = VGroup(*[Rectangle(width=0.35, height=0.16, stroke_width=0, fill_color=S.MEMORY, fill_opacity=0.9)
                        .next_to(s, RIGHT, buff=0.9) for s in decd.slabs])
        fan = VGroup(*[Line(top.get_right(), m.get_left(), color=S.MEMORY, stroke_width=1.5, stroke_opacity=0.8)
                       for m in mems])
        fl = T("decoder memory projected from the encoder's final output", S.SMALL, S.MEMORY)
        fit_width(fl, 6.0)
        fl.next_to(mems, RIGHT, buff=0.3)
        fl.set_x(min(fl.get_x(), safe_right() - fl.width / 2))
        self.play(Create(fan, lag_ratio=0.05), FadeIn(mems), run_time=self.dur(0.35))
        self.play(FadeIn(fl), run_time=0.5)
        self.hold()

        self.beat("b3")
        prompt = VGroup(*[Square(0.14, stroke_width=0, fill_color=S.TOKEN, fill_opacity=0.9) for _ in range(20)])
        prompt.arrange(RIGHT, buff=0.04).next_to(enc, DOWN, buff=0.25)
        self.play(FadeIn(prompt), decd.animate.set_opacity(0.25), run_time=0.5)
        self.play(prompt.animate.move_to(enc.get_top() + UP * 0.1).set_opacity(0.2),
                  LaggedStart(*[s.animate.set_fill(S.COMPUTE, opacity=0.85) for s in enc.slabs], lag_ratio=0.1),
                  run_time=self.dur(0.4))
        half = T("≈ half the prefill compute", S.BODY, S.COMPUTE, weight="BOLD").to_edge(UP, buff=0.6)
        self.play(FadeIn(half), run_time=0.5)
        self.hold()

        self.beat("b4")
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
        m1 = self._meter("PREFILL", 8, S.TOKEN).move_to([-2.6, 0, 0])
        m2 = self._meter("DECODE", 16, S.PARAM).move_to([2.6, 0, 0])
        self.play(FadeIn(m1[0]), FadeIn(m2[0]), run_time=0.4)
        self.play(GrowFromEdge(m1[1], DOWN), GrowFromEdge(m2[1], DOWN), FadeIn(m1[2]), FadeIn(m2[2]),
                  FadeIn(m1[3]), FadeIn(m2[3]), run_time=self.dur(0.4))
        src = source_line(PAPER + " Abstract, §2.2")
        self.add(src)
        self.hold()
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.finish(tail=0.1)

    def _meter(self, name, val, color):
        frame = Rectangle(width=1.4, height=4.0, stroke_color=S.MUTED, stroke_width=1.5)
        fill = Rectangle(width=1.4, height=4.0 * val / 16, stroke_width=0, fill_color=color, fill_opacity=0.85)
        fill.move_to(frame, aligned_edge=DOWN)
        lab = T(name, S.SMALL, color, weight="BOLD").next_to(frame, DOWN, buff=0.2)
        v = T(f"{val}B active", S.BODY, S.TEXT, weight="BOLD").next_to(frame, UP, buff=0.2)
        return VGroup(frame, fill, lab, v)


class S0906TheChart(DocScene):
    SCENE_ID = "s0906"

    def construct(self):
        items = [("DeepSeek-V1", 389120, "2023.11"), ("DeepSeek-V3.2", 48068, "2025.12"),
                 ("DeepSeek-V4-Flash", 3514, "2026.04"), ("DeepSeek-V4.1-Flash", 890, "2026.09")]
        chart = HBarChart(items, max_len=6.8, bar_h=0.5, gap=0.55, color=S.MEMORY, highlight=3)
        chart.move_to([0.6, -0.2, 0])
        title = T("Global KV cache per token (bytes)", S.BODY, S.TEXT, weight="BOLD").to_edge(UP, buff=0.6)
        attr = source_line("Data: DeepSeek-AI, arXiv:2609.19969, Fig. 1(b) — recreated; linear scale")
        self.beat("b1")
        self.play(FadeIn(title), FadeIn(attr), Create(chart.axis), run_time=self.dur(0.5))
        self.hold()
        for k, b in enumerate(["b2", "b3", "b4", "b5"]):
            self.beat(b)
            r = chart.rows[k]
            if b == "b5":
                tease = VGroup(T("890 bytes", S.SMALL, S.MEMORY, weight="BOLD"), T("?", S.SMALL, S.PARAM, weight="BOLD"))
                tease.arrange(RIGHT, buff=0.1).move_to([safe_right() - 0.8, safe_top() - 0.2, 0])
                self.add(tease)
            self.play(FadeIn(r[0]), GrowFromEdge(r[1], LEFT), run_time=self.dur(0.35))
            self.play(FadeIn(r[2]), run_time=0.4)
            if b == "b5":
                self.play(tease.animate.next_to(r[2], RIGHT, buff=0.3).set_opacity(0), Flash(r[1], color=S.TOKEN),
                          run_time=1.0)
                self.remove(tease)
            self.hold()

        self.beat("b6")
        a1 = T("≈ 437× smaller than V1", S.BODY, S.TOKEN, weight="BOLD")
        a2 = T("≈ 4× smaller than V4-Flash", S.BODY, S.TOKEN, weight="BOLD")
        ann = VGroup(a1, a2).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to([3.4, -2.5, 0])
        ann.set_x(safe_right() - ann.width / 2)
        self.play(FadeIn(ann, lag_ratio=0.4), run_time=self.dur(0.5))
        self.hold()

        self.beat("b7")
        self.play(FadeOut(VGroup(chart, ann, title)), run_time=0.5)
        axl = Line(LEFT * 5, RIGHT * 5, color=S.MUTED).move_to(DOWN * 1.8)
        p1 = Dot(axl.get_left(), color=S.TEXT)
        p2 = Dot(axl.get_right(), color=S.TEXT)
        l1 = T("4K tokens", S.SMALL, S.TEXT).next_to(p1, DOWN, buff=0.2)
        l2 = T("1M tokens (256×)", S.SMALL, S.TEXT).next_to(p2, DOWN, buff=0.2)
        cost = Line(axl.get_left() + UP * 1.6, axl.get_right() + UP * 2.0, color=S.COMPUTE, stroke_width=6)
        cl = T("compute per new token: +¼", S.BODY, S.COMPUTE, weight="BOLD").next_to(cost, UP, buff=0.3)
        ctx = T("V4.1-Flash decode FLOPs vs context length (paper Fig. 2)", S.SMALL, S.MUTED).to_edge(UP, buff=0.6)
        self.play(Create(axl), FadeIn(p1), FadeIn(l1), FadeIn(ctx), run_time=0.6)
        self.play(FadeIn(p2), FadeIn(l2), Create(cost), run_time=self.dur(0.4))
        self.play(FadeIn(cl), run_time=0.5)
        self.hold()

        self.beat("b8")
        self.play(FadeOut(VGroup(axl, p1, p2, l1, l2, cost, cl, ctx)), run_time=0.5)
        card = RoundedRectangle(corner_radius=0.15, width=9.4, height=2.0, stroke_color=S.TOKEN, stroke_width=2,
                                fill_color=S.PANEL, fill_opacity=1)
        c1 = T("smaller memory, better overall results than V4-Flash", S.BODY, S.TEXT, weight="BOLD")
        c2 = T("as reported by DeepSeek, on its own evaluations", S.SMALL, S.MUTED)
        fit_width(c1, 8.8)
        VGroup(c1, c2).arrange(DOWN, buff=0.2).move_to(card)
        self.play(FadeIn(card), FadeIn(c1), FadeIn(c2), run_time=self.dur(0.4))
        self.hold()
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.finish(tail=0.2)
