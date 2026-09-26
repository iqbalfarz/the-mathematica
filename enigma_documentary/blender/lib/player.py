"""Plays an enigma_core event stream on the rig.

This is the only place key presses become motion, and it takes every fact
(which rotors step, where the current goes, which lamp lights) from the stream.
"""
from __future__ import annotations

from . import api


def play(rig, stream: dict, press_times: list[float], fps: int, show_signal=False, signal_dur=1.6,
         hold=0.55, signal_pins: dict | None = None, lamps=True, slow: float = 1.0, linger: float = 0.0):
    """Animate every press in `stream` at `press_times` (seconds).

    For shots, prefer play_shot(ctx), which reads press times, holds and the
    signal settings from config/shots.yaml via the timeline."""
    # `hold` is seconds the key stays down (lamp lit): one number or one per press.
    # `slow` stretches the mechanical part of each press (pawls, stepping) for close-ups.
    presses = stream["presses"]
    if len(press_times) != len(presses):
        raise ValueError(f"{len(presses)} presses in stream but {len(press_times)} times given")
    api.set_rotor_positions(rig, stream["config"]["positions"], 0.0, fps)
    holds = hold if isinstance(hold, (list, tuple)) else [hold] * len(presses)
    for press, t, h in zip(presses, press_times, holds):
        api.step_press(rig, press, t, fps, slow=slow, linger=linger)
        on = t + api.CURRENT_ON * slow          # the contact closes only after the rotors have stepped
        key_hold = max(h, (signal_dur + 0.4) if show_signal else h)
        api.animate_key(rig, press["key"], t, fps, hold=key_hold)
        lamp_on = on + (signal_dur if show_signal else 0.0)
        if lamps:     # play_shot() lights the lamp itself when it draws the current
            api.animate_lamp(rig, press["lamp"], lamp_on, t + key_hold + 0.05, fps)
        if show_signal:
            api.show_signal_path(rig, press, on, signal_dur, fps, t_off=t + key_hold + 0.3,
                                 pins=signal_pins if press["index"] == 0 else None)
    return presses


def play_shot(ctx, show_signal=None):
    """Play the shot's own event stream with timing from build/timeline.json.

    A `replay` shot continues a press made in an earlier scene: the rotors are
    already stepped, the key is still held down and the current carries on
    along the same schedule (pins outside the scene say where it already is).
    """
    sig = ctx.shot.get("signal") or {}
    show = sig.get("show", False) if show_signal is None else show_signal
    if ctx.shot.get("replay"):
        return replay(ctx, show)
    presses = play(ctx.rig, ctx.stream, ctx.sc["press_times"], ctx.fps, show_signal=False,
                   hold=ctx.sc["press_holds"], lamps=not show, slow=ctx.sc.get("slow", 1.0),
                   linger=ctx.sc.get("linger", 0.0))
    if show and presses:
        _signal_and_lamp(ctx, presses[0], ctx.sc["press_times"][0] + ctx.sc["press_holds"][0])
    return presses


def replay(ctx, show=True):
    rig, fps, press = ctx.rig, ctx.fps, ctx.stream["presses"][0]
    api.set_rotor_positions(rig, press["positions_after"], 0.0, fps)
    stem = rig.keys[press["key"]]
    api.U.key(stem, "location", 1, stem.location.z - api.L.KEY_TRAVEL, index=2, interp="CONSTANT")
    if show:
        _signal_and_lamp(ctx, press, 1e6)
    return [press]


def _signal_and_lamp(ctx, press, key_up):
    rig, fps = ctx.rig, ctx.fps
    t0, dur, pins = ctx.sc["signal_start"], ctx.sc["signal_dur"], ctx.sc["signal_pins"]
    api.show_signal_path(rig, press, t0, dur, fps, pins=pins,
                         t_off=None if key_up > ctx.duration else key_up + 0.3)
    lamp_t = t0 + dur
    if lamp_t < ctx.duration:
        api.animate_lamp(rig, press["lamp"], max(lamp_t, 0.0), min(key_up + 0.05, ctx.duration + 5), fps)
