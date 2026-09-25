"""ACT 4 — Inside a Transformer, built from a single sentence."""
import numpy as np
from manim import *  # noqa: F401,F403

from docu import style as S
from docu.base_scene import DocScene
from docu.components import (GPU, Block, Heatmap, LayerTower, M, T, Token, TokenRow, attention_arcs, caption, chip,
                             fit_width, prob_bars, softmax, vec_column)

WORDS = ["The", "animal", "didn't", "cross", "the", "street", "because", "it", "was", "tired", "."]
IT = 7
# illustrative raw scores of "it"'s query against keys of earlier tokens (causal)
SCORES = np.array([-0.6, 4.1, -0.9, 0.9, -0.6, 1.3, 0.5, 1.0])
VEC2 = {"animal": (2.0, 1.2), "dog": (2.4, 0.7), "cat": (1.6, 1.7), "street": (-1.9, 1.3), "road": (-2.3, 0.7),
        "tired": (0.5, -2.1), "sleepy": (1.6, -1.7), "it": (0.1, 0.9)}


def sentence_row(size=S.SMALL):
    return TokenRow(WORDS, size=size, buff=0.1)


def vec_icon(color, n=4, size=0.2):
    return VGroup(*[Square(size, stroke_width=0, fill_color=color, fill_opacity=0.35 + 0.6 * ((k * 37) % 5) / 5)
                    for k in range(n)]).arrange(RIGHT, buff=0.03)


def causal_matrix(n=11, seed=3):
    rng = np.random.default_rng(seed)
    m = np.zeros((n, n))
    for i in range(n):
        s = rng.normal(0, 1, i + 1)
        s[i] += 1.2
        if i >= 1:
            s[i - 1] += 0.8
        if i == IT:
            s[:IT + 1] = SCORES
        m[i, :i + 1] = softmax(s)
    return m


class S0401TheSentence(DocScene):
    SCENE_ID = "s0401"

    def construct(self):
        self.beat("b1")
        g = GPU(w=3.4, h=2.5, cores=(10, 14))
        self.add(g)
        self.play(self.camera.frame.animate.scale(0.12).move_to(g.cores[70]), g.cores.animate.set_fill(opacity=0.9),
                  run_time=self.dur(0.7))
        self.play(FadeOut(g), run_time=0.4)
        self.camera.frame.scale(1 / 0.12).move_to(ORIGIN)
        inside = T("inside a language model", S.BODY, S.MUTED)
        self.play(FadeIn(inside, scale=1.1), run_time=0.8)
        self.hold()
        self.play(FadeOut(inside), run_time=0.4)

        self.beat("b2")
        sent = T("The animal didn't cross the street because it was tired.", S.H2, S.TEXT)
        fit_width(sent)
        self.play(AddTextLetterByLetter(sent), run_time=self.dur(0.6, hi=3.2))
        self.hold()

        self.beat("b3")
        row = sentence_row(S.BODY)
        self.play(FadeOut(sent), FadeIn(row), run_time=0.5)
        it = row[IT]
        self.play(it.glow(S.QCOL, 0.5), run_time=0.5)
        arcs = VGroup(*[ArcBetweenPoints(it.get_top() + UP * 0.05, row[k].get_top() + UP * 0.05, angle=-1.1,
                                         color=S.ATTN, stroke_width=3) for k in (1, 5)])
        dashed = VGroup(*[DashedVMobject(a, num_dashes=18) for a in arcs])
        qm = T("?", S.H2, S.PARAM, weight="BOLD").move_to(UP * 2.2)
        self.play(Create(dashed), FadeIn(qm), run_time=self.dur(0.4))
        self.hold()

        self.beat("b4")
        strong = arcs[0].copy().set_stroke(width=9)
        self.play(ReplacementTransform(dashed[0], strong), dashed[1].animate.set_opacity(0.12), FadeOut(qm),
                  row[1].glow(S.TOKEN, 0.55), run_time=self.dur(0.3))
        clue = T("clue: tired", S.SMALL, S.PARAM).next_to(row[9], DOWN, buff=0.35)
        self.play(row[9].glow(S.PARAM, 0.5), FadeIn(clue), run_time=self.dur(0.2))
        self.hold()

        self.beat("b5")
        self.play(FadeOut(VGroup(strong, dashed[1], clue)), *[t.glow(S.TOKEN, 0.16) for t in row], run_time=0.5)
        target = row.copy().arrange(RIGHT, buff=0.3).move_to(ORIGIN)
        fit_width(target)
        self.play(Transform(row, target), run_time=self.dur(0.3))
        lbl = T("tokens", S.BODY, S.TOKEN, weight="BOLD").next_to(row, DOWN, buff=0.5)
        self.play(FadeIn(lbl, shift=UP * 0.2), run_time=0.6)
        self.hold()
        self.play(FadeOut(lbl), row.animate.scale(0.8).to_edge(UP, buff=0.6), run_time=0.6)
        self.finish(tail=0.1)


