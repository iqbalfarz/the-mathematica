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
        # Blender holds an object's first key backwards to frame 1, so an object first
        # keyed "hidden" at t would vanish from the start of the shot. Key its current
        # state at the start first.
        if t > 0 and not _has_fcurve(o, "hide_render"):
            U.key(o, "hide_render", _f(0.0, fps), o.hide_render, interp="CONSTANT")
            U.key(o, "hide_viewport", _f(0.0, fps), o.hide_viewport, interp="CONSTANT")
        U.key(o, "hide_render", _f(t, fps), not visible, interp="CONSTANT")
        U.key(o, "hide_viewport", _f(t, fps), not visible, interp="CONSTANT")


def _has_fcurve(o, path):
    return any(fc.data_path == path for fc in U._fcurves(o))


def show_enigma(rig, t=0.0, fps=24):
    set_visible([o for c in rig.cols.values() for o in c.objects if "wires" not in o.name], True, t, fps)


def hide_casing(rig, t: float, fps: int, hide=True, keep=("ENIGMA_case_base",)):
    """Hide the wooden case, front panel and decks (keeps keys, lamps, rotors and,
    by default, the base board so the parts don't float in a void)."""
    objs = [o for o in rig.cols["casing"].objects if o.name not in keep]
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
    # Rotor bodies and alphabet rings turn to smoked glass so the copper wiring
    # inside is visible; ring letters stay, floating on the glass.
    glass = rig.mats["core_glass"]
    for slot in slots:
        for part in ("body", "ring"):
            ob = bpy.data.objects.get(f"ENIGMA_rotor_{slot}_{part}")
            if ob and on:
                ob.data.materials.clear()
                ob.data.materials.append(glass)


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


def rotate_rotor(rig, slot: str, from_letter: str, t0: float, dur: float, fps: int, steps=1, ease="EASE_OUT"):
    """Advance a rotor `steps` positions (always forward, never the short way round)."""
    r = rig.rotors[slot]
    # Keep a running angle so Z -> A keeps turning forward instead of unwinding a full turn.
    a0 = r.get("angle", L.rotor_angle(ord(from_letter) - 65))
    expected = L.rotor_angle(ord(from_letter) - 65)
    if abs(((a0 - expected + math.pi) % (2 * math.pi)) - math.pi) > 1e-6:
        raise ValueError(f"rotor {slot} is not showing {from_letter}: rig and simulator disagree")
    # the interpolation stored on a key governs the segment that starts there
    U.key(r, "rotation_euler", _f(t0, fps), a0, index=0,
          interp="LINEAR" if ease == "LINEAR" else "BEZIER", ease="AUTO" if ease == "LINEAR" else ease)
    U.key(r, "rotation_euler", _f(t0 + dur, fps), a0 - steps * L.STEP, index=0, interp="BEZIER", ease=ease if ease != "LINEAR" else "AUTO")
    r["angle"] = a0 - steps * L.STEP


def animate_pawls(rig, steps: list, t: float, fps: int, slow: float = 1.0, linger: float = 0.0):
    """All three pawls move forward on every key press. A pawl that can drop (pawl 1
    always; pawls 2 and 3 only into a notch) falls in, catches a tooth and pushes
    it one step; the others slide along on their ring and push nothing.
    `slow` stretches the motion for close-ups (1 = real speed); `linger` keeps the
    pawls at the end of their push for that many extra seconds (to explain it)."""
    engaged = {s["pawl"] for s in steps}
    drop = L.NOTCH_RING_R - (L.RATCHET_ROOT_R + 0.0003)
    t_in, t_push0, t_push1 = t + 0.5 * STEP_START * slow, t + STEP_START * slow, t + STEP_END * slow
    t_out, t_back = t + (STEP_END + 0.05) * slow + linger, t + 0.45 * slow + linger
    for pawl, pivot in rig.pawls.items():
        body = rig.parts[f"ENIGMA_pawl_{pawl}_body"]
        rest = body.get("rest")
        if rest is None:
            rest = tuple(body.location)
            body["rest"] = rest
        U.key(pivot, "rotation_euler", _f(t_push0, fps), 0.0, index=0,
              interp="LINEAR" if slow > 1 else "BEZIER")          # moves with the rotor it pushes
        U.key(pivot, "rotation_euler", _f(t_push1, fps), -L.STEP, index=0)
        U.key(pivot, "rotation_euler", _f(t_out, fps), -L.STEP, index=0)
        U.key(pivot, "rotation_euler", _f(t_back, fps), 0.0, index=0)
        d = drop if pawl in engaged else 0.0
        inward = tuple(-v / L.NOTCH_RING_R * d for v in _radial_of(rest))
        dropped = tuple(r + i for r, i in zip(rest, inward))
        for tt, loc in ((t, rest), (t_in, dropped), (t_push1, dropped), (t_out, rest)):
            for i in (1, 2):
                U.key(body, "location", _f(tt, fps), loc[i], index=i)
    lever = rig.parts["ENIGMA_stepping_lever"]
    U.key(lever, "rotation_euler", _f(t, fps), 0.0, index=0)
    U.key(lever, "rotation_euler", _f(t + KEY_DOWN * slow, fps), math.radians(6), index=0)
    U.key(lever, "rotation_euler", _f(t + 0.6 * slow, fps), 0.0, index=0)


