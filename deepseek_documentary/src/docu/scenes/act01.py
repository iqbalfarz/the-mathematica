"""ACT 1 — The Impossible Constraint."""
from manim import *  # noqa: F401,F403

from docu import style as S
from docu.base_scene import DocScene
from docu.components import (GPU, ChipCard, T, big_number, caption, cell_grid, chip, fit_width, gpu_wall,
                             persistent_question, question_banner, safe_right, safe_top, source_line, strike)

QUESTION = "What do you do when you can't buy your way out?"


class S0101ColdOpen(DocScene):
    SCENE_ID = "s0101"

    def construct(self):
        self.beat("b1")
        g = GPU(w=1.3, h=0.9)
        self.play(FadeIn(g, scale=0.8), run_time=self.dur(0.4))
        self.play(g.cores.animate.set_fill(opacity=0.8), rate_func=there_and_back, run_time=self.dur(0.4))
        self.hold()

        self.beat("b2")
        row = VGroup(*[GPU(w=1.3, h=0.9) for _ in range(5)]).arrange(RIGHT, buff=0.3)
        self.play(ReplacementTransform(VGroup(g), row), run_time=self.dur(0.35))
        grid = VGroup(*[GPU(w=1.0, h=0.7, cores=(4, 6)) for _ in range(24)]).arrange_in_grid(4, 6, buff=0.25)
        self.play(ReplacementTransform(row, grid), run_time=self.dur(0.45))
        self.hold()

        self.beat("b3")
        wall = gpu_wall(18, 34, unit=0.36)
        wall.scale_to_fit_width(config.frame_width * 1.9)
        self.play(ReplacementTransform(grid, wall), run_time=self.dur(0.35))
        self.play(self.camera.frame.animate.scale(1.9), run_time=self.dur(0.3))
        cols = [VGroup(*[wall[i * 34 + j] for i in range(18)]) for j in range(34)]
        self.play(LaggedStart(*[c.animate(rate_func=there_and_back).set_fill(S.COMPUTE, opacity=0.9)
                                for c in cols], lag_ratio=0.06), run_time=self.dur(0.35))
        self.hold()

        self.beat("b4")
        chain = VGroup(T("more money", S.H2, S.PARAM, weight="BOLD"), T("→", S.H2, S.MUTED),
                       T("more GPUs", S.H2, S.COMPUTE, weight="BOLD"), T("→", S.H2, S.MUTED),
                       T("better models", S.H2, S.TOKEN, weight="BOLD")).arrange(RIGHT, buff=0.35)
        chain.scale(1.9)
        panel = BackgroundRectangle(chain, color=S.BG, fill_opacity=0.85, buff=0.5)
        self.play(wall.animate.set_opacity(0.35), FadeIn(panel), run_time=self.dur(0.2))
        self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.3) for m in chain], lag_ratio=0.25),
                  run_time=self.dur(0.55))
        self.hold()
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.finish(tail=0.2)


def _timeline():
    x0, x1 = -6.0, 6.0
    line = Line([x0, 0.4, 0], [x1, 0.4, 0], color=S.MUTED, stroke_width=2)
    years = VGroup()
    ticks = VGroup()
    for k, y in enumerate(range(2022, 2027)):
        x = x0 + 0.6 + k * 2.6
        ticks.add(Line([x, 0.3, 0], [x, 0.5, 0], color=S.MUTED, stroke_width=2))
        years.add(T(str(y), S.TINY, S.MUTED).move_to([x, 0.05, 0]))
    def xat(t):  # t = fractional year
        return x0 + 0.6 + (t - 2022) * 2.6
    return VGroup(line, ticks, years), xat


