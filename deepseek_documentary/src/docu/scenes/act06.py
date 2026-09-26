"""ACT 6 — Mixture of Experts."""
import numpy as np
from manim import *  # noqa: F401,F403

from docu import style as S
from docu.base_scene import DocScene
from docu.components import (GPU, Block, Expert, ExpertGrid, M, MatrixGrid, Router, SharedExpert, T, Token, caption,
                             chip, fit_width, softmax, source_line, vec_column)


def expert_row(n=8, w=1.05, h=0.95, labels=True):
    return VGroup(*[Expert(f"E{k+1}" if labels else None, w=w, h=h) for k in range(n)]).arrange(RIGHT, buff=0.22)


class S0601SplitTheNetwork(DocScene):
    SCENE_ID = "s0601"

    def construct(self):
        self.beat("b1")
        blk = Block(w=9.6, h=1.0, label_size=S.BODY).move_to(DOWN * 0.2)
        self.play(FadeIn(blk), run_time=0.6)
        self.play(Indicate(blk.ffn, color=S.PARAM, scale_factor=1.03), run_time=self.dur(0.5))
        self.hold()

        self.beat("b2")
        ex = expert_row().move_to(blk.ffn)
        self.play(FadeOut(blk.ffn_t), ReplacementTransform(blk.ffn, ex), run_time=self.dur(0.4))
        el = T("experts", S.BODY, S.EXPERT, weight="BOLD").next_to(ex, DOWN, buff=0.35)
        self.play(FadeIn(el), run_time=0.6)
        self.hold()

        self.beat("b3")
        self.play(ex[1].on(), ex[5].on(), *[e.box.animate.set_opacity(0.25) for k, e in enumerate(ex)
                                             if k not in (1, 5)], run_time=self.dur(0.4))
        self.hold()

        self.beat("b4")
        stored = T("stored: 8 experts", S.BODY, S.TEXT).move_to([-3, -2.6, 0])
        comp = T("computed per token: 2", S.BODY, S.EXPERT, weight="BOLD").move_to([3, -2.6, 0])
        title = T("Mixture of Experts  (MoE)", S.H2, S.EXPERT, weight="BOLD").to_edge(UP, buff=0.7)
        self.play(FadeOut(el), FadeIn(stored), FadeIn(comp), run_time=self.dur(0.35))
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.7)
        self.hold()
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.finish(tail=0.1)


class S0602TheRouter(DocScene):
    SCENE_ID = "s0602"

    def construct(self):
        ex = expert_row().move_to(DOWN * 2.1)
        self.add(ex)
        self.beat("b1")
        slot = UP * 2.5
        tok = Token("?", S.BODY).move_to(slot)
        self.play(FadeIn(tok, shift=DOWN * 0.2), run_time=self.dur(0.4))
        self.hold()

        self.beat("b2")
        router = Router(0.5).move_to(UP * 0.7)
        a = Arrow(tok.get_bottom(), router.diamond.get_top(), buff=0.1, color=S.TOKEN)
        self.play(FadeIn(router), GrowArrow(a), run_time=self.dur(0.3))
        rng = np.random.default_rng(1)
        sc = rng.uniform(0.2, 0.8, 8)
        bars = VGroup(*[Rectangle(width=0.5, height=0.7 * s, stroke_width=0, fill_color=S.ROUTER, fill_opacity=0.7)
                        .next_to(e, UP, buff=0.12) for s, e in zip(sc, ex)])
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1), run_time=self.dur(0.4))
        self.hold()

        routes = {"integral": (1, 4), "def": (0, 6), "mitochondria": (2, 5), "the": (3, 7)}
        self.beat("b3")
        cur = self._route(tok, router, ex, bars, "integral", routes["integral"], self.dur(0.8))
        self.hold()

        self.beat("b4")
        for w in ("def", "mitochondria", "the"):
            cur = self._route(cur, router, ex, bars, w, routes[w], self.dur(0.3, lo=1.0))
        self.hold()

        self.beat("b5")
        topics = ["code?", "maths?", "biology?", "grammar?", "maths?", "biology?", "code?", "grammar?"]
        tl = VGroup(*[T(t, S.TINY, S.MUTED).next_to(e, DOWN, buff=0.15) for t, e in zip(topics, ex)])
        self.play(FadeIn(tl), run_time=self.dur(0.25))
        q = VGroup(*[T("?", S.SMALL, S.MUTED).move_to(t) for t in tl])
        self.play(ReplacementTransform(tl, q), run_time=self.dur(0.25))
        il = chip("real specialisation is learned, and rarely tidy", S.MUTED).to_edge(UP, buff=0.3).shift(RIGHT * 2.6)
        self.play(FadeIn(il), run_time=0.6)
        self.hold()
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.finish(tail=0.1)

    def _route(self, old, router, ex, bars, word, pair, rt):
        tok = Token(word, S.BODY).move_to(UP * 2.5)
        new_h = [0.15] * 8
        for k in pair:
            new_h[k] = 0.85
        anims = [ReplacementTransform(old, tok)]
        anims += [b.animate.stretch_to_fit_height(0.7 * h).next_to(e, UP, buff=0.12)
                  for b, h, e in zip(bars, new_h, ex)]
        anims += [e.off() for k, e in enumerate(ex) if k not in pair]
        anims += [ex[k].on() for k in pair]
        self.play(*anims, run_time=max(0.6, rt * 0.6))
        arrows = VGroup(*[Arrow(router.diamond.get_bottom(), ex[k].get_top() + UP * 0.8, buff=0.05,
                                color=S.EXPERT, stroke_width=3) for k in pair])
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.3), run_time=max(0.4, rt * 0.3))
        self.play(FadeOut(arrows), run_time=0.3)
        return tok


