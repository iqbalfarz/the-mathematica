"""DocScene: every documentary scene inherits from this.

Timing model (audio-first)
--------------------------
Narration is synthesised per beat before rendering (build/audio/timing.json).
A scene calls `self.beat("b2")` when the visual for beat b2 should start.
`beat()` waits until the previous beat's audio (+ pause) has finished, then
records the *actual* start time. The composer places each beat's audio at that
recorded time, so picture and sound always line up, even if an animation runs
long. Nothing depends on resolution or frame rate.

Layout guard
------------
After every `play`/`add`, visible text objects are checked for leaving the
safe frame, colliding with other text, or being too small. Violations are
written next to the timeline and gathered by validation/visual_validation.py.
"""
from __future__ import annotations

import json
import os

from manim import (MathTex, MovingCameraScene, SingleStringMathTex, Tex, Text, MarkupText,
                   Paragraph, config)

from . import style as S
from .paths import TIMELINE, TIMING

TEXT_TYPES = (Text, MarkupText, MathTex, Tex, SingleStringMathTex, Paragraph)
LEAD_IN = 0.35
DEFAULT_TAIL = 0.6


class DocScene(MovingCameraScene):
    SCENE_ID: str = ""

    # ---------------------------------------------------------------- setup
    def setup(self):
        super().setup()
        self.camera.background_color = S.BG
        self._beats = self._load_beats()
        self._order = [b["id"] for b in self._beats]
        self._by_id = {b["id"]: b for b in self._beats}
        self._starts: dict[str, float] = {}
        self._cur: dict | None = None
        self._violations: list[dict] = []
        self._seen_viol: set = set()

    def _load_beats(self):
        if TIMING.exists():
            data = json.loads(TIMING.read_text())
            sc = data.get("scenes", {}).get(self.SCENE_ID)
            if sc:
                return sc["beats"]
        # No audio yet (layout development): estimate from word count.
        from .script import scene_by_id
        spec = scene_by_id(self.SCENE_ID)
        return [{"id": b.id, "dur": max(1.5, len(b.spoken.split()) / 2.35), "pause": b.pause,
                 "sfx": b.sfx} for b in spec.beats]

    # ---------------------------------------------------------------- time
    @property
    def now(self) -> float:
        return float(self.renderer.time)

    def beat(self, bid: str) -> float:
        """Begin beat `bid`; returns its narration duration in seconds."""
        if bid not in self._by_id:
            raise KeyError(f"{self.SCENE_ID}: unknown beat {bid}")
        idx = self._order.index(bid)
        if idx == 0:
            target = LEAD_IN
        else:
            prev = self._by_id[self._order[idx - 1]]
            if prev["id"] not in self._starts:
                raise RuntimeError(f"{self.SCENE_ID}: beat {prev['id']} skipped before {bid}")
            target = self._starts[prev["id"]] + prev["dur"] + prev["pause"]
        if self.now < target - 1e-3:
            super().wait(target - self.now)
        self._starts[bid] = self.now
        self._cur = self._by_id[bid]
        return self._cur["dur"]

    def dur(self, frac: float = 1.0, lo: float = 0.3, hi: float | None = None) -> float:
        """A run_time that is `frac` of the current beat's narration."""
        d = self._cur["dur"] * frac if self._cur else 1.0
        d = max(lo, d)
        return min(d, hi) if hi else d

    def left(self) -> float:
        """Seconds of the current beat (narration + pause) not yet used."""
        if not self._cur:
            return 0.0
        end = self._starts[self._cur["id"]] + self._cur["dur"] + self._cur["pause"]
        return max(0.0, end - self.now)

    def hold(self, minimum: float = 0.0):
        """Hold the picture until the current beat's audio (and pause) ends."""
        w = max(self.left(), minimum)
        if w > 1e-3:
            super().wait(w)

    def finish(self, tail: float = DEFAULT_TAIL):
        missing = [b for b in self._order if b not in self._starts]
        if missing:
            raise RuntimeError(f"{self.SCENE_ID}: beats never started: {missing}")
        self.hold()
        if tail > 0:
            super().wait(tail)
        self._write_timeline()

    def _write_timeline(self):
        out = {"scene": self.SCENE_ID, "duration": self.now,
               "starts": self._starts, "violations": self._violations,
               "resolution": [config.pixel_width, config.pixel_height], "fps": config.frame_rate}
        (TIMELINE / f"{self.SCENE_ID}.json").write_text(json.dumps(out, indent=1))

    # ---------------------------------------------------------------- layout guard
    def play(self, *args, **kwargs):
        self._in_play = True
        try:
            super().play(*args, **kwargs)
        finally:
            self._in_play = False
        self._check_layout()

    def add(self, *mobjects):
        r = super().add(*mobjects)
        if hasattr(self, "_violations") and not getattr(self, "_in_play", False):
            self._check_layout()
        return r

    def _visible_texts(self):
        found = []

        def walk(m):
            if getattr(m, "skip_layout_check", False):
                return
            if isinstance(m, TEXT_TYPES):
                try:
                    op = max(m.get_fill_opacity(), m.get_stroke_opacity())
                except Exception:
                    op = 1.0
                if op > 0.08 and m.width > 1e-3:
                    found.append(m)
                return
            for s in m.submobjects:
                walk(s)
        for m in self.mobjects:
            walk(m)
        return found

    def _check_layout(self):
        if os.environ.get("DOCU_NO_LAYOUT_CHECK"):
            return
        fr = self.camera.frame
        cx, cy = fr.get_center()[:2]
        hw, hh = fr.width / 2, fr.height / 2
        tol = 0.02 * fr.width
        texts = self._visible_texts()
        boxes = []
        for m in texts:
            x0, y0 = m.get_corner([-1, -1, 0])[:2]
            x1, y1 = m.get_corner([1, 1, 0])[:2]
            boxes.append((m, x0, y0, x1, y1))
            label = self._label(m)
            if x0 < cx - hw - tol or x1 > cx + hw + tol or y0 < cy - hh - tol or y1 > cy + hh + tol:
                self._record("out_of_frame", label)
            if isinstance(m, Text) and len(label) > 1 and not getattr(self, "allow_small", False):
                lines = max(1, label.count("\n") + 1)
                if (m.height / lines) / fr.height < 0.018:
                    self._record("too_small", label)
        for i in range(len(boxes)):
            a, ax0, ay0, ax1, ay1 = boxes[i]
            for j in range(i + 1, len(boxes)):
                b, bx0, by0, bx1, by1 = boxes[j]
                if getattr(a, "allow_overlap", False) or getattr(b, "allow_overlap", False):
                    continue
                if self._related(a, b):
                    continue
                ix = min(ax1, bx1) - max(ax0, bx0)
                iy = min(ay1, by1) - max(ay0, by0)
                if ix <= 0 or iy <= 0:
                    continue
                area = ix * iy
                small = min((ax1 - ax0) * (ay1 - ay0), (bx1 - bx0) * (by1 - by0)) or 1e-6
                if area / small > 0.12:
                    self._record("overlap", f"{self._label(a)} <> {self._label(b)}")

    @staticmethod
    def _related(a, b):
        return a in b.get_family() or b in a.get_family()

    @staticmethod
    def _label(m) -> str:
        for attr in ("text", "original_text", "tex_string"):
            v = getattr(m, attr, None)
            if isinstance(v, str) and v:
                return v[:60]
        return type(m).__name__

    def _record(self, kind: str, what: str):
        key = (kind, what)
        if key in self._seen_viol:
            return
        self._seen_viol.add(key)
        self._violations.append({"t": round(self.now, 2), "type": kind, "what": what})
