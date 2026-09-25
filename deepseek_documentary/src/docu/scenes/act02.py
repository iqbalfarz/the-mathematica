"""ACT 2 — What does 'compute' even mean?"""
import numpy as np
from manim import *  # noqa: F401,F403

from docu import style as S
from docu.base_scene import DocScene
from docu.components import (GPU, LayerTower, M, MatrixGrid, Neuron, T, caption, cell_grid, chip, fit_width,
                             safe_right, safe_top, source_line, vec_column, vec_row)

W3 = np.array([[4, -2, 5], [1, 0, 2], [-1, 3, 1]])
X3 = np.array([[3, 0, 1], [1, 2, 0], [2, 1, 1]])


class S0201OneMultiplication(DocScene):
    SCENE_ID = "s0201"

    def construct(self):
        self.beat("b1")
        dot = Dot(ORIGIN, radius=0.08, color=S.TEXT)
        self.add(dot)
        expr = M(r"3 \times 4", 120)
        self.play(ReplacementTransform(dot, expr), run_time=self.dur(0.4))
        self.hold()

        self.beat("b2")
        full = M(r"3 \times 4 = 12", 120)
        self.play(TransformMatchingTex(expr, full), run_time=self.dur(0.3))
        ops = chip("1 operation", S.COMPUTE).next_to(full, DOWN, buff=0.7)
        self.play(FadeIn(ops, shift=UP * 0.2), run_time=0.6)
        self.hold()

        self.beat("b3")
        self.play(FadeOut(ops), full.animate.shift(UP * 0.6), run_time=0.6)
        three, four = full[0][0], full[0][2]
        l1 = T("input  x", S.SMALL, S.TOKEN).next_to(three, DOWN, buff=0.5)
        l2 = T("weight  w", S.SMALL, S.PARAM).next_to(four, DOWN, buff=0.5)
        l2.shift(RIGHT * 0.4)
        self.play(three.animate.set_color(S.TOKEN), FadeIn(l1, shift=UP * 0.2), run_time=self.dur(0.25))
        self.play(four.animate.set_color(S.PARAM), FadeIn(l2, shift=UP * 0.2), run_time=self.dur(0.25))
        self.hold()

        self.beat("b4")
        self.play(FadeOut(VGroup(full, l1, l2)), run_time=0.5)
        n = Neuron(inputs=("3", "1", "2"), weights=("4", "−2", "5"))
        self.play(FadeIn(n.inputs), run_time=0.5)
        self.play(Create(n.edges), FadeIn(n.wlabels), run_time=self.dur(0.2))
        self.play(Create(n.node), FadeIn(n.sigma), run_time=0.6)
        prods = VGroup(*[T(p, S.SMALL, S.COMPUTE, mono=True) for p in ("12", "−2", "10")])
        for p, e in zip(prods, n.edges):
            p.move_to(e.point_from_proportion(0.14) + DOWN * 0.3)
        self.play(LaggedStart(*[FadeIn(p, scale=1.3) for p in prods], lag_ratio=0.4), run_time=self.dur(0.25))
        res = T("20", S.H2, S.TEXT, weight="BOLD", mono=True).next_to(n.out, RIGHT, buff=0.2)
        self.play(GrowArrow(n.out), *[p.animate.move_to(n.node).set_opacity(0) for p in prods],
                  FadeIn(res), run_time=self.dur(0.2))
        self.hold()

        self.beat("b5")
        lab = T("parameters = the weights", S.BODY, S.PARAM, weight="BOLD").to_edge(UP, buff=0.9)
        self.play(n.edges.animate.set_stroke(width=6), n.wlabels.animate.scale(1.25), FadeIn(lab, shift=DOWN * 0.2),
                  run_time=self.dur(0.4))
        self.hold()
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.finish(tail=0.1)


