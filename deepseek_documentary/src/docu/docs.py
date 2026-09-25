"""Generate human-readable production documents from the structured script:

  story/script.md          production-annotated narration (timestamps, pauses, visuals, SFX, music, loops)
  story/storyboard.md      scene-by-scene storyboard with sources and Manim classes
  story/scene_manifest.yaml  machine-readable scene list

    python -m docu.docs [--quality preview]
"""
from __future__ import annotations

import argparse
import csv
import json

import yaml

from .paths import OUTPUT, RESEARCH, SCENES_OUT, STORY, TIMING
from .rendering.presets import load_video_config, resolve_quality
from .script import load_script


def mmss(t):
    return f"{int(t // 60):02d}:{int(t % 60):02d}"


def build(q):
    scenes = load_script()
    timing = json.loads(TIMING.read_text()) if TIMING.exists() else {"scenes": {}}
    ledger = {}
    with (RESEARCH / "claim_ledger.csv").open() as f:
        for r in csv.DictReader(f):
            ledger[r["claim_id"]] = r
    loops = yaml.safe_load((STORY / "loop_map.yaml").read_text())
    od = SCENES_OUT / q["name"]
    # absolute timeline: prefer rendered timelines, else narration estimate
    t = 0.0
    abs_starts, scene_start, scene_dur = {}, {}, {}
    for s in scenes:
        tl = od / f"{s.filename}.timeline.json"
        scene_start[s.id] = t
        if tl.exists():
            d = json.loads(tl.read_text())
            for bid, st in d["starts"].items():
                abs_starts[(s.id, bid)] = t + st
            t += d["duration"]
        else:
            tt = t + 0.35
            for b in timing["scenes"].get(s.id, {}).get("beats", []):
                abs_starts[(s.id, b["id"])] = tt
                tt += b["dur"] + b["pause"]
            t = tt + 0.6
        scene_dur[s.id] = t - scene_start[s.id]
    total = t

    # ---------- script.md
    L = [f"# Narration script — {load_video_config()['title']}\n",
         f"Voice: Kokoro-82M (`am_michael`). Total runtime ≈ {mmss(total)}. Timestamps from the "
         f"{q['name']} render when available. `[[ID]]` tags point to `research/claim_ledger.csv` and are not spoken.\n"]
    cur_act = None
    for s in scenes:
        if s.act != cur_act:
            cur_act = s.act
            L.append(f"\n---\n\n## ACT {s.act} — {s.act_title}   ·   MUSIC: {s.music}\n")
        L.append(f"\n### {s.id} · {s.title}\n")
        if s.loops_open:
            L.append("LOOP OPENED: " + "; ".join(f"{l} — {loops[l]['question']}" for l in s.loops_open) + "\n")
        beats = timing["scenes"].get(s.id, {}).get("beats", [])
        bd = {b["id"]: b for b in beats}
        for b in s.beats:
            st = abs_starts.get((s.id, b.id), 0)
            en = st + bd.get(b.id, {}).get("dur", 0)
            L.append(f"\n**[{mmss(st)}–{mmss(en)}]**\n\nNARRATOR:\n> {b.say}\n\n[PAUSE {b.pause:.1f}s]\n\n"
                     f"VISUAL: {b.visual}\n")
            if b.sfx:
                L.append(f"\nSFX: {b.sfx}\n")
        if s.loops_close:
            L.append("\nLOOP CLOSED: " + "; ".join(f"{l} — {loops[l]['question']}" for l in s.loops_close) + "\n")
    (STORY / "script.md").write_text("\n".join(L))

    # ---------- storyboard.md
    B = [f"# Storyboard\n\nOne entry per scene. Each scene is one Manim class in `src/docu/scenes/actNN.py`, "
         f"rendered to `scene_NNN.mp4`. Every beat's visual intent is listed under the narration it serves.\n"]
    for s in scenes:
        tags = sorted({t for b in s.beats for t in b.tags if t != "MATH"})
        srcs = sorted({f"{ledger[t]['source']} ({ledger[t]['location']})" for t in tags if t in ledger})
        sfxs = sorted({b.sfx for b in s.beats if b.sfx})
        B.append(f"\n## SCENE {s.index:03d} · {s.id} · {s.title}\n\n"
                 f"| Field | Value |\n|---|---|\n"
                 f"| Time | {mmss(scene_start[s.id])}–{mmss(scene_start[s.id] + scene_dur[s.id])} |\n"
                 f"| Act | {s.act} — {s.act_title} |\n"
                 f"| Manim class | `{s.module}.{s.cls}` |\n"
                 f"| Output | `{s.filename}.mp4` |\n"
                 f"| Claims | {', '.join(tags) or '— (conceptual / pedagogical only)'} |\n"
                 f"| Sources | {'; '.join(srcs) or '—'} |\n"
                 f"| Audio | music: {s.music}; SFX: {', '.join(sfxs) or 'none'} |\n"
                 f"| Loop opened | {', '.join(s.loops_open) or '—'} |\n"
                 f"| Loop closed | {', '.join(s.loops_close) or '—'} |\n")
        for b in s.beats:
            B.append(f"- **{b.id}** — *{b.spoken[:140]}{'…' if len(b.spoken) > 140 else ''}*  \n  → {b.visual}")
    (STORY / "storyboard.md").write_text("\n".join(B) + "\n")

    # ---------- manifest
    man = [{"index": s.index, "id": s.id, "act": s.act, "class": s.cls, "module": s.module, "file": f"{s.filename}.mp4",
            "title": s.title, "start": round(scene_start[s.id], 2), "duration": round(scene_dur[s.id], 2),
            "beats": [b.id for b in s.beats], "music": s.music} for s in scenes]
    (STORY / "scene_manifest.yaml").write_text(yaml.safe_dump(man, sort_keys=False, allow_unicode=True))
    print(f"[docs] script.md, storyboard.md, scene_manifest.yaml written; runtime ≈ {mmss(total)}")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--quality")
    a = ap.parse_args(argv)
    build(resolve_quality(a.quality))


if __name__ == "__main__":
    main()