class S0402Embeddings(DocScene):
    SCENE_ID = "s0402"

    def construct(self):
        row = sentence_row(S.BODY).arrange(RIGHT, buff=0.3).scale(0.8).to_edge(UP, buff=0.6)
        self.add(row)
        self.beat("b1")
        tok = row[1].copy()
        self.play(tok.animate.move_to([-4.8, 1.3, 0]), run_time=0.6)
        col = vec_column(["0.21", "−1.3", "0.82", "0.05", "−0.6", "1.1"], color=S.TOKEN, cell=0.62, num_size=S.SMALL)
        col.next_to(tok, DOWN, buff=0.25)
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.1) for c in VGroup(*[VGroup(col.cells[k], col.nums[k])
                                                                               for k in range(6)])], lag_ratio=0.2),
                  run_time=self.dur(0.5))
        lab = T("embedding", S.SMALL, S.TOKEN).next_to(col, DOWN, buff=0.2)
        self.play(FadeIn(lab), run_time=0.5)
        self.hold()

        self.beat("b2")
        ax = Axes(x_range=[-3, 3, 1], y_range=[-3, 3, 1], x_length=5.2, y_length=4.6,
                  axis_config={"color": S.DIM, "stroke_width": 1.5, "include_ticks": False}).move_to([2.2, -0.9, 0])
        self.play(Create(ax), run_time=0.6)
        arrows = {}

        def arrow(word, color=S.TOKEN):
            v = VEC2[word]
            a = Arrow(ax.c2p(0, 0), ax.c2p(*v), buff=0, color=color, stroke_width=4,
                      max_tip_length_to_length_ratio=0.12)
            d = {"tired": LEFT + DOWN * 0.3, "sleepy": RIGHT + DOWN * 0.3}.get(
                word, np.sign(v[0]) * RIGHT * 0.6 + np.sign(v[1]) * UP * 0.4)
            t = T(word, S.SMALL, color).next_to(ax.c2p(*v), d, buff=0.1)
            return VGroup(a, t)
        arrows["animal"] = arrow("animal")
        two = VGroup(col.nums[0].copy(), col.nums[1].copy())
        self.play(ReplacementTransform(VGroup(col, lab), arrows["animal"]), run_time=self.dur(0.5))
        self.play(FadeOut(tok), run_time=0.3)
        self.hold()

        self.beat("b3")
        order = [("dog", S.TOKEN), ("cat", S.TOKEN), ("street", S.KCOL), ("road", S.KCOL), ("tired", S.PARAM),
                 ("sleepy", S.PARAM)]
        for w, c in order:
            arrows[w] = arrow(w, c)
        self.play(LaggedStart(*[GrowArrow(arrows[w][0]) for w, _ in order], lag_ratio=0.25),
                  LaggedStart(*[FadeIn(arrows[w][1]) for w, _ in order], lag_ratio=0.25), run_time=self.dur(0.7))
        self.hold()

        self.beat("b4")
        others = VGroup(*[arrows[w] for w in ("cat", "street", "road", "tired", "sleepy")])
        self.play(others.animate.set_opacity(0.15), run_time=0.5)
        a1, a2 = arrows["animal"][0], arrows["dog"][0]
        ang = Angle(a2, a1, radius=0.9, color=S.ATTN, stroke_width=4)
        dot = M(r"\vec a \cdot \vec b \;=\; |a|\,|b|\cos\theta", 38, S.ATTN).move_to([-3.6, -0.6, 0])
        big = T("small angle → big dot product → related", S.SMALL, S.TEXT).next_to(dot, DOWN, buff=0.35)
        fit_width(big, 6.0)
        self.play(Create(ang), Write(dot), run_time=self.dur(0.4))
        self.play(FadeIn(big), run_time=0.6)
        self.hold()
        self.play(FadeOut(VGroup(ax, *arrows.values(), ang, dot, big)), run_time=0.6)
        self.finish(tail=0.1)