class S0202DotProduct(DocScene):
    SCENE_ID = "s0202"

    def construct(self):
        self.beat("b1")
        n = Neuron(inputs=("3", "1", "2"), weights=("4", "−2", "5"))
        self.add(n)
        w = vec_row([4, "−2", 5], color=S.PARAM, cell=0.8, num_size=S.BODY)
        x = vec_column([3, 1, 2], color=S.TOKEN, cell=0.8, num_size=S.BODY)
        dotm = M(r"\cdot", 80)
        grp = VGroup(w, dotm, x).arrange(RIGHT, buff=0.4).shift(UP * 1.7)
        self.play(ReplacementTransform(n, grp), run_time=self.dur(0.5))
        self.hold()

        self.beat("b2")
        terms = VGroup()
        prods = ["12", "−2", "10"]
        slots = VGroup(*[T(p, S.BODY, S.COMPUTE, mono=True) for p in prods])
        plus = [T("+", S.BODY, S.MUTED) for _ in range(2)]
        line = VGroup(slots[0], plus[0], slots[1], plus[1], slots[2]).arrange(RIGHT, buff=0.3)
        line.next_to(grp, DOWN, buff=0.6)
        for k in range(3):
            hl = VGroup(SurroundingRectangle(w.cell(0, k), color=S.COMPUTE, buff=0.03),
                        SurroundingRectangle(x.cell(k, 0), color=S.COMPUTE, buff=0.03))
            anims = [Create(hl), FadeIn(slots[k], shift=UP * 0.2)]
            if k > 0:
                anims.append(FadeIn(plus[k - 1]))
            self.play(*anims, run_time=self.dur(0.12))
            self.play(FadeOut(hl), run_time=0.25)
        total = T("= 20", S.BODY, S.TEXT, weight="BOLD", mono=True).next_to(line, RIGHT, buff=0.3)
        name = T("dot product", S.SMALL, S.MUTED).next_to(VGroup(line, total), DOWN, buff=0.35)
        self.play(FadeIn(total), FadeIn(name), run_time=self.dur(0.15))
        self.hold()

        self.beat("b3")
        count = VGroup(T("3 multiplies", S.BODY, S.COMPUTE), T("+", S.BODY, S.MUTED), T("2 adds", S.BODY, S.COMPUTE),
                       T("=", S.BODY, S.MUTED), T("5 FLOPs", S.BODY, S.TEXT, weight="BOLD")).arrange(RIGHT, buff=0.25)
        count.next_to(name, DOWN, buff=0.4)
        self.play(FadeIn(count, shift=UP * 0.2), run_time=self.dur(0.3))
        defn = caption("FLOP = one floating-point operation: a single multiply or add")
        self.play(FadeIn(defn), run_time=self.dur(0.2))
        self.hold()

        self.beat("b4")
        unit = T("FLOP", S.SMALL, S.COMPUTE, weight="BOLD").move_to([safe_right() - 0.5, safe_top() - 0.2, 0])
        self.play(count[4].animate.scale(1.25).set_color(S.COMPUTE), run_time=self.dur(0.3))
        self.play(ReplacementTransform(count[4].copy(), unit), run_time=0.8)
        self.hold()
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.finish(tail=0.1)