def _radial_of(loc):
    """Unit-length-times-R radial vector of a body rest position (it is R * radial)."""
    return (0.0, loc[1], loc[2])


def step_press(rig, press: dict, t: float, fps: int, slow: float = 1.0, linger: float = 0.0):
    """The mechanical half of a key press: pawls move, rotors that the stream says
    step turn one position, all while the key goes down (before the current)."""
    before = dict(zip(("left", "middle", "right"), press["positions_before"]))
    moved = {s["rotor"] for s in press["steps"]}
    animate_pawls(rig, press["steps"], t, fps, slow=slow, linger=linger)
    for slot in ("left", "middle", "right"):
        if slot in moved:
            rotate_rotor(rig, slot, before[slot], t + STEP_START * slow, (STEP_END - STEP_START) * slow, fps,
                         ease="LINEAR" if slow > 1 else "EASE_OUT")


# ------------------------------------------------------------------ current
def show_signal_path(rig, press: dict, t0: float, dur: float, fps: int, t_off: float | None = None,
                     pins: dict | None = None):
    """Draw the current for one key press: a glowing trace that grows from key to
    lamp over `dur` seconds, following layout.signal_schedule()."""
    fwd, back = L.signal_points(press)
    col = rig.cols["signal"]
    tag = f"{press['index']:03d}"
    objs = []
    for part, pts, mat in (("fwd", fwd, rig.mats["signal"]), ("ret", back, rig.mats["signal_return"])):
        trace = U.poly_curve(f"ENIGMA_signal_{tag}_{part}", col, pts, bevel=0.0016, material=mat,
                             parent=rig.root)
        trace.color = (1, 1, 1, 1)
        objs.append(trace)
    # Grow each half along the shared schedule (slow in the rotors, fast on plain wires).
    sched = L.signal_schedule(press, t0, dur, pins)
    for ob, half in zip(objs, ("fwd", "ret")):
        cu = ob.data
        U.key(cu, "bevel_factor_end", _f(0, fps), 0.0, interp="CONSTANT")
        for a in sched:
            if a["half"] == half:
                U.key(cu, "bevel_factor_end", _f(a["t"], fps), a["f"], interp="LINEAR")
        if t_off is not None:
            U.key(ob, "color", _f(t_off - 0.2, fps), (1, 1, 1, 1))
            U.key(ob, "color", _f(t_off, fps), (0, 0, 0, 1))
    return objs


def set_plugboard(rig, spec: str):
    from enigma_model.build import set_plugboard as _sp
    _sp(rig, spec)


# ------------------------------------------------------------------ single rotor (Act IV)
def rotor_tree(rig, slot):
    """The rotor's parent empty and everything under it."""
    r = rig.rotors[slot]
    return [r, *r.children_recursive]


def isolate(rig, keep: list, t: float, fps: int):
    """Hide every ENIGMA object except `keep` (and their descendants) from time t."""
    keep_set = set()
    for ob in keep:
        keep_set.add(ob.name)
        keep_set.update(c.name for c in ob.children_recursive)
    hide = [o for c in rig.cols.values() for o in c.objects
            if o.name not in keep_set and o.type != "EMPTY" and not o.hide_render]
    set_visible(hide, False, t, fps)


def lift_rotor(rig, slot: str, to, t0: float, dur: float, fps: int):
    """Carry a rotor off the axle to world position `to` (it keeps its orientation)."""
    r = rig.rotors[slot]
    U.key(r, "location", _f(t0, fps), tuple(r.location))
    U.key(r, "location", _f(t0 + dur, fps), tuple(to), ease="EASE_IN_OUT")
    r.location = to