class S0403QueryKeyValue(DocScene):
    SCENE_ID = "s0403"

    def construct(self):
        row = sentence_row(S.BODY).arrange(RIGHT, buff=0.3).scale(0.8).to_edge(UP, buff=0.6)
        self.add(row)
        self.beat("b1")
        it = row[IT].copy()
        self.play(it.animate.scale(1.3).move_to([-4.6, 0.4, 0]), run_time=0.6)
        emb = vec_icon(S.TOKEN, 5, 0.26).next_to(it, DOWN, buff=0.25)
        self.play(FadeIn(emb), run_time=0.4)
        names = [("Q", S.QCOL, "W_Q"), ("K", S.KCOL, "W_K"), ("V", S.VCOL, "W_V")]
        outs = VGroup()
        for k, (n, c, w) in enumerate(names):
            y = 1.3 - k * 1.25
            mat = VGroup(Square(0.62, stroke_color=S.PARAM, stroke_width=2, fill_color=S.PARAM, fill_opacity=0.12),
                         M(w, 30, S.PARAM))
            mat[1].move_to(mat[0])
            mat.move_to([-1.6, y, 0])
            v = vec_icon(c, 4, 0.26).move_to([0.6, y, 0])
            vl = M(n, 40, c).next_to(v, RIGHT, buff=0.25)
            a1 = Arrow(emb.get_right(), mat.get_left(), buff=0.12, color=S.MUTED, stroke_width=2.5)
            a2 = Arrow(mat.get_right(), v.get_left(), buff=0.12, color=S.MUTED, stroke_width=2.5)
            outs.add(VGroup(a1, mat, a2, v, vl))
        self.play(LaggedStart(*[FadeIn(o, shift=RIGHT * 0.2) for o in outs], lag_ratio=0.35),
                  run_time=self.dur(0.6))
        self.hold()

        self.beat("b2")
        qb = T("“which noun am I talking about?”", S.SMALL, S.QCOL).next_to(outs[0][4], RIGHT, buff=0.4)
        self.play(Indicate(outs[0][3], color=S.QCOL), FadeIn(qb), run_time=self.dur(0.5))
        self.hold()

        self.beat("b3")
        self.play(FadeOut(VGroup(it, emb, outs, qb)), run_time=0.5)
        ks = VGroup(*[vec_icon(S.KCOL, 3, 0.16).next_to(t, DOWN, buff=0.28) for t in row])
        kl = T("keys", S.SMALL, S.KCOL).next_to(ks, LEFT, buff=0.2)
        kl.set_x(max(kl.get_x(), -6.9 + kl.width / 2))
        self.play(LaggedStart(*[FadeIn(k) for k in ks], lag_ratio=0.08), run_time=self.dur(0.35))
        ab = T("“living thing, a noun”", S.SMALL, S.KCOL).next_to(ks[1], DOWN, buff=0.35)
        self.play(FadeIn(ab), run_time=0.6)
        self.hold()

        self.beat("b4")
        vs = VGroup(*[vec_icon(S.VCOL, 3, 0.16).next_to(k, DOWN, buff=0.18) for k in ks])
        self.play(FadeOut(ab), LaggedStart(*[FadeIn(v) for v in vs], lag_ratio=0.08), run_time=self.dur(0.4))
        vl = T("values", S.SMALL, S.VCOL).next_to(vs, DOWN, buff=0.3)
        self.play(FadeIn(vl), run_time=0.4)
        self.hold()

        self.beat("b5")
        self.play(FadeOut(vl), run_time=0.3)
        q = vec_icon(S.QCOL, 3, 0.2).move_to([row[IT].get_x(), -1.7, 0])
        ql = M("Q_{it}", 34, S.QCOL).next_to(q, DOWN, buff=0.15)
        self.play(FadeIn(q), FadeIn(ql), row[IT].glow(S.QCOL, 0.5), run_time=0.6)
        mask = VGroup(*[t for t in row[IT + 1:]] + [ks[k] for k in range(IT + 1, 11)] + [vs[k] for k in range(IT + 1, 11)])
        self.play(mask.animate.set_opacity(0.18), run_time=0.5)
        masked = T("future tokens: not visible", S.TINY, S.MUTED).next_to(VGroup(*[row[k] for k in range(IT + 1, 11)]),
                                                                         DOWN, buff=1.3)
        self.play(FadeIn(masked), run_time=0.4)
        scores = VGroup()
        for k in range(IT + 1):
            s = T(f"{SCORES[k]:.1f}", S.SMALL, S.ATTN if SCORES[k] > 1.2 else S.TEXT, mono=True)
            s.move_to([row[k].get_x(), -2.6, 0])
            scores.add(s)
        for k in range(IT + 1):
            self.play(q.animate.move_to([row[k].get_x(), -1.7, 0]), ql.animate.next_to(
                [row[k].get_x(), -1.7 - 0.2, 0], DOWN, buff=0.15), FadeIn(scores[k], scale=1.3),
                run_time=self.dur(0.06, lo=0.22))
        self.hold()

        self.beat("b6")
        self.play(FadeOut(VGroup(q, ql, masked, ks, vs, scores)), row.animate.set_opacity(1), run_time=0.5)
        hm = Heatmap(causal_matrix(), cell=0.36).move_to([1.6, -0.9, 0])
        rl = VGroup(*[T(w, S.TINY, S.TEXT).next_to(hm.cells[i * 11], LEFT, buff=0.12) for i, w in enumerate(WORDS)])
        expr = M(r"Q K^{\top}", 64, S.ATTN).move_to([-4.2, -0.4, 0])
        cap = T("causal: each token only sees the past", S.TINY, S.MUTED).next_to(expr, DOWN, buff=0.4)
        self.play(FadeIn(hm, lag_ratio=0.01), FadeIn(rl), run_time=self.dur(0.4))
        self.play(Write(expr), FadeIn(cap), run_time=self.dur(0.3))
        self.hold()
        self.play(FadeOut(VGroup(hm, rl, expr, cap)), run_time=0.5)
        self.finish(tail=0.1)


