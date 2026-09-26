"""Cameras and lights: the documentary's photographic grammar.

Physical engineering = macro lenses, shallow depth of field, warm key light,
cool rim, near-black world. Camera cuts inside a shot use timeline markers bound
to cameras, so one image sequence can contain several angles.
"""
from __future__ import annotations

import math

import bpy
from mathutils import Vector

from . import util as U


def lights(scene, col=None, strength=1.0):
    col = col or U.collection("LIGHTS")
    world = bpy.data.worlds.new("WORLD_dark")
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.004, 0.0045, 0.006, 1)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 1.0
    scene.world = world
    specs = [  # name, location, energy (W), colour, size
        ("LIGHT_key", (-0.35, -0.45, 0.55), 22, (1.0, 0.86, 0.70), 0.25),
        ("LIGHT_fill", (0.45, -0.35, 0.25), 4, (0.85, 0.9, 1.0), 0.4),
        ("LIGHT_rim", (0.1, 0.55, 0.45), 30, (0.75, 0.85, 1.0), 0.15),
        ("LIGHT_top", (0.0, 0.05, 0.6), 5, (1.0, 0.95, 0.9), 0.3),
    ]
    out = {}
    for name, loc, energy, color, size in specs:
        ld = bpy.data.lights.new(name, "AREA")
        ld.energy = energy * strength
        ld.color = color
        ld.size = size
        ob = bpy.data.objects.new(name, ld)
        ob.location = loc
        col.objects.link(ob)
        _aim(ob, Vector((0, -0.02, 0.1)))
        out[name] = ob
    return out


def _aim(ob, target):
    d = Vector(target) - ob.location
    ob.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()


def camera(name, lens=50.0, fstop=4.0, col=None):
    col = col or U.collection("CAMERAS")
    cd = bpy.data.cameras.new(name)
    cd.lens = lens
    cd.sensor_width = 36
    cd.clip_start = 0.002
    cd.clip_end = 20
    cd.dof.use_dof = True
    cd.dof.aperture_fstop = fstop
    cam = bpy.data.objects.new(name, cd)
    col.objects.link(cam)
    target = U.empty(f"{name}_target", col, (0, 0, 0.1), size=0.01)
    con = cam.constraints.new("TRACK_TO")
    con.target = target
    con.track_axis = "TRACK_NEGATIVE_Z"
    con.up_axis = "UP_Y"
    cd.dof.focus_object = target
    return cam, target


def move(cam, target, t, fps, loc=None, look=None, interp="BEZIER"):
    f = U.sec(t, fps)
    if loc is not None:
        U.key(cam, "location", f, tuple(loc), interp=interp)
    if look is not None:
        U.key(target, "location", f, tuple(look), interp=interp)


def orbit_points(center, radius, height, a0_deg, a1_deg, n=6):
    cx, cy, cz = center
    out = []
    for i in range(n):
        a = math.radians(a0_deg + (a1_deg - a0_deg) * i / (n - 1))
        out.append((cx + radius * math.sin(a), cy - radius * math.cos(a), cz + height))
    return out


def cut(scene, cam, t, fps):
    """Switch the active camera at time t (a marker bound to the camera)."""
    m = scene.timeline_markers.new(f"cut_{cam.name}_{t:.2f}", frame=int(round(U.sec(t, fps))))
    m.camera = cam
    if scene.camera is None:
        scene.camera = cam
    return m
