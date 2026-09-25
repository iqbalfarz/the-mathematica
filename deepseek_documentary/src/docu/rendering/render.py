"""Scene-level, cached, resumable render queue.

    python -m docu.rendering.render --quality preview            # everything
    python -m docu.rendering.render --quality 4k --workers 2
    python -m docu.rendering.render --resolution 3840x2160 --fps 60
    python -m docu.rendering.render --scenes s0301,s0302 --force
    python -m docu.rendering.render --act 4
    python -m docu.rendering.render --shard 2/8                   # CI matrix sharding
    python -m docu.rendering.render --list

Each scene renders to build/scenes/<quality>/scene_NNN.mp4. A content hash of the
scene's code, shared components, script beats and narration timing is stored next
to it; unchanged scenes are skipped, so a failed scene 37 re-renders only scene 37.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

from ..paths import BUILD, LOGS, ROOT, SCENES_OUT, TIMELINE, TIMING
from ..script import load_script
from .presets import resolve_quality

SRC = ROOT / "src"
SHARED = ["docu/base_scene.py", "docu/style.py", "docu/script.py", "docu/paths.py"]


def _scene_hash(spec, q) -> str:
    h = hashlib.sha256()
    for rel in SHARED + [f"docu/scenes/act{spec.act:02d}.py"]:
        h.update((SRC / rel).read_bytes())
    for p in sorted((SRC / "docu/components").glob("*.py")):
        h.update(p.read_bytes())
    h.update(json.dumps([b.__dict__ for b in spec.beats], sort_keys=True).encode())
    if TIMING.exists():
        sc = json.loads(TIMING.read_text())["scenes"].get(spec.id)
        h.update(json.dumps(sc, sort_keys=True).encode())
    h.update(f"{q['width']}x{q['height']}@{q['fps']}".encode())
    return h.hexdigest()[:20]


def out_dir(q) -> Path:
    d = SCENES_OUT / q["name"]
    d.mkdir(parents=True, exist_ok=True)
    return d


def render_one(spec, q, force=False, retries=1) -> dict:
    od = out_dir(q)
    mp4 = od / f"{spec.filename}.mp4"
    keyf = od / f"{spec.filename}.key"
    key = _scene_hash(spec, q)
    if not force and mp4.exists() and keyf.exists() and keyf.read_text() == key:
        return {"scene": spec.id, "status": "cached", "file": str(mp4)}
    media = BUILD / "media" / q["name"] / spec.id
    logd = LOGS / q["name"]
    logd.mkdir(parents=True, exist_ok=True)
    log = logd / f"{spec.filename}_{spec.id}.log"
    cmd = [sys.executable, "-m", "manim", "render",
           "--resolution", f"{q['width']},{q['height']}", "--frame_rate", str(q["fps"]),
           "--media_dir", str(media), "-o", spec.filename, "--disable_caching",
           "--progress_bar", "none", "--format", "mp4",
           str(SRC / "docu" / "scenes" / f"act{spec.act:02d}.py"), spec.cls]
    env = dict(os.environ, PYTHONPATH=str(SRC) + os.pathsep + os.environ.get("PYTHONPATH", ""))
    last = None
    for attempt in range(retries + 1):
        t0 = time.time()
        with log.open("w") as fh:
            fh.write(" ".join(cmd) + "\n")
            fh.flush()
            r = subprocess.run(cmd, stdout=fh, stderr=subprocess.STDOUT, env=env, cwd=str(ROOT))
        found = sorted(media.rglob(f"{spec.filename}.mp4"))
        if r.returncode == 0 and found:
            shutil.move(str(found[-1]), mp4)
            shutil.rmtree(media, ignore_errors=True)
            tl = TIMELINE / f"{spec.id}.json"
            if tl.exists():
                shutil.copy(tl, od / f"{spec.filename}.timeline.json")
            keyf.write_text(key)
            return {"scene": spec.id, "status": "rendered", "file": str(mp4), "seconds": round(time.time() - t0, 1),
                    "attempts": attempt + 1}
        last = f"exit {r.returncode}; see {log}"
    return {"scene": spec.id, "status": "failed", "error": last}


def select(args):
    scenes = load_script()
    if args.scenes:
        want = set(args.scenes.split(","))
        scenes = [s for s in scenes if s.id in want or s.filename in want or str(s.index) in want]
    if args.act:
        acts = {int(a) for a in str(args.act).split(",")}
        scenes = [s for s in scenes if s.act in acts]
    if args.shard:
        i, n = (int(v) for v in args.shard.split("/"))
        scenes = [s for k, s in enumerate(scenes) if k % n == i - 1]
    return scenes


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--quality")
    ap.add_argument("--resolution")
    ap.add_argument("--fps", type=int)
    ap.add_argument("--scenes")
    ap.add_argument("--act")
    ap.add_argument("--shard", help="i/n: render every n-th scene starting at i (1-based)")
    ap.add_argument("--workers", type=int, default=int(os.environ.get("RENDER_WORKERS", os.cpu_count() or 2)))
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--retries", type=int, default=1)
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--compose", action="store_true", help="compose the full film afterwards")
    args = ap.parse_args(argv)

    q = resolve_quality(args.quality, args.resolution, args.fps)
    scenes = select(args)
    if args.list:
        for s in scenes:
            print(f"{s.index:3d} {s.id} act{s.act:02d} {s.cls:28s} {s.title}")
        return
    if not TIMING.exists():
        print("WARNING: no narration timing yet; run `python -m docu.narration.generate_voice` first.")
    state_f = out_dir(q) / "state.json"
    state = json.loads(state_f.read_text()) if state_f.exists() else {}
    print(f"[render] {len(scenes)} scenes at {q['width']}x{q['height']}@{q['fps']} ({q['name']}), "
          f"{args.workers} workers")
    t0 = time.time()
    failed = []
    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(render_one, s, q, args.force, args.retries): s for s in scenes}
        for f in cf.as_completed(futs):
            res = f.result()
            state[res["scene"]] = res
            state_f.write_text(json.dumps(state, indent=1))
            print(f"[render] {res['scene']}: {res['status']} {res.get('seconds', '')} {res.get('error', '')}",
                  flush=True)
            if res["status"] == "failed":
                failed.append(res["scene"])
    print(f"[render] done in {(time.time()-t0)/60:.1f} min; failed: {failed or 'none'}")
    if failed:
        sys.exit(1)
    if args.compose:
        from .compose import compose
        compose(q)


if __name__ == "__main__":
    main()
