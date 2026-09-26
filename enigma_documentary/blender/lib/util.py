"""Small bpy helpers: collections, primitives, text, curves, keyframes.

Written for Blender 4.2 LTS; keyframe helpers also handle the layered-action
API of Blender 4.4+/5.x.
"""
from __future__ import annotations

import math

import bmesh
import bpy
from mathutils import Vector


# ------------------------------------------------------------------ scene
def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    return bpy.context.scene


def collection(name: str, parent=None):
    col = bpy.data.collections.get(name) or bpy.data.collections.new(name)
    parent = parent or bpy.context.scene.collection
    if col.name not in [c.name for c in parent.children]:
        parent.children.link(col)
    return col


def link(obj, col):
    for c in obj.users_collection:
        c.objects.unlink(obj)
    col.objects.link(obj)
    return obj


def empty(name, col, loc=(0, 0, 0), parent=None, size=0.02):
    e = bpy.data.objects.new(name, None)
    e.empty_display_size = size
    e.location = loc
    col.objects.link(e)
    if parent:
        e.parent = parent
    return e


def mesh_object(name, col, bm, material=None, parent=None, loc=(0, 0, 0), smooth=False):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    if smooth:
        for p in me.polygons:
            p.use_smooth = True
    ob = bpy.data.objects.new(name, me)
    ob.location = loc
    col.objects.link(ob)
    if material:
        me.materials.append(material)
    if parent:
        ob.parent = parent
    return ob


# ------------------------------------------------------------------ primitives (bmesh)
def bm_box(sx, sy, sz, bevel=0.0):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=Vector((sx, sy, sz)), verts=bm.verts)
    if bevel > 0:
        bmesh.ops.bevel(bm, geom=list(bm.edges), offset=bevel, segments=2, affect="EDGES", profile=0.5)
    return bm


def bm_cylinder(radius, depth, segments=48, axis="Z", radius2=None, bevel=0.0):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=segments,
                          radius1=radius, radius2=radius if radius2 is None else radius2, depth=depth)
    if bevel > 0:
        rim = [e for e in bm.edges if len(e.link_faces) == 2 and
               abs(e.link_faces[0].normal.dot(e.link_faces[1].normal)) < 0.5]
        bmesh.ops.bevel(bm, geom=rim, offset=bevel, segments=2, affect="EDGES", profile=0.5)
    _orient(bm, axis)
    return bm


def bm_gear(radius, depth, teeth=52, tooth=0.002, axis="X"):
    """Serrated disc (thumbwheel / ratchet): alternating radius around the rim."""
    bm = bmesh.new()
    n = teeth * 2
    top, bot = [], []
    for i in range(n):
        a = 2 * math.pi * i / n
        r = radius + (tooth if i % 2 == 0 else 0.0)
        top.append(bm.verts.new((r * math.cos(a), r * math.sin(a), depth / 2)))
        bot.append(bm.verts.new((r * math.cos(a), r * math.sin(a), -depth / 2)))
    bm.faces.new(top)
    bm.faces.new(list(reversed(bot)))
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new((bot[i], bot[j], top[j], top[i]))
    bm.normal_update()
    _orient(bm, axis)
    return bm


def bm_uv_sphere(radius, segs=24, rings=12):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=segs, v_segments=rings, radius=radius)
    return bm


def _orient(bm, axis):
    if axis == "X":
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=_rot("Y", math.pi / 2))
    elif axis == "Y":
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=_rot("X", math.pi / 2))


def _rot(axis, angle):
    from mathutils import Matrix
    return Matrix.Rotation(angle, 3, axis)


# ------------------------------------------------------------------ text & curves
def text(name, col, body, size, material=None, loc=(0, 0, 0), rot=(0, 0, 0), extrude=0.0,
         parent=None, font=None):
    cu = bpy.data.curves.new(name, "FONT")
    cu.body = body
    cu.size = size
    cu.align_x = "CENTER"
    cu.align_y = "CENTER"
    cu.extrude = extrude
    # Note: don't thicken strokes with cu.offset: it corrupts glyphs with holes (B renders as P).
    if font:
        cu.font = font
    ob = bpy.data.objects.new(name, cu)
    ob.location = loc
    ob.rotation_euler = rot
    col.objects.link(ob)
    if material:
        cu.materials.append(material)
    if parent:
        ob.parent = parent
    return ob


def poly_curve(name, col, points, bevel=0.0007, material=None, parent=None, resolution=4):
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = bevel
    cu.bevel_resolution = resolution
    cu.use_fill_caps = True
    cu.bevel_factor_mapping_start = "SPLINE"
    cu.bevel_factor_mapping_end = "SPLINE"
    add_spline(cu, points)
    ob = bpy.data.objects.new(name, cu)
    col.objects.link(ob)
    if material:
        cu.materials.append(material)
    if parent:
        ob.parent = parent
    return ob


def add_spline(cu, points, smooth=True):
    if smooth and len(points) > 2:
        sp = cu.splines.new("NURBS")
        sp.points.add(len(points) - 1)
        for p, co in zip(sp.points, points):
            p.co = (*co, 1.0)
        sp.order_u = 3
        sp.use_endpoint_u = True
        sp.resolution_u = 12
    else:
        sp = cu.splines.new("POLY")
        sp.points.add(len(points) - 1)
        for p, co in zip(sp.points, points):
            p.co = (*co, 1.0)
    return sp


# ------------------------------------------------------------------ keyframes
def _fcurves(idblock):
    ad = idblock.animation_data
    if not ad or not ad.action:
        return []
    act = ad.action
    if hasattr(act, "fcurves") and len(getattr(act, "fcurves", [])) > 0:
        return list(act.fcurves)
    out = []   # Blender 4.4+ layered actions
    for layer in getattr(act, "layers", []):
        for strip in layer.strips:
            for bag in getattr(strip, "channelbags", []):
                out.extend(bag.fcurves)
    return out


def key(idblock, path, frame, value=None, index=-1, interp="BEZIER", ease="AUTO"):
    """Set a property (optionally) and keyframe it with a given interpolation."""
    if value is not None:
        target, attr = _resolve(idblock, path)
        if index >= 0:
            getattr(target, attr)[index] = value
        else:
            setattr(target, attr, value)
    idblock.keyframe_insert(data_path=path, frame=frame, index=index)
    for fc in _fcurves(idblock):
        if fc.data_path == path and (index < 0 or fc.array_index == index):
            for kp in fc.keyframe_points:
                if abs(kp.co.x - frame) < 1e-4:
                    kp.interpolation = interp
                    kp.easing = ease


def _resolve(idblock, path):
    parts = path.split(".")
    target = idblock
    for p in parts[:-1]:
        target = getattr(target, p)
    return target, parts[-1]


def sec(t: float, fps: int) -> float:
    """Seconds -> (fractional) frame number. Frame 1 is t = 0."""
    return 1 + t * fps
