"""Stage everything Remotion needs into remotion/public/, then write captions.

    python -m enigma_doc.stage --profile draft

public/timeline.json  = build/timeline.json + event streams + which media exist
public/media/...      = links (or copies on Windows) to renders, narration, SFX

Missing renders are fine: Remotion shows a labelled slate with the scene's
storyboard text instead, so you can watch an animatic before anything renders.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
from pathlib import Path

from .paths import AUDIO, EVENTS, OUTPUT, REMOTION, REMOTION_MEDIA, RENDERS, SFX_DIR
from .script import load_script
from .timeline import load


def _link(src: Path, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.is_symlink() or dst.exists():
        if dst.is_dir() and not dst.is_symlink():
            shutil.rmtree(dst)
        else:
            dst.unlink()
    try:
        os.symlink(src.resolve(), dst, target_is_directory=src.is_dir())
    except OSError:          # Windows without developer mode: copy instead
        (shutil.copytree if src.is_dir() else shutil.copy2)(src, dst)


def _srt_time(t: float) -> str:
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_srt(tl: dict, path: Path):
    lines, n = [], 1
    for sc in tl["scenes"]:
        for b in sc["beats"]:
            a = sc["film_start"] + b["start"]
            lines += [str(n), f"{_srt_time(a)} --> {_srt_time(a + b['dur'])}", b["text"], ""]
            n += 1
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines))


def stage(profile: str | None = None) -> dict:
    tl = load(profile)
    prof = tl["profile"]
    specs = {s.id: s for s in load_script()}
    if REMOTION_MEDIA.exists():
        shutil.rmtree(REMOTION_MEDIA)
    REMOTION_MEDIA.mkdir(parents=True)
    if AUDIO.exists() and (AUDIO / "beats").exists():
        _link(AUDIO / "beats", REMOTION_MEDIA / "audio" / "beats")
    if SFX_DIR.exists():
        _link(SFX_DIR, REMOTION_MEDIA / "sfx")
    for sc in tl["scenes"]:
        sc["visuals"] = [b.visual for b in specs[sc["id"]].beats]
        sc["media"] = None
        if sc["tool"] == "blender":
            d = RENDERS / "blender" / prof / sc["id"]
            frames = sorted(d.glob("frame_*.png")) if d.exists() else []
            frames = [f for f in frames if f.stat().st_size > 0]
            if len(frames) == sc["frames"]:
                _link(d, REMOTION_MEDIA / "blender" / sc["id"])
                sc["media"] = {"type": "frames", "dir": f"media/blender/{sc['id']}", "pad": 4}
            elif frames:
                print(f"[stage] {sc['id']}: {len(frames)}/{sc['frames']} frames rendered — showing slate")
        else:
            # Link the whole directory: Remotion's bundler keeps directory links but not file links.
            f = RENDERS / "manim" / prof / f"{sc['id']}.mp4"
            if f.exists():
                if not (REMOTION_MEDIA / "manim").exists():
                    _link(RENDERS / "manim" / prof, REMOTION_MEDIA / "manim")
                sc["media"] = {"type": "video", "src": f"media/manim/{sc['id']}.mp4"}
        if sc["shot"]:
            ev = EVENTS / f"{sc['shot']}.json"
            sc["events"] = json.loads(ev.read_text()) if ev.exists() else None
    tl["has_sfx"] = SFX_DIR.exists()
    (REMOTION / "public" / "timeline.json").write_text(json.dumps(tl, indent=1))
    write_srt(tl, OUTPUT / f"enigma_{prof}.srt")
    have = sum(1 for s in tl["scenes"] if s["media"])
    print(f"[stage] {prof}: {have}/{len(tl['scenes'])} scenes have media; timeline -> remotion/public/timeline.json")
    return tl


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile")
    a = ap.parse_args(argv)
    stage(a.profile)


if __name__ == "__main__":
    main()
