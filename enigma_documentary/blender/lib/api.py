"""The helper API shots are written in (see design/G_blender_asset_architecture.md).

All times are in seconds from the start of the shot; `fps` converts to frames.
Nothing here decides *what* the machine does -- that always comes from an
enigma_core event stream (see player.py). These helpers only say *how it looks*.
"""
from __future__ import annotations

import math

import bpy

from . import layout as L
from . import util as U

KEY_DOWN = 0.10          # key reaches bottom
STEP_START, STEP_END = 0.03, 0.10   # rotors move while the key is going down
CURRENT_ON = 0.11        # contact closes after stepping: current flows


def _f(t, fps):
    return U.sec(t, fps)


def _objs(rig, prefix):
    return [o for o in bpy.data.objects if o.name.startswith(prefix)]


# ------------------------------------------------------------------ visibility
def set_visible(objs, visible: bool, t: float, fps: int):
    for o in objs:
        U.key(o, "hide_render", _f(t, fps), not visible, interp="CONSTANT")
        U.key(o, "hide_viewport", _f(t, fps), not visible, interp="CONSTANT")


def show_enigma(rig, t=0.0, fps=24):
    set_visible([o for c in rig.cols.values() for o in c.objects if "wires" not in o.name], True, t, fps)


def hide_casing(rig, t: float, fps: int, hide=True):
    """Hide the wooden case, front panel and decks (keeps keys, lamps, rotors)."""
    objs = [o for o in rig.cols["casing"].objects]
    set_visible(objs, not hide, t, fps)


def open_lid(rig, t0: float, dur: float, fps: int, angle_deg=110.0):
    hinge = rig.parts["ENIGMA_lid_hinge"]
    hinge.rotation_mode = "XYZ"
    U.key(hinge, "rotation_euler", _f(t0, fps), 0.0, index=0)
    U.key(hinge, "rotation_euler", _f(t0 + dur, fps), -math.radians(angle_deg), index=0)


def explode_enigma(rig, t0: float, dur: float, fps: int, amount=1.0):
    """Pull the main assemblies apart along readable directions."""
    moves = {"casing": (0, 0, -0.10), "keyboard": (0, -0.12, 0.02), "lampboard": (0, -0.05, 0.07),
             "plugboard": (0, -0.20, -0.04), "stepping": (0, 0, -0.05)}
    for col, d in moves.items():
        for o in rig.cols[col].objects:
            if o.parent is not rig.root:
                continue
            start = tuple(o.location)
            U.key(o, "location", _f(t0, fps), start)
            U.key(o, "location", _f(t0 + dur, fps), tuple(s + amount * v for s, v in zip(start, d)))
    spread = {"reflector": -0.05, "left": -0.025, "middle": 0.0, "right": 0.025, "entry": 0.05}
    for slot, dx in spread.items():
        o = rig.rotors.get(slot) or rig.parts.get({"reflector": "ENIGMA_reflector",
                                                    "entry": "ENIGMA_entry_wheel"}.get(slot, ""))
        if o is None:
            continue
        start = tuple(o.location)
        U.key(o, "location", _f(t0, fps), start)
        U.key(o, "location", _f(t0 + dur, fps), (start[0] + amount * dx, start[1], start[2] + amount * 0.04))


def focus_rotor(rig, slot: str):
    return rig.rotors[slot]


def show_wiring(rig, t: float, fps: int, slots=("left", "middle", "right"), on=True):
    """Reveal internal wires; rotor bodies switch to smoked glass (keyed on/off)."""
    for slot in slots:
        set_visible([rig.parts[f"ENIGMA_rotor_{slot}_wires"]], on, t, fps)
    if "reflector" in slots or slots == ("left", "middle", "right"):
        set_visible([rig.parts["ENIGMA_reflector_wires"]], on, t, fps)
    glass = rig.mats["core_glass"]
    for slot in slots:
        body = bpy.data.objects.get(f"ENIGMA_rotor_{slot}_body")
        if body and on:
            body.data.materials.clear()
            body.data.materials.append(glass)


# ------------------------------------------------------------------ keys, lamps
def animate_key(rig, letter: str, t: float, fps: int, hold=0.5):
    stem = rig.keys[letter]
    z0 = stem.location.z
    U.key(stem, "location", _f(t, fps), z0, index=2)
    U.key(stem, "location", _f(t + KEY_DOWN, fps), z0 - L.KEY_TRAVEL, index=2)
    U.key(stem, "location", _f(t + hold, fps), z0 - L.KEY_TRAVEL, index=2)
    U.key(stem, "location", _f(t + hold + 0.12, fps), z0, index=2)


