"""The planned timeline: when every scene and beat happens in the film.

Audio-first: each beat lasts as long as its narration plus its pause, so the
picture is built to the voice, never the other way round. Before narration
exists, durations are estimated from word count (2.4 words/s) so Blender and
Manim can still be developed.

Blender shots, Manim scenes and Remotion all read build/timeline.json, so the
three tools agree on every frame.

    python -m enigma_doc.timeline --profile draft
"""
from __future__ import annotations

import argparse
import json
import re

import yaml

from .paths import CONFIG, TIMELINE, TIMING, ensure_dirs
from .profiles import resolve
from .script import load_script

WPS = 2.4


def _beat_durations() -> dict:
    if TIMING.exists():
        return json.loads(TIMING.read_text()).get("scenes", {})
    return {}


def build(profile: dict) -> dict:
    audio = _beat_durations()
    shots = yaml.safe_load((CONFIG / "shots.yaml").read_text())["shots"]
    fps = profile["fps"]
    t_film = 0.0
    scenes = []
    for sc in load_script():
        real = {b["id"]: b for b in audio.get(sc.id, {}).get("beats", [])}
        t = profile["lead_in"] + sc.allow_black
        beats = []
        for b in sc.beats:
            dur = real[b.id]["dur"] if b.id in real else max(1.2, len(b.spoken.split()) / WPS)
            beats.append({"id": b.id, "start": round(t, 3), "dur": round(dur, 3), "pause": b.pause,
                          "text": b.spoken, "sfx": b.sfx,
                          "wav": f"audio/beats/{sc.id}/{b.id}.wav" if b.id in real else None})
            t += dur + b.pause
        duration = t + profile["tail"]
        frames = int(round(duration * fps))
        entry = {"beats": beats}
        cues = [{"t": b["start"], "sfx": b["sfx"]} for b in beats if b["sfx"]]
        shot = shots.get(sc.shot) if sc.shot else None
        press_times = [round(beat_time(entry, r), 3) for r in (shot or {}).get("press_at", [])]
        slow = float((shot or {}).get("slow", 1.0))
        for pt in press_times:       # mechanical sounds of every key press (see blender/lib/api.py timing)
            cues += [{"t": round(pt + 0.03 * slow, 3), "sfx": "clack"}, {"t": round(pt + 0.10 * slow, 3), "sfx": "click"}]
        scenes.append({"id": sc.id, "title": sc.title, "act": sc.act, "act_title": sc.act_title,
                       "tool": sc.tool, "shot": sc.shot, "music": sc.music,
                       "film_start": round(t_film, 3), "duration": round(duration, 3), "frames": frames,
                       "beats": beats, "press_times": press_times, "slow": slow,
                       "linger": float((shot or {}).get("linger", 0.0)),
                       "press_holds": _holds(entry, shot, press_times),
                       **_signal(entry, shot, press_times), "sfx": sorted(cues, key=lambda c: c["t"]),
                       "estimated": not real})
        t_film += frames / fps
    return {"profile": profile["name"], "fps": fps, "width": profile["width"], "height": profile["height"],
            "render": profile["blender"], "manim_quality": profile["manim_quality"], "crf": profile["crf"],
            "duration": round(t_film, 3), "scenes": scenes, "shots": shots}


def _holds(entry, shot, press_times):
    """Key hold per press: seconds, or a beat reference meaning 'hold until then'."""
    raw = list((shot or {}).get("hold", [0.5] * len(press_times)))
    return [round(beat_time(entry, h) - t, 3) if isinstance(h, str) else float(h)
            for h, t in zip(raw, press_times)]


def _signal(entry, shot, press_times) -> dict:
    """Resolve a shot's `signal` block to absolute scene times.

    signal: {dur: s} | {until: beat} | {pins: {stage: beat ref | seconds}}.
    The current starts when the key contact closes (0.11 s after the press) unless
    pins give `start`; it reaches the lamp at the `lamp` pin (or after `dur`).
    Numeric pins may lie outside the scene: negative = already happened before
    this scene began, very large = not reached in this scene (the current holds).
    """
    sig = (shot or {}).get("signal") or {}
    pins = {k: (round(beat_time(entry, v), 3) if isinstance(v, str) else float(v))
            for k, v in (sig.get("pins") or {}).items()}
    start = pins.pop("start", None)
    if start is None:
        start = round(press_times[0] + 0.11, 3) if press_times else 0.0
    end = pins.get("lamp")
    if end is None and sig.get("until"):
        end = beat_time(entry, sig["until"])
    dur = round(end - start, 3) if end is not None else float(sig.get("dur", 1.6))
    return {"signal_start": start, "signal_dur": dur, "signal_pins": pins}


def beat_time(scene: dict, ref: str) -> float:
    """'b3' -> start of beat b3; 'b3+1.2' -> 1.2 s after; 'b3.end' -> end of its narration."""
    m = re.fullmatch(r"(b\d+)(\.end)?([+-]\d+(?:\.\d+)?)?", ref.strip())
    if not m:
        raise ValueError(f"bad beat reference {ref!r}")
    b = next(x for x in scene["beats"] if x["id"] == m.group(1))
    t = b["start"] + (b["dur"] if m.group(2) else 0.0)
    return t + (float(m.group(3)) if m.group(3) else 0.0)


def load(profile_name: str | None = None) -> dict:
    """Read timeline.json, rebuilding it when missing or built for another profile."""
    p = resolve(profile_name)
    if TIMELINE.exists():
        data = json.loads(TIMELINE.read_text())
        if data.get("profile") == p["name"]:
            return data
    return write(p)


def write(profile: dict) -> dict:
    ensure_dirs()
    data = build(profile)
    TIMELINE.write_text(json.dumps(data, indent=1))
    return data


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile")
    a = ap.parse_args(argv)
    data = write(resolve(a.profile))
    for s in data["scenes"]:
        flag = " (estimated — run `make voice`)" if s["estimated"] else ""
        print(f"{s['id']} {s['tool']:8s} {s['duration']:6.1f}s  {s['title']}{flag}")
    print(f"total {data['duration']/60:.2f} min @ {data['fps']} fps -> {TIMELINE}")


if __name__ == "__main__":
    main()
