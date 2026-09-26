"""Render Manim scenes for a profile, skipping scenes whose inputs are unchanged.

    python -m enigma_doc.render_manim                 # all manim scenes, current profile
    python -m enigma_doc.render_manim --scene s0203

Output: renders/manim/<profile>/<scene>.mp4 (exactly the scene's planned length).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys

from .paths import BUILD, RENDERS, ROOT, TIMELINE
from .timeline import load

MODULE_OF_ACT = "manim_scenes.act{:02d}"


def _sig(sc, tl) -> str:
    files = sorted((ROOT / "manim_scenes").glob("*.py"))
    blob = json.dumps([sc, tl["width"], tl["height"], tl["fps"], [f.read_text() for f in files]], sort_keys=True)
    return hashlib.sha1(blob.encode()).hexdigest()


def render_scene(sc: dict, tl: dict, force=False) -> bool:
    out_dir = RENDERS / "manim" / tl["profile"]
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{sc['id']}.mp4"
    sig_file = out.with_suffix(".sha1")
    sig = _sig(sc, tl)
    if not force and out.exists() and sig_file.exists() and sig_file.read_text() == sig:
        print(f"[manim] {sc['id']} up to date")
        return True
    from .script import scene_by_id
    cls = scene_by_id(sc["id"]).cls
    media = BUILD / "manim_media"
    cmd = [sys.executable, "-m", "manim", "render", "--disable_caching", "--progress_bar", "none", "-v", "WARNING",
           "-r", f"{tl['width']},{tl['height']}", "--fps", str(tl["fps"]), "--media_dir", str(media),
           "-o", sc["id"], str(ROOT / "manim_scenes" / f"act{sc['act']:02d}.py"), cls]
    env = dict(os.environ, ENIGMA_ROOT=str(ROOT), PYTHONPATH=f"{ROOT}{os.pathsep}{ROOT / 'src'}")
    print(f"[manim] {sc['id']} {cls} {tl['width']}x{tl['height']}@{tl['fps']}", flush=True)
    r = subprocess.run(cmd, cwd=ROOT, env=env)
    if r.returncode != 0:
        print(f"[manim] {sc['id']} FAILED")
        return False
    produced = next(media.rglob(f"{sc['id']}.mp4"))
    shutil.move(str(produced), out)
    sig_file.write_text(sig)
    return True


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile")
    ap.add_argument("--scene", action="append")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args(argv)
    tl = load(a.profile)
    ok = True
    for sc in tl["scenes"]:
        if sc["tool"] != "manim" or (a.scene and sc["id"] not in a.scene):
            continue
        ok &= render_scene(sc, tl, a.force)
    over = BUILD / "manim_overruns.json"
    if over.exists():
        for sid, items in json.loads(over.read_text()).items():
            for it in items:
                print(f"[manim] WARNING {sid}: animation reached {it['beat']} {it['late_by']}s late")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
