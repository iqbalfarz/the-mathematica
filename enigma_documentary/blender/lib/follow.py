"""A camera that follows the head of the current (shared by s0302, s0501, s0503)."""
from __future__ import annotations

from . import layout as L
from . import staging as S

OFFSET = (0.05, -0.15, 0.23)       # steeply down on the current, over the keys


def follow_current(ctx, press, t_from: float, t_to: float, name="CAM_follow", step=0.6, offset=OFFSET,
                   lens=35, fstop=6.3):
    t0, dur, pins = ctx.sc["signal_start"], ctx.sc["signal_dur"], ctx.sc["signal_pins"]
    cam, tgt = S.camera(name, lens=lens, fstop=fstop)
    t = max(t_from, 0.0)
    while t <= t_to + 1e-6:
        h = L.head_position(press, t0, dur, t, pins)
        S.move(cam, tgt, t, ctx.fps, loc=tuple(a + o for a, o in zip(h, offset)), look=h)
        t += step
    return cam, tgt


def caption_stages(ctx, press, stages=None):
    """Captions naming the part the current is in, for stops inside this scene."""
    t0, dur, pins = ctx.sc["signal_start"], ctx.sc["signal_dur"], ctx.sc["signal_pins"]
    for stop in L.signal_timeline(press, t0, dur, pins):
        if not 0 <= stop["t"] <= ctx.duration or (stages and stop["stage"] not in stages):
            continue
        text = stop["part"].upper() if stop["in"] == stop["out"] else f"{stop['part'].upper()}   {stop['in']} → {stop['out']}"
        ctx.labels.caption(stop["t"], text)