class S0404Softmax(DocScene):
    SCENE_ID = "s0404"

    def construct(self):
        row = sentence_row(S.BODY).arrange(RIGHT, buff=0.3).scale(0.8).to_edge(UP, buff=0.6)
        self.add(row)
        n = IT + 1
        base_y = -0.4
        xs = [row[k].get_x() for k in range(n)]
        self.beat("b1")
        unit = 0.55
        bars = VGroup()
        for k in range(n):
            h = SCORES[k] * unit
            r = Rectangle(width=0.5, height=abs(h), stroke_width=0, fill_color=S.ATTN, fill_opacity=0.8)
            r.move_to([xs[k], base_y + h / 2, 0])
            bars.add(r)
        axis = Line([xs[0] - 0.6, base_y, 0], [xs[-1] + 0.6, base_y, 0], color=S.MUTED, stroke_width=1.5)
        lab = T("raw scores for “it”", S.SMALL, S.MUTED).next_to(axis, DOWN, buff=0.9).align_to(axis, RIGHT)
        self.play(Create(axis), FadeIn(lab), LaggedStart(*[GrowFromEdge(b, DOWN if SCORES[k] > 0 else UP)
                                                          for k, b in enumerate(bars)], lag_ratio=0.1),
                  run_time=self.dur(0.5))
        self.hold()

        self.beat("b2")
        ex = np.exp(SCORES)
        eunit = 3.0 / ex.max()
        new = VGroup(*[Rectangle(width=0.5, height=max(0.03, e * eunit), stroke_width=0, fill_color=S.ATTN,
                                 fill_opacity=0.8).move_to([xs[k], base_y + e * eunit / 2 - 1.2, 0])
                       for k, e in enumerate(ex)])
        self.play(axis.animate.shift(DOWN * 1.2), lab.animate.become(
            T("e^score", S.SMALL, S.MUTED).next_to(axis.copy().shift(DOWN * 1.2), RIGHT, buff=0.25)),
            ReplacementTransform(bars, new), run_time=self.dur(0.5))
        f1 = M(r"s_i \;\to\; e^{s_i}", 40).move_to([4.6, 1.3, 0])
        self.play(Write(f1), run_time=0.8)
        self.hold()

        self.beat("b3")
        w = softmax(SCORES)
        total_w = 9.0
        segs = VGroup()
        x = -total_w / 2
        for k in range(n):
            seg = Rectangle(width=max(0.02, w[k] * total_w), height=0.55, stroke_color=S.BG, stroke_width=1.5,
                            fill_color=S.ATTN, fill_opacity=0.3 + 0.7 * w[k] / w.max())
            seg.move_to([x + w[k] * total_w / 2, -2.4, 0])
            x += w[k] * total_w
            segs.add(seg)
        f2 = M(r"\mathrm{softmax}(s)_i = \frac{e^{s_i}}{\sum_j e^{s_j}}", 40).move_to([4.2, 1.2, 0])
        pct = T(f"animal: {w[1]*100:.0f}%", S.SMALL, S.TEXT, weight="BOLD").next_to(segs[1], DOWN, buff=0.2)
        one = T("adds up to 1", S.TINY, S.MUTED).next_to(segs, RIGHT, buff=0.2)
        self.play(ReplacementTransform(new.copy(), segs), ReplacementTransform(f1, f2), run_time=self.dur(0.4))
        self.play(FadeIn(pct), FadeIn(one), run_time=0.6)
        self.hold()

        self.beat("b4")
        f3 = M(r"\mathrm{softmax}\!\left(\frac{Q K^{\top}}{\sqrt{d}}\right)", 48, S.ATTN).move_to([4.2, 1.2, 0])
        note = T("d = length of each Q/K vector", S.TINY, S.MUTED).next_to(f3, DOWN, buff=0.25)
        self.play(ReplacementTransform(f2, f3), run_time=self.dur(0.35))
        self.play(FadeIn(note), run_time=0.5)
        self.hold()

        self.beat("b5")
        self.play(FadeOut(VGroup(new, axis, lab, segs, pct, one, f3, note)), run_time=0.5)
        row2 = row.copy()
        self.play(row.animate.move_to(ORIGIN + DOWN * 0.8), run_time=0.6)
        full = np.zeros(11)
        full[:n] = w
        arcs = attention_arcs(row[IT], [row[k] for k in range(IT)], full[:IT] / full.max(), max_width=12)
        self.play(row[IT].glow(S.QCOL, 0.5), LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.1),
                  run_time=self.dur(0.5))
        self.hold()
        self.play(FadeOut(arcs), run_time=0.4)
        self.finish(tail=0.1)