def place_rotor(rig, slot: str, to, t: float, fps: int):
    r = rig.rotors[slot]
    U.key(r, "location", _f(t, fps), tuple(to), interp="CONSTANT")


def explode_rotor(rig, slot: str, t0: float, dur: float, fps: int, gap=0.028, back_at: float | None = None):
    """Slide a rotor's parts apart along its axle (index ring, tyre, core, thumbwheel, ratchet)."""
    # left: index ring (with the notch) and alphabet tyre; right: thumbwheel and ratchet.
    # They go well clear of the core so both contact faces can be seen.
    offsets = {"notchring": -2.8, "notch": -2.8, "ring": -1.6, "ringletter": -1.6, "thumbwheel": 1.5, "ratchet": 2.7}
    for ob in rig.rotors[slot].children:
        part = ob.name.replace(f"ENIGMA_rotor_{slot}_", "").split("_")[0]
        k = offsets.get(part)
        if k is None:
            continue
        x0 = ob.location.x
        U.key(ob, "location", _f(t0, fps), x0, index=0)
        U.key(ob, "location", _f(t0 + dur, fps), x0 + k * gap, index=0, ease="EASE_IN_OUT")
        if back_at is not None:
            U.key(ob, "location", _f(back_at, fps), x0 + k * gap, index=0)
            U.key(ob, "location", _f(back_at + dur, fps), x0, index=0, ease="EASE_IN_OUT")


def glass_core(rig, slot: str):
    """Rotor body (and ring) as smoked glass, so the wires inside can be seen."""
    for part in ("body", "ring"):
        ob = bpy.data.objects.get(f"ENIGMA_rotor_{slot}_{part}")
        if ob:
            ob.data.materials.clear()
            ob.data.materials.append(rig.mats["core_glass"])


def glow(obj, t_on: float, fps: int, t_off: float | None = None, level=1.0):
    U.key(obj, "color", _f(max(0.0, t_on - 1 / fps), fps), tuple(obj.color), interp="CONSTANT")
    U.key(obj, "color", _f(t_on, fps), (level, level, level, 1), interp="CONSTANT")
    obj.color = (level, level, level, 1)
    if t_off is not None:
        U.key(obj, "color", _f(t_off, fps), (0, 0, 0, 1), interp="CONSTANT")
        obj.color = (0, 0, 0, 1)


def glow_label(obj, t_on: float, fps: int, t_off: float | None = None):
    """A letter that is only visible (and lit) while its contact carries current."""
    if not obj.get("_hidden_from_start"):
        set_visible([obj], False, 0.0, fps)      # else Blender holds the first "visible" key backwards
        obj["_hidden_from_start"] = True
    set_visible([obj], True, t_on, fps)
    glow(obj, t_on, fps, t_off)
    if t_off is not None:
        set_visible([obj], False, t_off, fps)


def glow_wire(rig, slot: str, pin: str, t_on: float, fps: int, t_off: float | None = None):
    glow(rig.parts[f"wires_{slot}"][pin], t_on, fps, t_off)


def glass_reflector(rig):
    ob = rig.parts["ENIGMA_reflector"]
    ob.data.materials.clear()
    ob.data.materials.append(rig.mats["core_glass"])


def reflector_pair(rig, a: str, b: str):
    """The glowing wire object joining contacts a and b (either order)."""
    wires = rig.parts["reflector_wires"]
    return wires.get(a + b) or wires[b + a]


def return_rotor(rig, slot: str, lifted_at, t0: float, dur: float, fps: int, showing: str, set_to: str):
    """Put a lifted rotor back on the axle, then spin it forward (the operator's thumb
    on the thumbwheel) from the letter it shows to the letter it must show."""
    home = (L.AXIS_X[slot], L.ROTOR_AXIS_Y, L.ROTOR_AXIS_Z)
    r = rig.rotors[slot]
    a = L.rotor_angle(ord(showing) - 65)
    r["angle"] = a
    U.key(r, "rotation_euler", _f(0.0, fps), a, index=0, interp="CONSTANT")
    U.key(r, "location", _f(0.0, fps), tuple(lifted_at), interp="CONSTANT")
    U.key(r, "location", _f(t0, fps), tuple(lifted_at))
    U.key(r, "location", _f(t0 + dur, fps), home, ease="EASE_IN_OUT")
    steps = (ord(set_to) - ord(showing)) % 26
    if steps:
        rotate_rotor(rig, slot, showing, t0 + dur + 0.3, 0.9, fps, steps=steps)