class S0203MatrixMultiply(DocScene):
    SCENE_ID = "s0203"

    def construct(self):
        self.beat("b1")
        row = vec_row([4, -2, 5], color=S.PARAM, cell=0.7)
        row.move_to(LEFT * 3 + UP * 0.7)
        self.play(FadeIn(row), run_time=0.5)
        W = MatrixGrid(W3, cell=0.7, color=S.PARAM).move_to(LEFT * 3)
        x = vec_column([3, 1, 2], color=S.TOKEN, cell=0.7).next_to(W, RIGHT, buff=0.5)
        wl = M("W", 44, S.PARAM).next_to(W, UP, buff=0.3)
        xl = M("x", 44, S.TOKEN).next_to(x, UP, buff=0.3)
        self.play(ReplacementTransform(row, W), run_time=self.dur(0.35))
        self.play(FadeIn(x), FadeIn(wl), FadeIn(xl), run_time=self.dur(0.2))
        self.hold()

        self.beat("b2")
        eq = M("=", 60).next_to(x, RIGHT, buff=0.45)
        y = MatrixGrid(np.array([["", ], [""], [""]], dtype=object), cell=0.7, color=S.COMPUTE, show_numbers=False)
        y.next_to(eq, RIGHT, buff=0.45)
        yl = M("y", 44, S.COMPUTE).next_to(y, UP, buff=0.3)
        self.play(FadeIn(eq), FadeIn(y), FadeIn(yl), run_time=0.5)
        yvals = [20, 7, 2]
        for i in range(3):
            hl = VGroup(SurroundingRectangle(W.row(i), color=S.COMPUTE, buff=0.04),
                        SurroundingRectangle(x, color=S.COMPUTE, buff=0.04))
            v = T(str(yvals[i]), S.SMALL, S.TEXT, mono=True).move_to(y.cell(i, 0))
            self.play(Create(hl), run_time=self.dur(0.08, lo=0.25))
            self.play(FadeIn(v, scale=1.3), FadeOut(hl), run_time=self.dur(0.12, lo=0.3))
            y.add(v)
        self.hold()

        self.beat("b3")
        X = MatrixGrid(X3, cell=0.7, color=S.TOKEN).move_to(x, aligned_edge=LEFT)
        Xl = M("X", 44, S.TOKEN).next_to(X, UP, buff=0.3)
        eq2 = M("=", 60).next_to(X, RIGHT, buff=0.45)
        Yv = W3 @ X3
        Y = MatrixGrid(np.full((3, 3), "", dtype=object), cell=0.7, color=S.COMPUTE, show_numbers=False)
        Y.next_to(eq2, RIGHT, buff=0.45)
        Yl = M("Y", 44, S.COMPUTE).next_to(Y, UP, buff=0.3)
        self.play(ReplacementTransform(x, X), ReplacementTransform(xl, Xl), FadeOut(VGroup(eq, y, yl)),
                  run_time=self.dur(0.2))
        self.play(FadeIn(eq2), FadeIn(Y), FadeIn(Yl), run_time=0.5)
        cells = []
        for i in range(3):
            for j in range(3):
                cells.append(T(str(Yv[i, j]), S.SMALL, S.TEXT, mono=True).move_to(Y.cell(i, j)))
        hlr = SurroundingRectangle(W.row(0), color=S.COMPUTE, buff=0.04)
        hlc = SurroundingRectangle(X.col(0), color=S.COMPUTE, buff=0.04)
        self.play(Create(hlr), Create(hlc), run_time=0.4)
        step = self.dur(0.5) / 9
        for k, c in enumerate(cells):
            i, j = divmod(k, 3)
            self.play(hlr.animate.move_to(W.row(i)), hlc.animate.move_to(X.col(j)), FadeIn(c, scale=1.3),
                      run_time=max(0.2, step))
        self.play(FadeOut(hlr), FadeOut(hlc), run_time=0.3)
        self.hold()

        self.beat("b4")
        counter = Integer(0, font_size=64, color=S.COMPUTE).to_edge(DOWN, buff=1.5)
        clabel = T("multiplications", S.SMALL, S.MUTED).next_to(counter, RIGHT, buff=0.25)
        clabel.add_updater(lambda m: m.next_to(counter, RIGHT, buff=0.3))
        self.play(FadeIn(counter), FadeIn(clabel), run_time=0.4)
        self.play(ChangeDecimalToValue(counter, 27), run_time=self.dur(0.35))
        rule = M(r"(m\times n)\cdot(n\times p)\;\rightarrow\; m\,n\,p \text{ multiplications}", 36, S.TEXT)
        rule.next_to(counter, DOWN, buff=0.4)
        fit_width(rule)
        self.play(Write(rule), run_time=self.dur(0.3))
        self.hold()
        self.play(FadeOut(Group(*[m for m in self.mobjects if m not in (W,)])), W.animate.move_to(ORIGIN),
                  run_time=0.8)
        self.finish(tail=0.1)