class S0405WeightedValues(DocScene):
    SCENE_ID = "s0405"

    def construct(self):
        row = sentence_row(S.BODY).arrange(RIGHT, buff=0.3).scale(0.8).move_to(DOWN * 0.8)
        self.add(row)
        w = softmax(SCORES)
        self.beat("b1")
        vs = VGroup(*[vec_icon(S.VCOL, 3, 0.2).next_to(row[k], DOWN, buff=0.3) for k in range(IT + 1)])
        self.play(LaggedStart(*[FadeIn(v) for v in vs], lag_ratio=0.1), run_time=self.dur(0.25))
        self.play(*[v.animate.scale(0.4 + 1.6 * w[k] / w.max()) for k, v in enumerate(vs)], run_time=self.dur(0.25))
        target = row[IT].get_center() + UP * 1.6
        newv = vec_icon(S.VCOL, 3, 0.3).move_to(target)
        self.play(*[v.animate.move_to(target).set_opacity(0.0) for v in vs], FadeIn(newv), run_time=self.dur(0.35))
        self.hold()

        self.beat("b2")
        ax = Axes(x_range=[-3, 3, 1], y_range=[-3, 3, 1], x_length=4.4, y_length=3.6,
                  axis_config={"color": S.DIM, "stroke_width": 1.5, "include_ticks": False}).move_to([4.2, 1.6, 0])
        self.play(FadeOut(newv), row.animate.move_to(DOWN * 2.6), Create(ax), run_time=0.6)
        an = Arrow(ax.c2p(0, 0), ax.c2p(*VEC2["animal"]), buff=0, color=S.TOKEN, stroke_width=4)
        anl = T("animal", S.SMALL, S.TOKEN).next_to(an.get_end(), UR, buff=0.05)
        itv = Arrow(ax.c2p(0, 0), ax.c2p(*VEC2["it"]), buff=0, color=S.QCOL, stroke_width=4)
        itl = T("it", S.SMALL, S.QCOL).next_to(itv.get_end(), UL, buff=0.05)
        self.play(GrowArrow(an), FadeIn(anl), GrowArrow(itv), FadeIn(itl), run_time=0.8)
        newp = (0.72 * np.array(VEC2["animal"]) + 0.28 * np.array(VEC2["it"]))
        it2 = Arrow(ax.c2p(0, 0), ax.c2p(*newp), buff=0, color=S.QCOL, stroke_width=5)
        self.play(Transform(itv, it2), itl.animate.next_to(ax.c2p(*newp), DOWN, buff=0.15), run_time=self.dur(0.4))
        side = T("“it”, now carrying “animal”", S.SMALL, S.QCOL).move_to([-3.2, 1.6, 0])
        self.play(FadeIn(side), run_time=0.6)
        self.hold()

        self.beat("b3")
        self.play(FadeOut(VGroup(ax, an, anl, itv, itl, side)), run_time=0.5)
        eq = M(r"\mathrm{Attention}(Q,K,V) \;=\; \mathrm{softmax}\!\left(\frac{Q K^{\top}}{\sqrt{d}}\right) V", 52)
        fit_width(eq)
        eq.move_to(UP * 0.8)
        self.play(Write(eq), run_time=self.dur(0.6))
        src = T("Vaswani et al., “Attention Is All You Need”, 2017", S.TINY, S.MUTED).next_to(eq, DOWN, buff=0.4)
        self.play(FadeIn(src), run_time=0.5)
        self.hold()

        self.beat("b4")
        items = VGroup(*[M(t, 36, S.TEXT) for t in (r"Q = XW_Q", r"K = XW_K", r"V = XW_V", r"QK^{\top}",
                                                        r"(\cdot)\,V")]).arrange(RIGHT, buff=0.7)
        fit_width(items)
        items.next_to(src, DOWN, buff=0.7)
        self.play(FadeIn(items), run_time=0.5)
        for it in items:
            self.play(it.animate(rate_func=there_and_back).set_color(S.COMPUTE).scale(1.15), run_time=self.dur(0.1, lo=0.35))
        tag = T("5 matrix multiplications", S.SMALL, S.COMPUTE, weight="BOLD").next_to(items, DOWN, buff=0.4)
        self.play(FadeIn(tag), items.animate.set_color(S.COMPUTE), run_time=0.6)
        self.hold()
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.finish(tail=0.1)


