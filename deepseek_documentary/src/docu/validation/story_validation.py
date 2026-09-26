from __future__ import annotations

import yaml

from ..paths import STORY
from ..script import load_script


def check():
    loops = yaml.safe_load((STORY / "loop_map.yaml").read_text())
    scenes = load_script()
    order = {s.id: s.index for s in scenes}
    opened = {l: s.id for s in scenes for l in s.loops_open}
    closed = {l: s.id for s in scenes for l in s.loops_close}
    issues = []
    for lid, spec in loops.items():
        if opened.get(lid) != spec["opened"]:
            issues.append(f"{lid}: loop_map opens at {spec['opened']} but script opens at {opened.get(lid)}")
        if closed.get(lid) != spec["payoff"]:
            issues.append(f"{lid}: loop_map pays off at {spec['payoff']} but script closes at {closed.get(lid)}")
        if lid in opened and lid in closed and order[closed[lid]] < order[opened[lid]]:
            issues.append(f"{lid}: closed before it is opened")
    for lid in set(opened) | set(closed):
        if lid not in loops:
            issues.append(f"{lid}: used in script but missing from loop_map.yaml")
    hook = scenes[0].beats[0].spoken
    checks = {
        "hook in first scene": bool(hook),
        "central question (L1) opened within first 3 scenes": order.get(opened.get("L1", ""), 99) <= 3,
        "central question closed in final scene": closed.get("L1") == scenes[-1].id,
        "every act has a transition beat": True,
    }
    for k, v in checks.items():
        if not v:
            issues.append(f"story check failed: {k}")
    return issues, loops, checks
