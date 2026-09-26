"""ACT 3 — Why GPUs matter: parallelism and the three walls."""
import numpy as np
from manim import *  # noqa: F401,F403

from docu import style as S
from docu.base_scene import DocScene
from docu.components import (GPU, CPUChip, MemoryBank, Pillar, Pipe, T, WALLS, WallsLegend, caption, cell_grid, chip,
                             fit_width, safe_right, safe_top, source_line)


def _grid(n=16, size=0.13):
    return cell_grid(n, n, size, color=S.COMPUTE, stroke=0.5, fill_opacity=0.05, gap=0.03)


class S0301CPUvsGPU(DocScene):
    SCENE_ID = "s0301"

    def construct(self):
        self.beat("b1")
        cpu = CPUChip(8).move_to([-3.6, 1.4, 0])
        cl = T("CPU", S.BODY, S.GRAD, weight="BOLD").next_to(cpu, UP, buff=0.2)
        tasks = VGroup(*[T("×", S.SMALL, S.TEXT) for _ in range(8)]).arrange(RIGHT, buff=0.25)
        tasks.next_to(cpu, LEFT, buff=0.5).shift(DOWN * 0.0)
        tasks.set_x(max(tasks.get_x(), -6.9 + tasks.width / 2))
        self.play(FadeIn(cpu), FadeIn(cl), run_time=self.dur(0.25))
        self.play(FadeIn(tasks), run_time=0.5)
        for t in tasks[::-1][:4]:
            self.play(t.animate.move_to(cpu).set_opacity(0), run_time=self.dur(0.08, lo=0.25))
        self.hold()

        self.beat("b2")
        g1 = _grid().move_to([-3.6, -1.7, 0])
        self.play(FadeIn(g1), FadeOut(tasks), run_time=0.5)
        cells = list(g1)
        chunk = 16
        n_chunks = 5
        for k in range(n_chunks):
            self.play(*[c.animate.set_fill(S.COMPUTE, opacity=0.8) for c in cells[k * chunk:(k + 1) * chunk]],
                      run_time=self.dur(0.12, lo=0.25))
        self.hold()

        self.beat("b3")
        g1s = g1.copy()
        self.play(g1.animate.arrange_in_grid(16, 16, buff=0.07).move_to([-3.6, -1.7, 0]), run_time=self.dur(0.3))
        note = T("each cell = its own dot product", S.SMALL, S.MUTED).next_to(g1, RIGHT, buff=0.5)
        self.play(FadeIn(note), run_time=0.6)
        self.hold()

        self.beat("b4")
        self.play(FadeOut(note), g1.animate.become(g1s), run_time=0.5)
        gpu = GPU(w=2.6, h=1.9, cores=(12, 18)).move_to([3.6, 1.4, 0])
        gl = T("GPU", S.BODY, S.COMPUTE, weight="BOLD").next_to(gpu, UP, buff=0.2)
        g2 = _grid().move_to([3.6, -1.7, 0])
        self.play(FadeIn(gpu), FadeIn(gl), FadeIn(g2), run_time=self.dur(0.3))
        self.play(LaggedStart(*[c.animate.set_fill(S.COMPUTE, opacity=0.8) for c in g2], lag_ratio=0.002),
                  gpu.cores.animate.set_fill(opacity=0.9), run_time=self.dur(0.25))
        self.play(gpu.cores.animate.set_fill(opacity=0.35), run_time=0.4)
        self.hold()

        self.beat("b5")
        self.play(*[c.animate.set_fill(opacity=0.05) for c in list(g1) + list(g2)], run_time=0.5)
        race = self.dur(0.6)
        self.play(LaggedStart(*[c.animate.set_fill(S.COMPUTE, opacity=0.8) for c in list(g1)[:26]], lag_ratio=1.0),
                  LaggedStart(*[c.animate.set_fill(S.COMPUTE, opacity=0.8) for c in g2], lag_ratio=0.01),
                  run_time=race)
        cap = caption("The maths of neural networks is almost perfectly parallel.", S.TEXT)
        self.play(FadeIn(cap), run_time=0.6)
        self.hold()
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.finish(tail=0.1)


