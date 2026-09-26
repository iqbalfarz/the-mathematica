"""Shared set-up for the stepping close-ups (Act VI): the rotor stack and the three
pawls alone, seen from below at the front, where the pawls meet the rotors."""
from __future__ import annotations

import math

from . import api
from . import layout as L
from . import staging as S

RADIAL = (0.0, -math.sin(L.PAWL_ANGLE), math.cos(L.PAWL_ANGLE))     # outward, at the pawls


def gap_x(pawl: int) -> float:
    a_slot, b_slot = L.PAWL_GAP[pawl]
    a_face = L.AXIS_X[a_slot] + L.ROTOR_W / 2
    b_face = L.AXIS_X[b_slot] - (L.ROTOR_W / 2 if b_slot != "entry" else L.ROTOR_W * 0.4)
    return (a_face + b_face) / 2


def tip(pawl: int, out: float = 0.0, dx: float = 0.0) -> tuple:
    """World point on the rim where `pawl` rests, `out` metres further out."""
    r = L.NOTCH_RING_R + out
    return (gap_x(pawl) + dx, L.ROTOR_AXIS_Y + r * RADIAL[1], L.ROTOR_AXIS_Z + r * RADIAL[2])


def view(pawl_or_x, dist: float, side: float = 0.35, up: float = 0.0) -> tuple:
    """Camera position looking in at a pawl from outside the rim: `side` swings it
    towards the operator's right (+x) so the rotor faces show."""
    x = gap_x(pawl_or_x) if isinstance(pawl_or_x, int) else pawl_or_x
    t = (x, *tip(1)[1:])
    n = math.sqrt(1 + side * side + up * up)
    return (t[0] + dist * side / n, t[1] + dist * RADIAL[1] / n, t[2] + dist * (RADIAL[2] + up) / n)


def isolate_stack(ctx, t: float):
    """From time t: only the rotors, entry wheel, reflector, axle and pawls."""
    rig = ctx.rig
    keep = [rig.rotors[s] for s in ("left", "middle", "right")]
    keep += [rig.parts[n] for n in ("ENIGMA_entry_wheel", "ENIGMA_axle", "ENIGMA_reflector")]
    keep += list(rig.pawls.values())
    api.isolate(rig, keep, t, ctx.fps)


def wide_start(ctx, t_iso: float):
    """The opening of each Act VI scene: the open machine, then the cutaway."""
    rig, fps = ctx.rig, ctx.fps
    api.open_lid(rig, 0.0, 0.01, fps)
    cam, tgt = S.camera("CAM_machine", lens=40, fstop=5.6)
    S.move(cam, tgt, 0.0, fps, loc=(0.22, -0.34, 0.38), look=(0.0, 0.05, 0.12))
    S.move(cam, tgt, t_iso, fps, loc=(0.18, -0.24, 0.26), look=(0.0, L.ROTOR_AXIS_Y, L.ROTOR_AXIS_Z))
    isolate_stack(ctx, t_iso)
    return cam


ORDER = ("left", "middle", "right", "entry")


def side_view(pawl: int, dist: float, mix: float = 0.35, lift: float = 0.0, dx: float = 0.0) -> tuple:
    """Camera looking along the axle from the operator's right at `pawl`, tipped
    `mix` towards the outside of the rim so the teeth and the ring edge both show."""
    t = tip(pawl, out=lift)
    d = (1.0, mix * RADIAL[1], mix * RADIAL[2])
    n = math.sqrt(sum(c * c for c in d))
    return (t[0] + dx + dist * d[0] / n, t[1] + dist * d[1] / n, t[2] + dist * d[2] / n)


def cut_away(ctx, pawl: int, t: float, show_again: float | None = None):
    """Hide everything to the right of `pawl` (for a side view of it), except the
    notched index ring of the rotor it rests on: that ring is what the pawl rides."""
    rig, fps = ctx.rig, ctx.fps
    ring_slot = L.PAWL_GAP[pawl][1]
    gone = []
    for slot in ORDER[ORDER.index(ring_slot):]:
        if slot == "entry":
            ob = rig.parts["ENIGMA_entry_wheel"]
            gone += [ob] + [c for c in ob.children_recursive if c.type != "EMPTY"]
            continue
        for c in rig.rotors[slot].children_recursive:
            if c.type == "EMPTY" or (slot == ring_slot and c.name.endswith("_notchring")):
                continue
            gone.append(c)
    for n, pivot in rig.pawls.items():
        if n < pawl:
            gone += [c for c in pivot.children_recursive if c.type != "EMPTY"]
    for o in gone:          # a first key would otherwise hold "hidden" backwards to frame 1
        if o.animation_data is None or o.animation_data.action is None:
            api.set_visible([o], True, 0.0, fps)
    api.set_visible(gone, False, t, fps)
    if show_again is not None:
        api.set_visible(gone, True, show_again, fps)
    return gone