def _head_pattern(kind, n=11):
    m = np.zeros((n, n))
    for i in range(n):
        if kind == "prev":
            m[i, max(0, i - 1)] = 1
        elif kind == "pron":
            m[i, i] = 0.4
            if i == IT:
                m[i, :] = 0
                m[i, 1] = 1
        elif kind == "verb":
            m[i, i] = 0.3
            if i >= 3:
                m[i, 1] = 0.7 if i in (3, 8) else 0.2
        elif kind == "first":
            m[i, 0] = 0.8
            m[i, i] = 0.3
    return m


class S0406HeadsAndFFN(DocScene):
    SCENE_ID = "s0406"

    def construct(self):
        self.beat("b1")
        hm = Heatmap(causal_matrix(), cell=0.36)
        self.play(FadeIn(hm), run_time=0.6)
        heads = VGroup(*[Heatmap(_head_pattern(k), cell=0.2) for k in ("pron", "prev", "verb", "first")])
        heads.arrange(RIGHT, buff=0.6).move_to(UP * 0.4)
        self.play(ReplacementTransform(VGroup(*[hm.copy() for _ in range(4)]), heads), FadeOut(hm),
                  run_time=self.dur(0.4))
        hl = VGroup(*[T(f"head {k+1}", S.SMALL, S.ATTN).next_to(h, UP, buff=0.2) for k, h in enumerate(heads)])
        self.play(FadeIn(hl), run_time=0.5)
        self.hold()

        self.beat("b2")
        caps = ["pronoun → noun", "previous word", "subject ↔ verb", "sentence start"]
        cl = VGroup(*[T(c, S.SMALL, S.TEXT).next_to(h, DOWN, buff=0.25) for c, h in zip(caps, heads)])
        il = chip("illustrative patterns", S.MUTED).to_edge(DOWN, buff=0.9)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cl], lag_ratio=0.3), FadeIn(il),
                  run_time=self.dur(0.6))
        self.hold()

        self.beat("b3")
        self.play(FadeOut(VGroup(heads, hl, cl, il)), run_time=0.5)
        blk = Block(w=3.4, h=0.7).move_to([-3.8, 0.2, 0])
        self.play(FadeIn(blk), run_time=0.6)
        v1 = vec_column([""] * 4, color=S.TOKEN, cell=0.36)
        wide = vec_column([""] * 12, color=S.PARAM, cell=0.36)
        v2 = vec_column([""] * 4, color=S.TOKEN, cell=0.36)
        grp = VGroup(v1, wide, v2).arrange(RIGHT, buff=1.4).move_to([2.6, 0.1, 0])
        a1 = Arrow(v1.get_right(), wide.get_left(), buff=0.15, color=S.PARAM)
        a2 = Arrow(wide.get_right(), v2.get_left(), buff=0.15, color=S.PARAM)
        l1 = M("W_1", 34, S.PARAM).next_to(a1, UP, buff=0.1)
        l2 = M("W_2", 34, S.PARAM).next_to(a2, UP, buff=0.1)
        zoom = DashedLine(blk.ffn.get_right(), grp.get_left() + LEFT * 0.2, color=S.MUTED)
        self.play(Indicate(blk.ffn, color=S.PARAM), Create(zoom), run_time=0.7)
        self.play(FadeIn(v1), run_time=0.3)
        self.play(GrowArrow(a1), FadeIn(l1), FadeIn(wide), run_time=self.dur(0.2))
        self.play(GrowArrow(a2), FadeIn(l2), FadeIn(v2), run_time=self.dur(0.2))
        talk = T("attention: tokens talk", S.SMALL, S.ATTN).next_to(blk, UP, buff=0.3)
        think = T("feed-forward: each token thinks", S.SMALL, S.PARAM).next_to(blk, DOWN, buff=0.3)
        self.play(FadeIn(talk), FadeIn(think), run_time=0.6)
        self.hold()

        self.beat("b4")
        self.play(FadeOut(VGroup(v1, wide, v2, a1, a2, l1, l2, zoom, talk, think)), run_time=0.5)
        tot = 7.0
        fb = Rectangle(width=tot * 2 / 3, height=0.6, stroke_width=0, fill_color=S.PARAM, fill_opacity=0.85)
        ab = Rectangle(width=tot / 3, height=0.6, stroke_width=0, fill_color=S.ATTN, fill_opacity=0.85)
        bar = VGroup(fb, ab).arrange(RIGHT, buff=0).move_to([1.8, 0.2, 0])
        fl = T("feed-forward", S.SMALL, S.PARAM).next_to(fb, DOWN, buff=0.2)
        al = T("attention", S.SMALL, S.ATTN).next_to(ab, DOWN, buff=0.2)
        head = T("where the parameters live (typical dense model)", S.SMALL, S.MUTED).next_to(bar, UP, buff=0.3)
        fit_width(head, 7.5)
        self.play(GrowFromEdge(fb, LEFT), GrowFromEdge(ab, LEFT), FadeIn(fl), FadeIn(al), FadeIn(head),
                  run_time=self.dur(0.5))
        self.play(Indicate(fb, color=S.PARAM, scale_factor=1.05), Indicate(blk.ffn, color=S.PARAM), run_time=1.0)
        self.hold()
        self.play(FadeOut(VGroup(bar, fl, al, head)), blk.animate.move_to(ORIGIN + DOWN * 2.2), run_time=0.6)
        self.finish(tail=0.1)


