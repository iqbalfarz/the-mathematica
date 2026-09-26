"""Tracked labels: project 3D anchors to screen space so Remotion can draw
crisp typography exactly on the parts (never baked into the 3D render).

    labels = Labels(ctx)
    labels.track("KEYBOARD", "ENIGMA_keycap_G", t0, t1)
    labels.track("ROTORS", (0.0, 0.075, 0.16), t0, t1)
    labels.caption(t, "right rotor  A → Q")
    labels.write(out_dir / "labels.json")

Positions are normalised (0..1, origin top-left) per frame, following the
active camera (including marker cuts). An anchor behind the camera or outside
the frame is written as null, and Remotion hides the label there.
"""
from __future__ import annotations

import json

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

from . import util as U


class Labels:
    def __init__(self, ctx):
        self.ctx = ctx
        self.items: list[dict] = []
        self.captions: list[dict] = []

    def track(self, text: str, anchor, t0: float, t1: float, offset=(0, 0, 0)):
        self.items.append({"text": text, "anchor": anchor, "t0": t0, "t1": t1, "offset": offset})

    def caption(self, t: float, text: str, until: float | None = None):
        self.captions.append({"t": round(t, 3), "text": text, "until": until})

    def _point(self, anchor, offset):
        if isinstance(anchor, str):
            ob = bpy.data.objects[anchor]
            base = ob.matrix_world.translation
        else:
            base = Vector(anchor)
        return base + Vector(offset)

    def _camera_at(self, frame):
        cam = self.ctx.scene.camera
        best = -1
        for m in self.ctx.scene.timeline_markers:
            if m.camera and m.frame <= frame and m.frame > best:
                best, cam = m.frame, m.camera
        return cam

    def compute(self) -> dict:
        scene, fps = self.ctx.scene, self.ctx.fps
        out = []
        for it in self.items:
            f0, f1 = int(U.sec(it["t0"], fps)), int(U.sec(it["t1"], fps))
            track = []
            for f in range(f0, f1 + 1):
                scene.frame_set(f)
                cam = self._camera_at(f)
                co = world_to_camera_view(scene, cam, self._point(it["anchor"], it["offset"]))
                ok = co.z > 0 and 0.0 <= co.x <= 1.0 and 0.0 <= co.y <= 1.0
                track.append([round(co.x, 4), round(1.0 - co.y, 4)] if ok else None)
            out.append({"text": it["text"], "t0": it["t0"], "t1": it["t1"], "frame0": f0, "track": track})
        return {"fps": fps, "labels": out, "captions": self.captions}

    def write(self, path):
        data = self.compute()
        path.write_text(json.dumps(data))
        return data
