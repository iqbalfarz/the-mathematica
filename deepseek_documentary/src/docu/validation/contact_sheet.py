"""Contact sheets for visual review: one frame near the end of each beat,
tiled into a single PNG per scene (build/review/<quality>/<scene>.png)."""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from ..paths import BUILD, SCENES_OUT
from ..rendering.presets import resolve_quality
from ..script import load_script


def sheet(spec, q, cols=3) -> Path | None:
    od = SCENES_OUT / q["name"]
    mp4 = od / f"{spec.filename}.mp4"
    tl = od / f"{spec.filename}.timeline.json"
    if not (mp4.exists() and tl.exists()):
        return None
    t = json.loads(tl.read_text())
    starts = t["starts"]
    ids = [b.id for b in spec.beats]
    times = []
    for k, bid in enumerate(ids):
        end = starts[ids[k + 1]] - 0.35 if k + 1 < len(ids) else t["duration"] - 1.4
        times.append(max(0.0, end))
    out = BUILD / "review" / q["name"]
    out.mkdir(parents=True, exist_ok=True)
    frames = []
    for k, tt in enumerate(times):
        f = out / f"_{spec.id}_{k}.png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{tt:.2f}", "-i", str(mp4), "-frames:v", "1",
                        "-vf", "scale=640:-2", str(f)], check=True)
        frames.append(f)
    rows = (len(frames) + cols - 1) // cols
    inputs = []
    for f in frames:
        inputs += ["-i", str(f)]
    n = len(frames)
    layout = "|".join(f"{(k % cols) * 640}_{(k // cols) * 360}" for k in range(n))
    dst = out / f"{spec.filename}_{spec.id}.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex",
                    f"xstack=inputs={n}:layout={layout}:fill=0x202020" if n > 1 else "null", str(dst)], check=True)
    for f in frames:
        f.unlink()
    return dst


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--quality")
    ap.add_argument("--scenes")
    ap.add_argument("--act")
    a = ap.parse_args(argv)
    q = resolve_quality(a.quality)
    for s in load_script():
        if a.scenes and s.id not in a.scenes.split(","):
            continue
        if a.act and str(s.act) not in a.act.split(","):
            continue
        p = sheet(s, q)
        tl = SCENES_OUT / q["name"] / f"{s.filename}.timeline.json"
        v = json.loads(tl.read_text())["violations"] if tl.exists() else "n/a"
        print(s.id, p, v)


if __name__ == "__main__":
    main()