class S0603RoutingMath(DocScene):
    SCENE_ID = "s0603"

    def construct(self):
        self.beat("b1")
        Wr = MatrixGrid(rows=8, cols=4, cell=0.44, color=S.ROUTER, show_numbers=False)
        x = vec_column([""] * 4, color=S.TOKEN, cell=0.44)
        s_vals = np.array([0.3, 2.1, -0.4, 0.2, 1.6, -0.8, 0.5, 0.1])
        s = vec_column([f"{v:.1f}" for v in s_vals], color=S.ROUTER, cell=0.56, num_size=S.SMALL)
        eq = VGroup(Wr, x, M("=", 44), s).arrange(RIGHT, buff=0.35).move_to([-3.2, 0.2, 0])
        lab = M(r"s = W_r\,x", 48).move_to([2.8, 1.6, 0])
        l1 = M("W_r", 34, S.ROUTER).next_to(Wr, UP, buff=0.2)
        l2 = M("x", 34, S.TOKEN).next_to(x, UP, buff=0.2)
        l3 = T("one score per expert", S.TINY, S.MUTED).next_to(s, RIGHT, buff=0.25)
        self.play(FadeIn(Wr), FadeIn(x), FadeIn(l1), FadeIn(l2), run_time=0.6)
        self.play(FadeIn(eq[2]), FadeIn(s), FadeIn(l3), Write(lab), run_time=self.dur(0.5))
        self.hold()

        self.beat("b2")
        g = softmax(s_vals)
        bars = VGroup(*[Rectangle(width=0.4, height=max(0.04, 3.2 * v), stroke_width=0, fill_color=S.EXPERT,
                                  fill_opacity=0.8) for v in g]).arrange(RIGHT, buff=0.18, aligned_edge=DOWN)
        bars.move_to([2.8, -0.9, 0])
        names = VGroup(*[T(f"E{k+1}", S.TINY, S.TEXT).next_to(b, DOWN, buff=0.12) for k, b in enumerate(bars)])
        f2 = M(r"g = \mathrm{top\text{-}k}\big(\mathrm{softmax}(s)\big)", 40).move_to(lab)
        self.play(ReplacementTransform(lab, f2), FadeIn(bars, lag_ratio=0.1), FadeIn(names), run_time=self.dur(0.4))
        top = np.argsort(-g)[:2]
        self.play(*[bars[k].animate.set_opacity(0.15) for k in range(8) if k not in top],
                  *[names[k].animate.set_opacity(0.3) for k in range(8) if k not in top], run_time=self.dur(0.25))
        kl = T("top-k, k = 2", S.SMALL, S.EXPERT).next_to(bars, UP, buff=0.3)
        self.play(FadeIn(kl), run_time=0.5)
        self.hold()

        self.beat("b3")
        self.play(FadeOut(VGroup(Wr, x, eq[2], s, l1, l2, l3)), run_time=0.5)
        f3 = M(r"y = \sum_{i \in \text{top-}k} g_i \, E_i(x)", 48).move_to([-3.2, 1.5, 0])
        e1 = Expert("E2", 1.2, 1.0).move_to([-4.6, -0.5, 0])
        e2 = Expert("E5", 1.2, 1.0).move_to([-2.0, -0.5, 0])
        o1 = Square(0.4, stroke_width=0, fill_color=S.EXPERT, fill_opacity=0.9).next_to(e1, DOWN, buff=0.3)
        o2 = Square(0.4, stroke_width=0, fill_color=S.EXPERT, fill_opacity=0.9).next_to(e2, DOWN, buff=0.3)
        y = Square(0.5, stroke_width=0, fill_color=S.EXPERT, fill_opacity=1).move_to([-3.3, -2.6, 0])
        yl = M("y", 36).next_to(y, RIGHT, buff=0.2)
        self.play(Write(f3), FadeIn(e1), FadeIn(e2), run_time=self.dur(0.35))
        self.play(FadeIn(o1), FadeIn(o2), run_time=0.4)
        self.play(o1.animate.scale(g[top[0]] / g[top].max()).move_to(y), o2.animate.scale(g[top[1]] / g[top].max()).move_to(y),
                  FadeIn(y), FadeIn(yl), run_time=self.dur(0.3))
        self.hold()

        self.beat("b4")
        self.play(FadeOut(VGroup(f3, e1, e2, o1, o2, y, yl, bars, names, kl, f2)), run_time=0.5)
        ex = expert_row(8, 1.0, 0.8).move_to(UP * 1.4)
        loads = VGroup(*[Rectangle(width=0.7, height=0.3, stroke_width=0, fill_color=S.EXPERT, fill_opacity=0.8)
                         .next_to(e, DOWN, buff=0.25, aligned_edge=DOWN) for e in ex])
        for l, e in zip(loads, ex):
            l.move_to([e.get_x(), -2.3, 0], aligned_edge=DOWN)
        base = Line([-5.6, -2.3, 0], [5.6, -2.3, 0], color=S.MUTED, stroke_width=1.5)
        ll = T("load", S.SMALL, S.MUTED).next_to(base, LEFT, buff=0.2)
        self.play(FadeIn(ex), Create(base), FadeIn(loads), FadeIn(ll), run_time=0.6)
        toks = VGroup(*[Token("", S.TINY).scale(0.45).move_to([-6 + 0.35 * k, 3.3, 0]) for k in range(20)])
        self.add(toks)
        self.play(LaggedStart(*[t.animate.move_to(ex[2].get_center()).set_opacity(0) for t in toks], lag_ratio=0.05),
                  loads[2].animate.stretch_to_fit_height(3.0).move_to([ex[2].get_x(), -2.3, 0], aligned_edge=DOWN)
                  .set_fill(S.LOSS), *[loads[k].animate.stretch_to_fit_height(0.05).move_to(
                      [ex[k].get_x(), -2.3, 0], aligned_edge=DOWN) for k in range(8) if k != 2],
                  run_time=self.dur(0.55))
        # loads grow downward from baseline: flip visual below axis
        warn = T("one overloaded expert, seven idle", S.SMALL, S.LOSS).move_to([0, -2.95, 0])
        self.play(FadeIn(warn), run_time=0.5)
        self.hold()

        self.beat("b5")
        arrows = VGroup(*[Arrow(e.get_top() + UP * (0.5 if k == 2 else 0.05), e.get_top() + UP * (0.05 if k == 2 else 0.5),
                                buff=0, color=S.LOSS if k == 2 else S.EXPERT, stroke_width=3)
                          for k, e in enumerate(ex)])
        bias = T("per-expert bias nudges the router", S.SMALL, S.TEXT).to_edge(UP, buff=0.3)
        self.play(FadeIn(arrows), FadeIn(bias), FadeOut(warn), run_time=self.dur(0.25))
        self.play(*[l.animate.stretch_to_fit_height(0.9).move_to([e.get_x(), -2.3, 0], aligned_edge=DOWN)
                    .set_fill(S.EXPERT) for l, e in zip(loads, ex)], run_time=self.dur(0.35))
        mm = T("V4.1-Flash: separate biases for text and image tokens", S.SMALL, S.EXPERT).move_to([0, 3.0, 0])
        src = source_line("DeepSeek-V4.1-Flash paper §2.1.1 (auxiliary-loss-free load balancing)")
        self.play(FadeIn(mm), FadeIn(src), run_time=0.6)
        self.hold()
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.finish(tail=0.1)