class S0204ScaleExplodes(DocScene):
    SCENE_ID = "s0204"

    def construct(self):
        self.beat("b1")
        W = MatrixGrid(W3, cell=0.7, color=S.PARAM)
        self.add(W)
        big = cell_grid(28, 28, 0.2, color=S.PARAM, stroke=0.5, fill_opacity=0.12)
        self.play(ReplacementTransform(W, big), run_time=self.dur(0.35))
        lab = T("7,168 × 7,168", S.H2, S.PARAM, weight="BOLD", mono=True).next_to(big, UP, buff=0.25)
        sub = T("one DeepSeek-V3 token = 7,168 numbers", S.SMALL, S.MUTED).next_to(big, DOWN, buff=0.25)
        self.play(FadeIn(lab), FadeIn(sub), big.animate.set_stroke(width=0.3), run_time=self.dur(0.4))
        self.hold()

        self.beat("b2")
        grp = VGroup(big, lab)
        self.play(FadeOut(sub), grp.animate.scale(0.62).to_edge(LEFT, buff=0.8), run_time=0.8)
        counter = Integer(27, font_size=72, color=S.COMPUTE, group_with_commas=True)
        counter.move_to(RIGHT * 3 + UP * 0.4)
        ctext = T("multiplications", S.SMALL, S.MUTED).next_to(counter, DOWN, buff=0.25)
        ctx = T("1 token · 1 matrix", S.SMALL, S.TEXT).next_to(ctext, DOWN, buff=0.2)
        self.play(FadeIn(counter), FadeIn(ctext), run_time=0.5)
        self.play(ChangeDecimalToValue(counter, 51380224), run_time=self.dur(0.4), rate_func=rush_into)
        self.play(FadeIn(ctx), run_time=0.6)
        self.hold()

        self.beat("b3")
        self.play(FadeOut(VGroup(counter, ctext, ctx, lab)), run_time=0.5)
        tower = LayerTower(n=16, w=2.6, h=0.17, gap=0.06).move_to(LEFT * 3.4)
        self.play(ReplacementTransform(big, tower), run_time=self.dur(0.3))
        rule = M(r"\text{FLOPs} \approx 2 \times \text{active parameters} \times \text{tokens}", 40)
        rule.move_to(RIGHT * 2.3 + UP * 1.2)
        fit_width(rule, 7.5)
        tag = T("rule of thumb", S.TINY, S.MUTED).next_to(rule, DOWN, buff=0.2)
        self.play(Write(rule), FadeIn(tag), run_time=self.dur(0.45))
        self.hold()

        self.beat("b4")
        calc = M(r"2 \times 37{,}000{,}000{,}000", 40, S.TEXT).next_to(tag, DOWN, buff=0.6)
        res = M(r"\approx 74 \text{ billion FLOPs per token}", 40, S.COMPUTE).next_to(calc, DOWN, buff=0.35)
        fit_width(res, 7.5)
        self.play(FadeIn(calc, shift=UP * 0.2), run_time=self.dur(0.3))
        self.play(Write(res), run_time=self.dur(0.35))
        self.play(tower.slabs.animate.set_fill(S.COMPUTE, opacity=0.8), rate_func=there_and_back, run_time=0.8)
        self.hold()

        self.beat("b5")
        self.play(FadeOut(VGroup(rule, tag, calc, res)), tower.animate.move_to(ORIGIN), run_time=0.6)
        field = VGroup(*[LayerTower(n=16, w=2.6, h=0.17, gap=0.06, opacity=0.18) for _ in range(48)])
        field.arrange_in_grid(6, 8, buff=0.9).move_to(ORIGIN)
        field.shift(tower.get_center() - field[27].get_center())
        field.remove(field[27])
        self.add(field)
        self.play(self.camera.frame.animate.scale(4.5), tower.slabs.animate.set_fill(S.COMPUTE, opacity=0.9),
                  run_time=self.dur(0.8))
        self.hold()

        self.beat("b6")
        g = GPU(w=2.6 * 1.3, h=2.0 * 1.3).move_to(tower)
        self.play(FadeOut(field), ReplacementTransform(tower, g), run_time=self.dur(0.5))
        self.play(self.camera.frame.animate.scale(1 / 4.5).move_to(g), run_time=1.2)
        self.hold()
        self.finish(tail=0.2)