def animate_lamp(rig, letter: str, t_on: float, t_off: float, fps: int):
    for ob in rig.lamps[letter]:
        U.key(ob, "color", _f(max(0.0, t_on - 1 / fps), fps), (0, 0, 0, 1), interp="CONSTANT")
        U.key(ob, "color", _f(t_on, fps), (1, 1, 1, 1), interp="CONSTANT")
        U.key(ob, "color", _f(t_off, fps), (0, 0, 0, 1), interp="CONSTANT")


# ------------------------------------------------------------------ rotors & stepping
def set_rotor_positions(rig, letters: str, t: float, fps: int):
    for slot, ch in zip(("left", "middle", "right"), letters):
        a = L.rotor_angle(ord(ch) - 65)
        rig.rotors[slot]["angle"] = a
        U.key(rig.rotors[slot], "rotation_euler", _f(t, fps), a, index=0, interp="CONSTANT")


def rotate_rotor(rig, slot: str, from_letter: str, t0: float, dur: float, fps: int, steps=1):
    """Advance a rotor `steps` positions (always forward, never the short way round)."""
    r = rig.rotors[slot]
    # Keep a running angle so Z -> A keeps turning forward instead of unwinding a full turn.
    a0 = r.get("angle", L.rotor_angle(ord(from_letter) - 65))
    expected = L.rotor_angle(ord(from_letter) - 65)
    if abs(((a0 - expected + math.pi) % (2 * math.pi)) - math.pi) > 1e-6:
        raise ValueError(f"rotor {slot} is not showing {from_letter}: rig and simulator disagree")
    U.key(r, "rotation_euler", _f(t0, fps), a0, index=0)
    U.key(r, "rotation_euler", _f(t0 + dur, fps), a0 - steps * L.STEP, index=0, interp="BEZIER", ease="EASE_OUT")
    r["angle"] = a0 - steps * L.STEP


def animate_pawls(rig, steps: list, t: float, fps: int):
    """All three pawls swing up on every key press; those that engage push a rotor."""
    engaged = {s["pawl"] for s in steps}
    for pawl, pivot in rig.pawls.items():
        lift = math.radians(14 if pawl in engaged else 9)
        U.key(pivot, "rotation_euler", _f(t, fps), 0.0, index=0)
        U.key(pivot, "rotation_euler", _f(t + STEP_END, fps), -lift, index=0)
        U.key(pivot, "rotation_euler", _f(t + 0.45, fps), -lift, index=0)
        U.key(pivot, "rotation_euler", _f(t + 0.6, fps), 0.0, index=0)
    lever = rig.parts["ENIGMA_stepping_lever"]
    U.key(lever, "rotation_euler", _f(t, fps), 0.0, index=0)
    U.key(lever, "rotation_euler", _f(t + KEY_DOWN, fps), math.radians(6), index=0)
    U.key(lever, "rotation_euler", _f(t + 0.6, fps), 0.0, index=0)


# ------------------------------------------------------------------ current
def show_signal_path(rig, press: dict, t0: float, dur: float, fps: int, t_off: float | None = None,
                     pulse_len=0.12):
    """Draw the current for one key press: a glowing trace that grows from key to
    lamp over `dur` seconds, plus a brighter travelling pulse at its head."""
    fwd, back = L.signal_points(press)
    col = rig.cols["signal"]
    tag = f"{press['index']:03d}"
    objs = []
    for part, pts, mat in (("fwd", fwd, rig.mats["signal"]), ("ret", back, rig.mats["signal_return"])):
        trace = U.poly_curve(f"ENIGMA_signal_{tag}_{part}", col, pts, bevel=0.0009, material=mat,
                             parent=rig.root)
        trace.color = (1, 1, 1, 1)
        objs.append(trace)
    half = dur / 2
    for ob, (a, b) in zip(objs, ((t0, t0 + half), (t0 + half, t0 + dur))):
        cu = ob.data
        U.key(cu, "bevel_factor_end", _f(0, fps), 0.0, interp="CONSTANT")
        U.key(cu, "bevel_factor_end", _f(a, fps), 0.0, interp="LINEAR")
        U.key(cu, "bevel_factor_end", _f(b, fps), 1.0, interp="LINEAR")
        if t_off is not None:
            U.key(ob, "color", _f(t_off - 0.2, fps), (1, 1, 1, 1))
            U.key(ob, "color", _f(t_off, fps), (0, 0, 0, 1))
    return objs


def set_plugboard(rig, spec: str):
    from enigma_model.build import set_plugboard as _sp
    _sp(rig, spec)
