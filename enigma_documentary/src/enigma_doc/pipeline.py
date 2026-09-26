"""One entry point for the whole local pipeline (Windows, macOS, Linux).

    python run.py doctor                    # check tools, print install hints
    python run.py all --profile draft       # everything, in order
    python run.py estimate --profile final  # 1 frame per Blender shot -> projected hours
    python run.py blender --profile final --scene s0101
    python run.py studio                    # open Remotion Studio to scrub the edit

Steps of `all`: test, ledger, voice, events, sfx, timeline, blender, manim, stage, remotion.
Every step is resumable/cached, so re-running `all` only redoes what changed.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

from .paths import OUTPUT, REMOTION, ROOT, ensure_dirs

STEPS = ["test", "ledger", "voice", "events", "sfx", "timeline", "blender", "manim", "stage", "remotion"]


def sh(cmd, cwd=ROOT, env=None, check=True):
    print("$ " + " ".join(str(c) for c in cmd), flush=True)
    e = dict(os.environ, PYTHONPATH=os.pathsep.join([str(ROOT / "src"), str(ROOT)]), ENIGMA_ROOT=str(ROOT))
    if env:
        e.update(env)
    r = subprocess.run([str(c) for c in cmd], cwd=cwd, env=e)
    if check and r.returncode != 0:
        raise SystemExit(f"step failed ({r.returncode}): {' '.join(str(c) for c in cmd)}")
    return r.returncode


# ------------------------------------------------------------------ tool discovery
def find_blender() -> str | None:
    cand = [os.environ.get("BLENDER"), shutil.which("blender")]
    if platform.system() == "Windows":
        base = Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "Blender Foundation"
        cand += sorted((str(p / "blender.exe") for p in base.glob("Blender *")), reverse=True)
    elif platform.system() == "Darwin":
        cand += ["/Applications/Blender.app/Contents/MacOS/Blender"]
    else:
        cand += sorted((str(p) for p in Path.home().glob("blender-*/blender")), reverse=True)
        cand += ["/snap/bin/blender", "/opt/blender/blender"]
    for c in cand:
        if c and Path(c).exists():
            return c
    return None


def find_npx() -> str | None:
    return shutil.which("npx.cmd" if platform.system() == "Windows" else "npx") or shutil.which("npx")


def blender_version(exe) -> tuple[int, int] | None:
    try:
        out = subprocess.run([exe, "--version"], capture_output=True, text=True, timeout=60).stdout
        m = re.search(r"Blender (\d+)\.(\d+)", out)
        return (int(m.group(1)), int(m.group(2))) if m else None
    except Exception:
        return None


def doctor(_a=None) -> bool:
    ok = True

    def line(good, what, hint=""):
        nonlocal ok
        ok &= bool(good)
        print(f"  [{'ok' if good else '!!'}] {what}" + ("" if good else f"\n       -> {hint}"))

    print("Enigma documentary — local toolchain check\n")
    line(sys.version_info >= (3, 10), f"Python {platform.python_version()}", "install Python 3.10-3.12")
    for mod, hint in [("yaml", "pip install -r requirements.txt"), ("numpy", "pip install -r requirements.txt"),
                      ("scipy", "pip install -r requirements.txt"), ("soundfile", "pip install -r requirements.txt"),
                      ("manim", "pip install -r requirements.txt  (Linux: sudo apt install libpango1.0-dev first)"),
                      ("kokoro_onnx", "pip install -r requirements.txt"), ("pytest", "pip install -r requirements.txt")]:
        try:
            __import__(mod)
            line(True, f"python module {mod}")
        except Exception:
            line(False, f"python module {mod}", hint)
    exe = find_blender()
    ver = blender_version(exe) if exe else None
    line(exe and ver and ver >= (4, 2), f"Blender {'.'.join(map(str, ver)) if ver else 'not found'} ({exe or '-'})",
         "install Blender 4.2 LTS or newer from blender.org; or set BLENDER=/path/to/blender")
    npx = find_npx()
    node = shutil.which("node")
    nv = subprocess.run([node, "--version"], capture_output=True, text=True).stdout.strip() if node else ""
    line(node and int(nv.lstrip("v").split(".")[0] or 0) >= 18, f"Node.js {nv or 'not found'}",
         "install Node.js 20 LTS from nodejs.org")
    line(npx, "npx", "comes with Node.js")
    line((REMOTION / "node_modules" / "remotion").exists(), "Remotion packages installed",
         "cd remotion && npm install")
    try:
        import manimpango
        fonts = set(manimpango.list_fonts())
        line("IBM Plex Sans" in fonts and "IBM Plex Mono" in fonts, "IBM Plex fonts (optional; fallbacks work)",
             "free from fonts.google.com: IBM Plex Sans + IBM Plex Mono (install for all users)")
    except Exception:
        pass
    free = shutil.disk_usage(ROOT).free / 2 ** 30
    line(free > 20, f"{free:.0f} GB free disk", "final 1080p frames for Acts I-II need ~5 GB; keep 20 GB free")
    print("\nAll good." if ok else "\nFix the [!!] lines, then run: python run.py all --profile draft")
    return ok


# ------------------------------------------------------------------ steps
def timeline_data(profile):
    from .timeline import load
    return load(profile)


def step_test(a):
    sh([sys.executable, "-m", "pytest", "-q", "tests"])


def step_ledger(a):
    sh([sys.executable, "research/build_ledger.py"])


def step_voice(a):
    sh([sys.executable, "-m", "enigma_doc.narration.generate_voice"])


def step_events(a):
    sh([sys.executable, "-m", "enigma_core", "shots"])


def step_sfx(a):
    sh([sys.executable, "-m", "enigma_doc.audio.sfx"])


def step_timeline(a):
    sh([sys.executable, "-m", "enigma_doc.timeline", "--profile", a.profile])


def _blender_scenes(a):
    tl = timeline_data(a.profile)
    return [s for s in tl["scenes"] if s["tool"] == "blender" and (not a.scene or s["id"] in a.scene)]


def step_blender(a, extra=()):
    exe = find_blender()
    if not exe:
        raise SystemExit("Blender not found. Install Blender 4.2 LTS+ or set BLENDER=/path/to/blender")
    for s in _blender_scenes(a):
        t0 = time.time()
        sh([exe, "-b", "--factory-startup", "-P", ROOT / "blender" / "render.py", "--", "--scene", s["id"], *extra])
        print(f"[blender] {s['id']} took {(time.time() - t0) / 60:.1f} min", flush=True)


def step_estimate(a):
    step_timeline(a)
    step_blender(a, extra=("--estimate",))
    est = ROOT / "build" / "estimate" / "estimates.json"
    data = json.loads(est.read_text())
    rows = [(k, v) for k, v in data.items() if k.startswith(a.profile + ":")]
    total = sum(v["hours"] for _, v in rows)
    print(f"\nProjected Blender render time for profile '{a.profile}':")
    for k, v in rows:
        print(f"  {k.split(':')[1]}: {v['sec_per_frame']:.1f} s/frame x {v['frames']} = {v['hours']:.2f} h ({v['device']})")
    print(f"  total: {total:.1f} h   (Manim and Remotion add minutes, not hours)")
    print(f"  sample frames: {ROOT / 'build' / 'estimate'}")


def step_manim(a):
    cmd = [sys.executable, "-m", "enigma_doc.render_manim", "--profile", a.profile]
    for s in a.scene or []:
        cmd += ["--scene", s]
    sh(cmd)


def step_stage(a):
    sh([sys.executable, "-m", "enigma_doc.stage", "--profile", a.profile])


def step_remotion(a):
    npx = find_npx()
    if not npx:
        raise SystemExit("npx not found: install Node.js 20 LTS")
    if not (REMOTION / "node_modules" / "remotion").exists():
        sh([shutil.which("npm.cmd" if platform.system() == "Windows" else "npm") or "npm", "install"], cwd=REMOTION)
    tl = timeline_data(a.profile)
    ensure_dirs()
    out = OUTPUT / f"enigma_{a.profile}.mp4"
    extra = ["--browser-executable", os.environ["REMOTION_BROWSER"]] if os.environ.get("REMOTION_BROWSER") else []
    sh([npx, "remotion", "render", "src/index.ts", "EnigmaFilm", out, "--crf", str(tl["crf"]),
        "--concurrency", str(a.concurrency or max(1, (os.cpu_count() or 2) // 2)), *extra], cwd=REMOTION)
    print(f"\n[done] {out}\n       captions: {out.with_suffix('.srt')}")


def step_studio(a):
    step_stage(a)
    sh([find_npx(), "remotion", "studio", "src/index.ts"], cwd=REMOTION)


STEP_FN = {"test": step_test, "ledger": step_ledger, "voice": step_voice, "events": step_events, "sfx": step_sfx,
           "timeline": step_timeline, "blender": step_blender, "manim": step_manim, "stage": step_stage,
           "remotion": step_remotion}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("step", choices=["doctor", "all", "estimate", "studio", *STEPS])
    ap.add_argument("--profile", default=os.environ.get("PROFILE", "draft"))
    ap.add_argument("--scene", action="append", help="limit blender/manim to these scene ids")
    ap.add_argument("--from", dest="start", choices=STEPS, help="with `all`: start at this step")
    ap.add_argument("--concurrency", type=int, help="Remotion render threads")
    a = ap.parse_args(argv)
    os.environ["PROFILE"] = a.profile
    if a.step == "doctor":
        sys.exit(0 if doctor() else 1)
    if a.step == "estimate":
        return step_estimate(a)
    if a.step == "studio":
        return step_studio(a)
    if a.step == "all":
        steps = STEPS[STEPS.index(a.start):] if a.start else STEPS
        t0 = time.time()
        for s in steps:
            print(f"\n=== {s} ({a.profile}) ===", flush=True)
            STEP_FN[s](a)
        print(f"\nfinished in {(time.time() - t0) / 3600:.2f} h")
        return
    STEP_FN[a.step](a)


if __name__ == "__main__":
    main()
