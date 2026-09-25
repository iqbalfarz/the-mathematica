"""Loads the structured script (story/acts/*.yaml).

The YAML script is the single source of truth: TTS reads `say`, the storyboard is
generated from `visual`, and Manim scenes are timed by beat ids.
"""
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
    index: int                     # global 1-based order
    beats: list[Beat] = field(default_factory=list)
    loops_open: list[str] = field(default_factory=list)
    loops_close: list[str] = field(default_factory=list)

    @property
    def module(self) -> str:
        return f"docu.scenes.act{self.act:02d}"

    @property
    def filename(self) -> str:
        return f"scene_{self.index:03d}"


@lru_cache(maxsize=1)
def load_script() -> list[SceneSpec]:
    scenes: list[SceneSpec] = []
    for path in sorted(ACTS.glob("act*.yaml")):
        data = yaml.safe_load(path.read_text())
        for sc in data["scenes"]:
            loops = sc.get("loops") or {}
            spec = SceneSpec(
                id=sc["id"], cls=sc["cls"], title=sc["title"], act=int(data["act"]),
                act_title=data["title"], music=data.get("music", "minimal"),
                index=len(scenes) + 1,
                loops_open=list(loops.get("open", []) or []),
                loops_close=list(loops.get("close", []) or []),
            )
            for b in sc["beats"]:
                spec.beats.append(Beat(id=b["id"], say=b["say"], pause=float(b.get("pause", 0.35)),
                                       visual=b.get("visual", ""), sfx=b.get("sfx")))
            scenes.append(spec)
    return scenes


def scene_by_id(scene_id: str) -> SceneSpec:
    for s in load_script():
        if s.id == scene_id:
            return s
    raise KeyError(scene_id)


def word_count() -> int:
    return sum(len(b.spoken.split()) for s in load_script() for b in s.beats)
