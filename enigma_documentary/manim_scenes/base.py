"""EnigmaScene: timing locked to the film timeline (build/timeline.json).

`self.until("b3")` waits until beat b3 starts. If the animation before it ran
long, the overrun is recorded and reported by the runner, never hidden. At the
end `self.until_end()` pads the scene to exactly its planned duration, so
Remotion can drop the MP4 at the scene's start and every word lands on time.
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

from manim import Scene

from manim_scenes import style as S

ROOT = Path(os.environ.get("ENIGMA_ROOT", Path(__file__).resolve().parents[1]))


class EnigmaScene(Scene):
    SCENE_ID = ""

    def setup(self):
        self.camera.background_color = S.BG
        tl = json.loads((ROOT / "build" / "timeline.json").read_text())
        self.spec = next(s for s in tl["scenes"] if s["id"] == self.SCENE_ID)
        self.overruns: list[dict] = []

    @property
    def now(self) -> float:
        return self.renderer.time

    def beat_time(self, ref: str) -> float:
        m = re.fullmatch(r"(b\d+)(\.end)?([+-]\d+(?:\.\d+)?)?", ref.strip())
        b = next(x for x in self.spec["beats"] if x["id"] == m.group(1))
        t = b["start"] + (b["dur"] if m.group(2) else 0.0)
        return t + (float(m.group(3)) if m.group(3) else 0.0)

    def until(self, ref: str):
        target = self.beat_time(ref)
        gap = target - self.now
        if gap > 1e-3:
            self.wait(gap)
        elif gap < -0.05:
            self.overruns.append({"beat": ref, "late_by": round(-gap, 3)})

    def until_end(self):
        gap = self.spec["duration"] - self.now
        if gap > 1e-3:
            self.wait(gap)
        elif gap < -0.05:
            self.overruns.append({"beat": "end", "late_by": round(-gap, 3)})
        out = ROOT / "build" / "manim_overruns.json"
        data = json.loads(out.read_text()) if out.exists() else {}
        data[self.SCENE_ID] = self.overruns
        out.write_text(json.dumps(data, indent=1))

    def slot(self, start: str, end: str, minimum=0.3) -> float:
        """Seconds available between now-ish and a later beat (for run_time)."""
        return max(minimum, self.beat_time(end) - self.beat_time(start))