class S0407TheStack(DocScene):
    SCENE_ID = "s0407"

    def construct(self):
        blk = Block(w=3.4, h=0.7).move_to(ORIGIN + DOWN * 2.2)
        self.add(blk)
        self.beat("b1")
        blocks = VGroup(*[Block(w=3.0, h=0.2, label_size=S.TINY, attn_label="", ffn_label="") for _ in range(9)])
        blocks.arrange(UP, buff=0.12).move_to([-1.6, -0.3, 0])
        self.play(ReplacementTransform(blk, blocks[0]), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in blocks[1:]], lag_ratio=0.2),
                  run_time=self.dur(0.5))
        lab = T("× dozens of blocks", S.SMALL, S.MUTED).next_to(blocks, LEFT, buff=0.3)
        self.play(FadeIn(lab), run_time=0.4)
        self.hold()

        self.beat("b2")
        inp = TokenRow(["because", "it", "was", "tired"], size=S.SMALL).next_to(blocks, DOWN, buff=0.35)
        self.play(FadeIn(inp), run_time=0.5)
        probs = prob_bars(["and", ".", "so", "but", "then"], [0.41, 0.22, 0.12, 0.08, 0.05], color=S.TOKEN,
                          max_h=2.6)
        probs.move_to([3.3, 0.2, 0])
        arr = Arrow(blocks.get_right() + UP * 0.8, probs.get_left() + UP * 0.2, color=S.MUTED, buff=0.2)
        pl = T("next-token probabilities (illustrative)", S.TINY, S.MUTED).next_to(probs, UP, buff=0.3)
        self.play(LaggedStart(*[b.attn.animate(rate_func=there_and_back).set_fill(opacity=0.6) for b in blocks],
                              lag_ratio=0.1), run_time=self.dur(0.35))
        self.play(GrowArrow(arr), FadeIn(probs, lag_ratio=0.2), FadeIn(pl), run_time=self.dur(0.4))
        self.hold()

        self.beat("b3")
        chosen = probs[0][1].copy()
        new_tok = Token("and", S.SMALL).next_to(inp, RIGHT, buff=0.1)
        self.play(Indicate(probs[0]), run_time=0.6)
        self.play(ReplacementTransform(chosen, new_tok), run_time=self.dur(0.25))
        self.play(LaggedStart(*[b.animate(rate_func=there_and_back).set_opacity(0.4) for b in blocks],
                              lag_ratio=0.08), run_time=self.dur(0.3))
        one = T("one token at a time", S.BODY, S.TEXT, weight="BOLD").to_edge(UP, buff=0.7)
        self.play(FadeIn(one), run_time=0.5)
        self.hold()

        self.beat("b4")
        self.allow_small = True  # deliberate pull-back
        self.play(self.camera.frame.animate.scale(2.2), run_time=self.dur(0.5))
        name = T("a Transformer", 90, S.TEXT, weight="BOLD").move_to(self.camera.frame.get_center() + UP * 6.0)
        self.play(FadeIn(name), run_time=0.8)
        self.hold()
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.finish(tail=0.1)
