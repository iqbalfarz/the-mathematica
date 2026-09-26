"""Plays an enigma_core event stream on the rig.

This is the only place key presses become motion, and it takes every fact
(which rotors step, where the current goes, which lamp lights) from the stream.
"""
from __future__ import annotations

from . import api


def play(rig, stream: dict, press_times: list[float], fps: int, show_signal=False, signal_dur=1.6,
         hold=0.55):
    presses = stream["presses"]
    if len(press_times) != len(presses):
        raise ValueError(f"{len(presses)} presses in stream but {len(press_times)} times given")
    api.set_rotor_positions(rig, stream["config"]["positions"], 0.0, fps)
    for press, t in zip(presses, press_times):
        before = dict(zip(("left", "middle", "right"), press["positions_before"]))
        moved = {s["rotor"] for s in press["steps"]}
        api.animate_pawls(rig, press["steps"], t, fps)
        for slot in ("left", "middle", "right"):
            if slot in moved:
                api.rotate_rotor(rig, slot, before[slot], t + api.STEP_START, api.STEP_END - api.STEP_START, fps)
        on = t + api.CURRENT_ON
        key_hold = max(hold, (signal_dur + 0.4) if show_signal else hold)
        api.animate_key(rig, press["key"], t, fps, hold=key_hold)
        lamp_on = on + (signal_dur if show_signal else 0.0)
        api.animate_lamp(rig, press["lamp"], lamp_on, t + key_hold + 0.05, fps)
        if show_signal:
            api.show_signal_path(rig, press, on, signal_dur, fps, t_off=t + key_hold + 0.3)
    return presses