class S0102RulesChanged(DocScene):
    SCENE_ID = "s0102"

    def construct(self):
        self.beat("b1")
        tl, xat = _timeline()
        self.wait(0.5)
        self.play(Create(tl[0]), run_time=self.dur(0.5))
        self.play(FadeIn(tl[1]), FadeIn(tl[2]), run_time=0.5)
        self.hold()

        self.beat("b2")
        m1 = self._marker("Oct 2022", xat(2022.77))
        a100 = ChipCard("A100", "NVIDIA")
        h100 = ChipCard("H100", "NVIDIA")
        top = VGroup(a100, h100).arrange(RIGHT, buff=0.25).move_to([xat(2022.77), 2.35, 0])
        self.play(FadeIn(m1), run_time=0.5)
        self.play(LaggedStart(FadeIn(a100, shift=DOWN * 0.2), FadeIn(h100, shift=DOWN * 0.2), lag_ratio=0.3),
                  run_time=self.dur(0.3))
        r1 = VGroup(a100.status("restricted"), h100.status("restricted"))
        self.play(FadeIn(r1, scale=1.2), run_time=self.dur(0.2))
        self.hold()

        self.beat("b3")
        a800 = ChipCard("A800", "China version")
        h800 = ChipCard("H800", "China version")
        low = VGroup(a800, h800).arrange(RIGHT, buff=0.9).move_to([xat(2023.25), -1.2, 0])
        link = Line(a800.get_right(), h800.get_left(), color=S.COMM, stroke_width=2)
        link_lbl = T("slower chip-to-chip links", S.TINY, S.COMM).next_to(low, DOWN, buff=0.45)
        self.play(LaggedStart(FadeIn(a800, shift=UP * 0.2), FadeIn(h800, shift=UP * 0.2), lag_ratio=0.3),
                  run_time=self.dur(0.35))
        self.play(Create(link), FadeIn(link_lbl), run_time=self.dur(0.3))
        self.hold()

        self.beat("b4")
        m2 = self._marker("Oct 2023", xat(2023.79))
        self.play(FadeIn(m2), run_time=0.5)
        r2 = VGroup(a800.status("restricted"), h800.status("restricted"))
        self.play(FadeOut(link_lbl), FadeIn(r2, scale=1.2), link.animate.set_color(S.LOSS), run_time=self.dur(0.35))
        self.hold()

        self.beat("b5")
        m3 = self._marker("Apr 2025", xat(2025.27))
        h20 = ChipCard("H20", "for China market", w=2.1).move_to([xat(2025.27), 2.35, 0])
        self.play(FadeIn(m3), FadeIn(h20, shift=DOWN * 0.2), run_time=self.dur(0.35))
        r3 = h20.status("licence required", S.PARAM)
        src = source_line("Sources: BIS rules Oct 2022 / Oct 2023 (via CSET, CSIS); NVIDIA Form 8-K, Apr 2025")
        self.play(FadeIn(r3, scale=1.2), FadeIn(src), run_time=self.dur(0.3))
        self.hold()
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)
        self.finish(tail=0.1)

    def _marker(self, text, x):
        dot = Dot([x, 0.4, 0], color=S.LOSS, radius=0.09)
        lbl = T(text, S.TINY, S.LOSS, weight="BOLD").move_to([x, 0.78, 0])
        return VGroup(dot, lbl)


