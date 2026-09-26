"""Render one Blender shot for one profile, resumably.

Run with Blender 4.2 LTS or newer (headless):
    blender -b --factory-startup -P blender/render.py -- --scene s0101
    blender -b --factory-startup -P blender/render.py -- --scene s0101 --estimate
    blender -b --factory-startup -P blender/render.py -- --scene s0101 --save-blend
or with the `bpy` pip module:  python blender/render.py --scene s0101

Inputs (written by the project Python first, see Makefile):
    build/timeline.json          profile, fps, size, beat times, render settings
    build/events/<shot>.json     simulator event stream for the shot
Output:
    renders/blender/<profile>/<scene>/frame_0001.png ...

Resumable: finished frames are skipped; a frame interrupted mid-render leaves
an empty placeholder that is deleted and re-rendered on the next run.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

import bpy  # noqa: E402

from enigma_model.build import build_enigma  # noqa: E402
from lib import staging  # noqa: E402
from lib import util as U  # noqa: E402


class Ctx:
    def __init__(self, scene, rig, timeline, sc, stream, lights):
        self.scene, self.rig, self.timeline, self.sc, self.stream, self.lights = scene, rig, timeline, sc, stream, lights
        self.fps = timeline["fps"]
        self.duration = sc["duration"]

    def beat(self, ref: str) -> float:
        import re
        m = re.fullmatch(r"(b\d+)(\.end)?([+-]\d+(?:\.\d+)?)?", ref.strip())
        b = next(x for x in self.sc["beats"] if x["id"] == m.group(1))
        t = b["start"] + (b["dur"] if m.group(2) else 0.0)
        return t + (float(m.group(3)) if m.group(3) else 0.0)

    def load_stream(self, shot_id: str) -> dict:
        return json.loads((ROOT / "build" / "events" / f"{shot_id}.json").read_text())


def _args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    ap = argparse.ArgumentParser()
    ap.add_argument("--scene", required=True)
    ap.add_argument("--estimate", action="store_true", help="render 1 frame and project the total time")
    ap.add_argument("--save-blend", action="store_true", help="also save build/blend/<scene>.blend to inspect")
    ap.add_argument("--frames", help="subset, e.g. 1-120 (for running several processes)")
    ap.add_argument("--no-render", action="store_true")
    ap.add_argument("--timeline", default=str(ROOT / "build" / "timeline.json"))
    return ap.parse_args(argv)


def setup_device(scene):
    want = os.environ.get("BLENDER_DEVICE", "AUTO").upper()
    scene.cycles.device = "CPU"
    if want == "CPU":
        return "CPU"
    try:
        prefs = bpy.context.preferences.addons["cycles"].preferences
        for backend in ("OPTIX", "CUDA", "HIP", "METAL", "ONEAPI"):
            try:
                prefs.compute_device_type = backend
            except TypeError:
                continue
            prefs.get_devices()
            gpus = [d for d in prefs.devices if d.type != "CPU"]
            if gpus:
                for d in prefs.devices:
                    d.use = d.type != "CPU"
                scene.cycles.device = "GPU"
                return f"GPU/{backend}"
    except Exception as e:  # pragma: no cover - depends on the machine
        print(f"[render] GPU setup failed, using CPU: {e}")
    return "CPU"


def configure(scene, tl):
    r = dict(tl["render"])
    if os.environ.get("SAMPLES"):
        r["samples"] = int(os.environ["SAMPLES"])
    scene.render.resolution_x, scene.render.resolution_y = tl["width"], tl["height"]
    scene.render.resolution_percentage = 100
    scene.render.fps = tl["fps"]
    if r.get("engine", "CYCLES").upper() == "EEVEE":
        _eevee(scene, r)
    else:
        scene.render.engine = "CYCLES"
        scene.cycles.samples = r["samples"]
        scene.cycles.use_adaptive_sampling = True
        scene.cycles.adaptive_threshold = 0.05
        scene.cycles.max_bounces = r["bounces"]
        scene.cycles.transparent_max_bounces = 4
        scene.cycles.caustics_reflective = False
        scene.cycles.caustics_refractive = False
        scene.cycles.use_denoising = bool(r["denoise"])
        if r["denoise"]:
            scene.cycles.denoiser = "OPENIMAGEDENOISE"
            try:
                scene.cycles.denoising_input_passes = "RGB_ALBEDO_NORMAL"
                scene.cycles.denoising_prefilter = "ACCURATE"
            except (AttributeError, TypeError):
                pass
    # Keep the built scene between frames: much faster, and this scene is small.
    scene.render.use_persistent_data = True
    scene.render.film_transparent = False
    try:
        scene.view_settings.view_transform = "AgX"
        scene.view_settings.look = "AgX - Medium High Contrast"
    except TypeError:
        pass
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_depth = "8"
    scene.render.image_settings.compression = 30
    scene.render.use_overwrite = False
    scene.render.use_placeholder = True
    threads = os.environ.get("BLENDER_THREADS")
    if threads:
        scene.render.threads_mode = "FIXED"
        scene.render.threads = int(threads)


def _eevee(scene, r):
    """EEVEE (Blender 4.2+ 'EEVEE Next'). Needs a GPU/OpenGL 4.3 context, even integrated."""
    for name in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
        try:
            scene.render.engine = name
            break
        except TypeError:
            continue
    ev = scene.eevee
    ev.taa_render_samples = r["samples"]
    for attr, val in (("use_raytracing", True), ("use_shadows", True), ("use_gtao", True),
                      ("shadow_ray_count", 2), ("shadow_step_count", 8)):
        if hasattr(ev, attr):
            setattr(ev, attr, val)
    if hasattr(ev, "ray_tracing_options"):
        ev.ray_tracing_options.resolution_scale = "1"
        if hasattr(ev.ray_tracing_options, "use_denoise"):
            ev.ray_tracing_options.use_denoise = True


def main():
    a = _args()
    tl = json.loads(Path(a.timeline).read_text())
    sc = next(s for s in tl["scenes"] if s["id"] == a.scene)
    if sc["tool"] != "blender":
        raise SystemExit(f"{a.scene} is a {sc['tool']} scene")
    shot_spec = tl["shots"][sc["shot"]]
    stream_path = ROOT / "build" / "events" / f"{sc['shot']}.json"
    stream = json.loads(stream_path.read_text())

    scene = U.reset_scene()
    configure(scene, tl)
    device = setup_device(scene)
    rig = build_enigma(stream["config"])
    lights = staging.lights(scene)
    mod = importlib.import_module(f"shots.{a.scene}")
    ctx = Ctx(scene, rig, tl, sc, stream, lights)
    mod.build(ctx)
    scene.frame_start, scene.frame_end = 1, sc["frames"]
    if a.frames:
        lo, hi = (int(x) for x in a.frames.split("-"))
        scene.frame_start, scene.frame_end = max(1, lo), min(sc["frames"], hi)

    out_dir = ROOT / "renders" / "blender" / tl["profile"] / a.scene
    out_dir.mkdir(parents=True, exist_ok=True)
    # Invalidate old frames if the shot definition changed (code, stream, timing, profile).
    sig = hashlib.sha1(json.dumps([sc, shot_spec, stream, tl["render"], tl["width"], tl["fps"],
                                   (HERE / "shots" / f"{a.scene}.py").read_text(),
                                   *[(p.name, p.read_text()) for p in sorted((HERE / "lib").glob("*.py"))],
                                   (HERE / "enigma_model" / "build.py").read_text()],
                                  sort_keys=True).encode()).hexdigest()
    sig_file = out_dir / "shot.sha1"
    if sig_file.exists() and sig_file.read_text() != sig and not a.estimate:
        print(f"[render] {a.scene}: shot changed since last render, clearing old frames")
        for f in out_dir.glob("frame_*.png"):
            f.unlink()
    for f in out_dir.glob("frame_*.png"):
        if f.stat().st_size == 0:
            f.unlink()          # placeholder of an interrupted frame
    scene.render.filepath = str(out_dir / "frame_")

    if a.save_blend:
        blend = ROOT / "build" / "blend" / f"{a.scene}.blend"
        blend.parent.mkdir(parents=True, exist_ok=True)
        bpy.ops.wm.save_as_mainfile(filepath=str(blend))
        print(f"[render] saved {blend}")
    if a.no_render:
        return
    if a.estimate:
        mid = (scene.frame_start + scene.frame_end) // 2
        scene.frame_set(mid)
        scene.render.filepath = str(ROOT / "build" / "estimate" / f"{a.scene}_frame.png")
        scene.render.use_overwrite = True
        t0 = time.time()
        bpy.ops.render.render(write_still=True)
        dt = time.time() - t0
        total = dt * sc["frames"]
        print(f"[estimate] {a.scene} {tl['profile']} {tl['width']}x{tl['height']} on {device}: "
              f"{dt:.1f}s/frame x {sc['frames']} frames = {total/3600:.2f} h")
        est = ROOT / "build" / "estimate" / "estimates.json"
        data = json.loads(est.read_text()) if est.exists() else {}
        data[f"{tl['profile']}:{a.scene}"] = {"sec_per_frame": dt, "frames": sc["frames"], "hours": total / 3600,
                                             "device": device}
        est.write_text(json.dumps(data, indent=1))
        return
    done = len([f for f in out_dir.glob("frame_*.png") if f.stat().st_size > 0])
    print(f"[render] {a.scene} {tl['profile']} {tl['width']}x{tl['height']}@{tl['fps']} on {device}: "
          f"{sc['frames']} frames ({done} already done)")
    t0 = time.time()
    bpy.ops.render.render(animation=True)
    sig_file.write_text(sig)
    print(f"[render] {a.scene} finished in {(time.time()-t0)/60:.1f} min -> {out_dir}")


main()