class S0604DeepSeekMoE(DocScene):
    SCENE_ID = "s0604"

    def construct(self):
        self.beat("b1")
        ex = expert_row(8, 1.05, 0.95).move_to(UP * 0.2)
        self.play(FadeIn(ex), run_time=0.5)
        fine = ExpertGrid(64, cols=16, size=0.3, gap=0.08).move_to(UP * 0.2)
        self.play(ReplacementTransform(ex, fine), run_time=self.dur(0.4))
        lab = T("many small experts", S.SMALL, S.EXPERT).next_to(fine, DOWN, buff=0.35)
        self.play(FadeIn(lab), run_time=0.5)
        self.hold()

        self.beat("b2")
        sh = SharedExpert(w=0.9, h=fine.height + 0.2).next_to(fine, LEFT, buff=0.5)
        tok = Token("token", S.SMALL).to_edge(UP, buff=0.7)
        line = Arrow(tok.get_bottom(), sh.get_top(), buff=0.1, color=S.EXPERT)
        self.play(FadeIn(sh), FadeIn(tok), GrowArrow(line), run_time=self.dur(0.35))
        al = T("every token, always", S.SMALL, S.EXPERT).next_to(sh, DOWN, buff=0.35)
        self.play(FadeOut(lab), FadeIn(al), sh.box.animate.set_fill(opacity=0.7), run_time=0.6)
        self.hold()

        self.beat("b3")
        self.play(FadeOut(VGroup(fine, sh, tok, line, al)), run_time=0.5)
        v2 = self._bars("DeepSeek-V2", 236, 21, "B")
        self.play(FadeIn(v2[0]), run_time=0.5)
        self.play(GrowFromEdge(v2[1], LEFT), run_time=0.6)
        self.play(GrowFromEdge(v2[2], LEFT), FadeIn(v2[3]), run_time=self.dur(0.3))
        self.hold()

        self.beat("b4")
        self.play(FadeOut(v2), run_time=0.4)
        g256 = ExpertGrid(256, cols=32, size=0.2, gap=0.06).move_to([0.6, 0.5, 0])
        sh = SharedExpert(w=0.7, h=g256.height + 0.1).next_to(g256, LEFT, buff=0.35)
        title = T("DeepSeek-V3: 256 routed + 1 shared expert per MoE layer", S.SMALL, S.TEXT).to_edge(UP, buff=0.6)
        fit_width(title)
        self.play(FadeIn(g256, lag_ratio=0.002), FadeIn(sh), FadeIn(title), run_time=self.dur(0.35))
        rng = np.random.default_rng(7)
        pick = rng.choice(256, 8, replace=False)
        self.play(*[g256.cells[k].animate.set_fill(S.EXPERT, opacity=1).set_stroke(width=2) for k in pick],
                  sh.box.animate.set_fill(opacity=0.7), run_time=self.dur(0.3))
        eight = T("8 of 256 routed experts per token", S.SMALL, S.EXPERT, weight="BOLD").next_to(g256, DOWN, buff=0.4)
        self.play(FadeIn(eight), run_time=0.5)
        src = source_line("DeepSeek-V3 official config (config_671B.json)")
        self.add(src)
        self.hold()

        self.beat("b5")
        self.play(FadeOut(VGroup(g256, sh, eight, title, src)), run_time=0.5)
        v3 = self._bars("DeepSeek-V3", 671, 37, "B")
        self.play(FadeIn(v3[0]), GrowFromEdge(v3[1], LEFT), run_time=self.dur(0.35))
        self.play(GrowFromEdge(v3[2], LEFT), FadeIn(v3[3]), run_time=self.dur(0.25))
        pct = T("≈ 5.5% active per token", S.BODY, S.EXPERT, weight="BOLD").next_to(v3, DOWN, buff=0.5)
        self.play(FadeIn(pct), run_time=0.5)
        self.hold()

        self.beat("b6")
        self.play(FadeOut(VGroup(v3, pct)), run_time=0.4)
        g384 = ExpertGrid(384, cols=32, size=0.18, gap=0.05).move_to([0.5, 0.3, 0])
        sh = SharedExpert(w=0.6, h=g384.height + 0.1).next_to(g384, LEFT, buff=0.3)
        title = T("DeepSeek-V4.1-Flash: 384 routed + 1 shared · 6 active", S.SMALL, S.TEXT).to_edge(UP, buff=0.6)
        fit_width(title)
        pick = rng.choice(384, 6, replace=False)
        self.play(FadeIn(g384, lag_ratio=0.002), FadeIn(sh), FadeIn(title), run_time=self.dur(0.35))
        self.play(*[g384.cells[k].animate.set_fill(S.EXPERT, opacity=1).set_stroke(width=2) for k in pick],
                  sh.box.animate.set_fill(opacity=0.7), run_time=self.dur(0.3))
        src = source_line("DeepSeek-V4.1-Flash paper §4.2.1")
        self.add(src)
        self.hold()

        self.beat("b7")
        self.play(FadeOut(VGroup(sh, title, src)), run_time=0.4)
        gpus = VGroup(*[GPU(w=2.7, h=1.9, cores=(2, 3), core_opacity=0.08) for _ in range(4)])
        gpus.arrange_in_grid(2, 2, buff=(0.8, 0.6)).move_to(DOWN * 0.1)
        cells = list(g384.cells)
        groups = [VGroup(*cells[k * 96:(k + 1) * 96]) for k in range(4)]
        gpus.set_z_index(0)
        for grp in groups:
            grp.set_z_index(3)
        self.play(FadeIn(gpus), *[grp.animate.arrange_in_grid(8, 12, buff=0.04).scale_to_fit_width(2.2).move_to(g.die)
                                  for grp, g in zip(groups, gpus)], run_time=self.dur(0.5))
        q = T("Where do all these experts actually live?", S.BODY, S.TEXT, weight="BOLD").to_edge(UP, buff=0.5)
        self.play(FadeIn(q), run_time=0.6)
        self.hold()
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.finish(tail=0.1)

    def _bars(self, name, total, active, unit):
        L = 9.0
        t = T(name, S.BODY, S.TEXT, weight="BOLD")
        tb = Rectangle(width=L, height=0.7, stroke_color=S.PARAM, stroke_width=2, fill_color=S.PARAM, fill_opacity=0.15)
        ab = Rectangle(width=L * active / total, height=0.7, stroke_width=0, fill_color=S.EXPERT, fill_opacity=0.95)
        g = VGroup(t, tb).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        ab.move_to(tb, aligned_edge=LEFT)
        labels = VGroup(T(f"{total}{unit} total parameters", S.SMALL, S.PARAM).next_to(tb, DOWN, buff=0.15,
                                                                                     aligned_edge=RIGHT),
                        T(f"{active}{unit} active per token", S.SMALL, S.EXPERT, weight="BOLD").next_to(tb, DOWN,
                                                                                                        buff=0.15,
                                                                                                        aligned_edge=LEFT))
        grp = VGroup(t, tb, ab, labels).move_to(ORIGIN)
        return grp