class S0103TheQuestion(DocScene):
    SCENE_ID = "s0103"

    def construct(self):
        self.beat("b1")
        card = RoundedRectangle(corner_radius=0.15, width=5.6, height=4.4, stroke_color=S.TOKEN, stroke_width=2,
                                fill_color=S.PANEL, fill_opacity=1).move_to([-3.3, -0.2, 0])
        name = T("DeepSeek-V3", S.H2, S.TEXT, weight="BOLD")
        date = T("released Dec 2024", S.SMALL, S.MUTED)
        head = VGroup(name, date).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        head.move_to(card.get_corner(UL) + np.array([0.35 + head.width / 2, -0.35 - head.height / 2, 0]))
        self.play(FadeIn(card), FadeIn(head, shift=UP * 0.2), run_time=self.dur(0.4))
        self.hold()

        self.beat("b2")
        row1 = VGroup(T("2,048", S.H2, S.COMPUTE, weight="BOLD", mono=True), T("H800 GPUs", S.BODY, S.TEXT))
        row1.arrange(RIGHT, buff=0.25, aligned_edge=DOWN)
        row1.next_to(head, DOWN, buff=0.55, aligned_edge=LEFT)
        dots = cell_grid(32, 64, 0.052, color=S.COMPUTE, stroke=0, fill_opacity=0.7, gap=0.022)
        dots.move_to([3.4, -0.2, 0])
        dots_lbl = T("2,048 GPUs", S.TINY, S.MUTED).next_to(dots, DOWN, buff=0.15)
        self.play(FadeIn(row1, shift=UP * 0.2), run_time=self.dur(0.25))
        self.play(LaggedStart(*[FadeIn(r) for r in [VGroup(*dots[k * 64:(k + 1) * 64]) for k in range(32)]],
                              lag_ratio=0.08), FadeIn(dots_lbl), run_time=self.dur(0.45))
        self.hold()

        self.beat("b3")
        row2 = VGroup(T("2.788M", S.H2, S.PARAM, weight="BOLD", mono=True), T("GPU-hours", S.BODY, S.TEXT))
        row2.arrange(RIGHT, buff=0.25, aligned_edge=DOWN).next_to(row1, DOWN, buff=0.45, aligned_edge=LEFT)
        rep = chip("reported by DeepSeek", S.MUTED).next_to(row2, DOWN, buff=0.35, aligned_edge=LEFT)
        bench = T("comparable to leading closed models*", S.SMALL, S.TOKEN).next_to(rep, DOWN, buff=0.3,
                                                                                      aligned_edge=LEFT)
        foot = T("*DeepSeek's own benchmarks", S.TINY, S.MUTED).next_to(bench, DOWN, buff=0.12, aligned_edge=LEFT)
        self.play(FadeIn(row2, shift=UP * 0.2), run_time=self.dur(0.25))
        self.play(FadeIn(rep), run_time=0.5)
        self.play(FadeIn(bench), FadeIn(foot), run_time=self.dur(0.25))
        self.hold()

        self.beat("b4")
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        imp = big_number("IMPOSSIBLE", S.TEXT, 110)
        fit_width(imp)
        self.play(FadeIn(imp, scale=1.1), run_time=self.dur(0.2))
        st = strike(imp)
        self.play(Create(st), run_time=0.5)
        sur = big_number("SURPRISING", S.PARAM, 110)
        fit_width(sur)
        self.play(FadeOut(VGroup(imp, st), shift=UP * 0.4), FadeIn(sur, shift=UP * 0.4), run_time=self.dur(0.25))
        self.hold()

        self.beat("b5")
        self.play(FadeOut(sur), run_time=0.5)
        q = question_banner(QUESTION, S.H2)
        self.play(AddTextLetterByLetter(q[0]), run_time=self.dur(0.35, hi=3.0))
        self.play(GrowFromCenter(q[1]), run_time=0.5)
        self.hold()

        self.beat("b6")
        pq = persistent_question(QUESTION)
        self.play(ReplacementTransform(q, pq), run_time=1.0)
        num = big_number("890 bytes", S.MEMORY, 100)
        qm = T("?", 100, S.PARAM, weight="BOLD")
        grp = VGroup(num, qm).arrange(RIGHT, buff=0.3)
        self.play(FadeIn(grp, scale=0.9), run_time=self.dur(0.2))
        self.wait(self.dur(0.35))
        corner = VGroup(T("890 bytes", S.SMALL, S.MEMORY, weight="BOLD"), T("?", S.SMALL, S.PARAM, weight="BOLD"))
        corner.arrange(RIGHT, buff=0.1).move_to([safe_right() - 0.8, safe_top() - 0.2, 0])
        self.play(ReplacementTransform(grp, corner), run_time=1.0)
        self.hold()

        self.beat("b7")
        dot = Dot(ORIGIN, radius=0.14, color=S.TEXT)
        halo = VGroup(*[Circle(r, color=S.PARAM, stroke_width=2, stroke_opacity=0.5 - 0.12 * k)
                        for k, r in enumerate((0.45, 0.85, 1.3))])
        self.play(*[m.animate.move_to(ORIGIN).scale(0.05).set_opacity(0) for m in self.mobjects],
                  FadeIn(dot), run_time=self.dur(0.5))
        self.play(LaggedStart(*[Create(c) for c in halo], lag_ratio=0.3), run_time=1.2)
        self.play(halo.animate.scale(1.15).set_stroke(opacity=0.15), dot.animate.scale(1.3), rate_func=there_and_back,
                  run_time=1.2)
        self.hold()
        self.finish(tail=0.3)
