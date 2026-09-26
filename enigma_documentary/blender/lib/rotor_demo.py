"""Shared set-up for the single-rotor scenes (Act IV)."""
from __future__ import annotations

from enigma_model.build import demo_stators, rotor_wire_objects

from . import api

LIFT = (0.0, -0.02, 0.30)      # where the lifted rotor floats, well above the machine


def lifted(ctx, slot: str, stators=False, wires=False, glass=False):
    """Rotor already out of the machine at t=0, everything else hidden."""
    rig, fps = ctx.rig, ctx.fps
    api.set_rotor_positions(rig, ctx.stream["config"]["positions"], 0.0, fps)
    api.place_rotor(rig, slot, LIFT, 0.0, fps)
    api.isolate(rig, [rig.rotors[slot]], 0.0, fps)
    out = {}
    if wires:
        out["wires"] = rotor_wire_objects(rig, slot)
        api.set_visible(list(out["wires"].values()), True, 0.0, fps)
    if stators:
        st = demo_stators(rig, slot)
        st["anchor"].location = LIFT
        # contacts and rings visible; letters appear only while their contact is lit
        labels = set(st["in_label"].values()) | set(st["out_label"].values())
        api.set_visible([o for o in st["anchor"].children_recursive if o not in labels], True, 0.0, fps)
        out["stators"] = st
    if glass:
        api.glass_core(rig, slot)
    return out


def rel(offset):
    return tuple(a + b for a, b in zip(LIFT, offset))