class S0302MemoryWall(DocScene):
    SCENE_ID = "s0302"

    def construct(self):
        self.beat("b1")
        mem = MemoryBank("HBM memory", w=1.6, h=2.8).move_to([-4.6, 0.2, 0])
        gpu = GPU(w=2.8, h=2.1, cores=(10, 14)).move_to([3.8, 0.2, 0])
        gpu.shift(UP * (mem.box.get_y() - gpu.die.get_y()))
        gl = T("compute units", S.SMALL, S.COMPUTE, weight="BOLD").next_to(gpu, DOWN, buff=0.15)
        pipe = Pipe(mem.box.get_right() + RIGHT * 0.05, gpu.die.get_left() + LEFT * 0.05, width=0.5)
        self.play(FadeIn(mem), FadeIn(gpu), FadeIn(gl), run_time=self.dur(0.35))
        self.play(Create(pipe), run_time=self.dur(0.25))
        self.hold()

        self.beat("b2")
        bw = T("bandwidth  (bytes / second)", S.SMALL, S.COMM).next_to(pipe, UP, buff=0.45)
        self.play(FadeIn(bw), run_time=0.6)
        parts = self._flow(pipe, 18, self.dur(0.6))
        self.hold()

        self.beat("b3")
        self.play(pipe.set_bandwidth(0.08), run_time=self.dur(0.2))
        idle = T("idle", S.BODY, S.MUTED, weight="BOLD").next_to(gpu, UP, buff=0.25)
        self.play(LaggedStart(*[c.animate.set_fill(opacity=0.06) for c in gpu.cores], lag_ratio=0.01),
                  FadeIn(idle), run_time=self.dur(0.4))
        self._flow(pipe, 3, self.dur(0.3), size=0.07)
        self.hold()

        self.beat("b4")
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
        pillars = VGroup(*[Pillar(n, c, w=2.4, h=3.4) for n, c in WALLS]).arrange(RIGHT, buff=1.1).shift(UP * 0.3)
        for p in pillars:
            self.play(GrowFromEdge(p.col, DOWN), FadeIn(p.t), run_time=self.dur(0.2, hi=1.4))
        subs = ["how fast you multiply", "how much you hold & read", "how fast chips talk"]
        subt = VGroup(*[T(s, S.TINY, S.MUTED).next_to(p.t, DOWN, buff=0.12) for s, p in zip(subs, pillars)])
        self.play(FadeIn(subt), run_time=0.8)
        self.hold()

        self.beat("b5")
        leg = WallsLegend()
        self.play(ReplacementTransform(VGroup(pillars, subt), leg), run_time=self.dur(0.4))
        self.hold()
        self.finish(tail=0.3)

    def _flow(self, pipe, n, rt, size=0.12):
        start, end = pipe.start, pipe.end
        dots = VGroup(*[Square(size, stroke_width=0, fill_color=S.PARAM, fill_opacity=0.95).move_to(start)
                        for _ in range(n)])
        self.add(dots)
        self.play(LaggedStart(*[d.animate(rate_func=linear).move_to(end) for d in dots], lag_ratio=0.15),
                  run_time=max(0.6, rt))
        self.remove(dots)
        return dots


