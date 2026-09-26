"""Loads the structured script (story/acts/*.yaml) — the single source of truth
for narration (`say`), storyboard (`visual`), SFX cues and which tool renders
each scene (`tool: blender | manim`)."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import lru_cache

import yaml

from .paths import ACTS

TAG_RE = re.compile(r"\s*\[\[([A-Z0-9\-]+)\]\]")


@dataclass
class Beat:
    id: str
    say: str
    pause: float
    visual: str
    sfx: str | None = None

    @property
    def tags(self) -> list[str]:
        return TAG_RE.findall(self.say)

    @property
    def spoken(self) -> str:
        return re.sub(r"\s+", " ", TAG_RE.sub("", self.say)).strip()


@dataclass
class SceneSpec:
    id: str
    cls: str
    title: str
    act: int
    act_title: str
    music: str
    tool: str
    index: int
    shot: str | None = None
    beats: list[Beat] = field(default_factory=list)
    loops_open: list[str] = field(default_factory=list)
    loops_close: list[str] = field(default_factory=list)
    allow_black: float = 0.0
    sim_check: dict | None = None

    def beat(self, bid: str) -> Beat:
        for b in self.beats:
            if b.id == bid:
                return b
        raise KeyError(f"{self.id}: no beat {bid}")


@lru_cache(maxsize=1)
def load_script() -> list[SceneSpec]:
    scenes: list[SceneSpec] = []
    for path in sorted(ACTS.glob("act*.yaml")):
        data = yaml.safe_load(path.read_text())
        for sc in data["scenes"]:
            loops = sc.get("loops") or {}
            spec = SceneSpec(
                id=sc["id"], cls=sc["cls"], title=sc["title"], act=int(data["act"]),
                act_title=data["title"], music=data.get("music", "minimal"), tool=sc["tool"],
                index=len(scenes) + 1, shot=sc.get("shot"),
                loops_open=list(loops.get("open", []) or []),
                loops_close=list(loops.get("close", []) or []),
                allow_black=float(sc.get("allow_black", 0.0)), sim_check=sc.get("sim_check"))
            for b in sc["beats"]:
                spec.beats.append(Beat(id=b["id"], say=b["say"], pause=float(b.get("pause", 0.35)),
                                       visual=b.get("visual", ""), sfx=b.get("sfx")))
            scenes.append(spec)
    return scenes


def scene_by_id(sid: str) -> SceneSpec:
    for s in load_script():
        if s.id == sid:
            return s
    raise KeyError(sid)
