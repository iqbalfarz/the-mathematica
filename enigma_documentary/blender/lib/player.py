"""Plays an enigma_core event stream on the rig.

This is the only place key presses become motion, and it takes every fact
(which rotors step, where the current goes, which lamp lights) from the stream.
"""
from __future__ import annotations

from . import api


def play(rig, stream: dict, press_times: list[float], fps: int, show_signal=False, signal_dur=1.6,
         hold=0.55, signal_pins: dict | None = None):
    """Animate every press in `stream` at `press_times` (seconds).

    For shots, prefer play_shot(ctx), which reads press times, holds and the
    signal settings from config/shots.yaml via the timeline."""
    # `hold` is seconds the key stays down (lamp lit): one number or one per press.
    presses = stream["presses"]
    if len(press_times) != len(presses):
        raise ValueError(f"{len(presses)} presses in stream but {len(press_times)} times given")
    api.set_rotor_positions(rig, stream["config"]["positions"], 0.0, fps)
    holds = hold if isinstance(hold, (list, tuple)) else [hold] * len(presses)
    for press, t, h in zip(presses, press_times, holds):
        before = dict(zip(("left", "middle", "right"), press["positions_before"]))
        moved = {s["rotor"] for s in press["steps"]}
        api.animate_pawls(rig, press["steps"], t, fps)
        for slot in ("left", "middle", "right"):
            if slot in moved:
                api.rotate_rotor(rig, slot, before[slot], t + api.STEP_START, api.STEP_END - api.STEP_START, fps)
        on = t + api.CURRENT_ON
        key_hold = max(h, (signal_dur + 0.4) if show_signal else h)
        api.animate_key(rig, press["key"], t, fps, hold=key_hold)
        lamp_on = on + (signal_dur if show_signal else 0.0)
        api.animate_lamp(rig, press["lamp"], lamp_on, t + key_hold + 0.05, fps)
        if show_signal:
            api.show_signal_path(rig, press, on, signal_dur, fps, t_off=t + key_hold + 0.3,
                                 pins=signal_pins if press["index"] == 0 else None)
    return presses


def play_shot(ctx, show_signal=None):
    """Play the shot's own event stream with timing from build/timeline.json."""
    sig = ctx.shot.get("signal") or {}
    return play(ctx.rig, ctx.stream, ctx.sc["press_times"], ctx.fps,
                show_signal=sig.get("show", False) if show_signal is None else show_signal,
                signal_dur=ctx.sc.get("signal_dur", 1.6), hold=ctx.sc["press_holds"],
                signal_pins=ctx.sc.get("signal_pins"))