class S0303ManyGPUs(DocScene):
    SCENE_ID = "s0303"

    def construct(self):
        leg = WallsLegend()
        self.add(leg)
        self.beat("b1")
        unit = 0.105  # frame units per GB
        wbar = Rectangle(width=671 * unit / 10 * 1.0, height=0.55, stroke_width=0, fill_color=S.PARAM,
                         fill_opacity=0.85)
        wbar.width = 11.0
        gb = 11.0 / 671
        wbar.move_to([0, 1.6, 0])
        wl = T("DeepSeek-V3 weights  ≈ 671 GB  (at 1 byte per parameter)", S.SMALL, S.TEXT).next_to(wbar, UP, buff=0.2)
        g1 = Rectangle(width=80 * gb, height=0.55, stroke_width=0, fill_color=S.MEMORY, fill_opacity=0.85)
        g1.next_to(wbar, DOWN, buff=0.7, aligned_edge=LEFT)
        g1l = T("one GPU's memory: 80 GB", S.SMALL, S.MEMORY).next_to(g1, RIGHT, buff=0.25)
        self.play(GrowFromEdge(wbar, LEFT), FadeIn(wl), run_time=self.dur(0.3))
        self.play(GrowFromEdge(g1, LEFT), FadeIn(g1l), run_time=self.dur(0.2))
        gpus = VGroup(*[GPU(w=1.05, h=0.75, cores=(4, 6)) for _ in range(9)]).arrange(RIGHT, buff=0.18)
        gpus.move_to([0, -1.7, 0])
        fit_width(gpus)
        chunks = VGroup(*[Rectangle(width=80 * gb, height=0.55, stroke_width=0, fill_color=S.PARAM,
                                    fill_opacity=0.85) for _ in range(9)])
        for c, k in zip(chunks, range(9)):
            c.move_to(wbar.get_left() + RIGHT * (80 * gb * (k + 0.5)))
            if k == 8:
                c.stretch_to_fit_width((671 - 640) * gb).move_to(wbar.get_left() + RIGHT * (640 * gb + (31 * gb) / 2))
        need = T("more than 8 GPUs just to hold the weights", S.SMALL, S.PARAM).next_to(gpus, DOWN, buff=0.3)
        self.add(chunks)
        self.remove(wbar)
        gpus.set_z_index(0)
        chunks.set_z_index(2)
        self.play(FadeIn(gpus), *[c.animate.move_to(g.die).scale_to_fit_height(0.3) for c, g in zip(chunks, gpus)],
                  run_time=self.dur(0.3))
        self.play(FadeIn(need), run_time=0.6)
        self.hold()

        self.beat("b2")
        self.play(FadeOut(VGroup(wl, g1, g1l, need, chunks)), run_time=0.5)
        ring = VGroup(*[GPU(w=1.05, h=0.75, cores=(4, 6)) for _ in range(9)])
        for k, g in enumerate(ring):
            a = PI / 2 - k * TAU / 9
            g.move_to([2.4 * np.cos(a), 2.2 * np.sin(a) + 0.2, 0])
        self.play(*[Transform(a, b) for a, b in zip(gpus, ring)], run_time=self.dur(0.25))
        links = VGroup()
        pairs = [(i, j) for i in range(9) for j in range(i + 1, 9) if (j - i) in (1, 2, 4) or (i, j) == (0, 8)]
        for i, j in pairs:
            links.add(Line(gpus[i].get_center(), gpus[j].get_center(), color=S.COMM, stroke_width=1.6,
                           stroke_opacity=0.55))
        self.bring_to_back(links)
        self.play(Create(links), run_time=self.dur(0.25))
        self.bring_to_back(links)
        dots = VGroup(*[Dot(radius=0.05, color=S.PARAM).move_to(l.get_start()) for l in links])
        self.play(LaggedStart(*[d.animate.move_to(l.get_end()) for d, l in zip(dots, links)], lag_ratio=0.03),
                  run_time=self.dur(0.3))
        self.play(FadeOut(dots), leg.item("COMMUNICATION").animate.scale(1.15), run_time=0.4)
        self.hold()

        self.beat("b3")
        self.play(FadeOut(VGroup(gpus, links)), leg.item("COMMUNICATION").animate.scale(1 / 1.15), run_time=0.5)
        left = self._pair("H100", 0.9, "≈ 900 GB/s").move_to([-3.3, 0.6, 0])
        right = self._pair("H800", 0.4, "≈ 400 GB/s").move_to([3.3, 0.6, 0])
        self.play(FadeIn(left, shift=UP * 0.2), run_time=self.dur(0.25))
        self.play(FadeIn(right, shift=UP * 0.2), run_time=self.dur(0.25))
        wr = chip("chip-to-chip link bandwidth · widely reported figures", S.MUTED).move_to([0, -1.1, 0])
        same = T("same compute engine", S.SMALL, S.COMPUTE).move_to([0, 2.4, 0])
        self.play(FadeIn(wr), FadeIn(same), run_time=0.8)
        self.hold()

        self.beat("b4")
        link = right[2]
        self.play(link.animate(rate_func=there_and_back).set_stroke(color=S.LOSS, width=link.get_stroke_width() * 2),
                  run_time=1.0)
        tagline = T("Same engine. Narrower pipes.", S.H2, S.TEXT, weight="BOLD").move_to([0, -2.2, 0])
        self.play(FadeIn(tagline, shift=UP * 0.2), run_time=self.dur(0.2))
        q = T("Why aren't more GPUs enough?", S.SMALL, S.PARAM, weight="BOLD")
        q.move_to([safe_right() - q.width / 2, safe_top() - q.height / 2, 0])
        self.play(FadeIn(q, shift=LEFT * 0.3), run_time=self.dur(0.2))
        self.hold()
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.finish(tail=0.1)

    def _pair(self, name, bw, label):
        a = GPU(name, w=1.4, h=1.0, cores=(5, 7))
        b = GPU(name, w=1.4, h=1.0, cores=(5, 7))
        VGroup(a, b).arrange(RIGHT, buff=2.4)
        link = Line(a.die.get_right(), b.die.get_left(), color=S.COMM, stroke_width=bw * 40)
        lab = T(label, S.SMALL, S.COMM, weight="BOLD").next_to(link, UP, buff=0.3)
        return VGroup(a, b, link, lab)
