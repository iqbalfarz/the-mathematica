"""s0302 "A key is a switch": one key press, the current traced from key to lamp.

The casing is cut away and the rotor bodies turn to smoked glass. The camera
follows the head of the current, whose timing (layout.signal_schedule, pinned
to the narration in config/shots.yaml) is shared with the captions, so the
caption names the part the glow is in. The lamp that lights is the simulator's.
"""
from lib import api, player
from lib import layout as L
from lib import staging as S
from lib.follow import caption_stages, follow_current

def build(ctx):
    fps, scene, rig = ctx.fps, ctx.scene, ctx.rig
    b = {k: ctx.beat(k) for k in ("b1", "b2", "b3", "b4", "b5", "b6", "b7")}
    cut_t = b["b1"] + 1.2
    api.hide_casing(rig, cut_t, fps)
    api.show_wiring(rig, 0.0, fps)
    player.play_shot(ctx)

    press = ctx.stream["presses"][0]
    t_on = ctx.sc["signal_start"]
    dur, pins = ctx.sc["signal_dur"], ctx.sc["signal_pins"]

    wide, wide_t = S.camera("CAM_cutaway", lens=40, fstop=5.6)
    S.move(wide, wide_t, 0.0, fps, loc=(0.34, -0.50, 0.40), look=(0.0, -0.02, 0.09))
    S.move(wide, wide_t, cut_t, fps, loc=(0.30, -0.46, 0.36), look=(0.0, -0.02, 0.09))
    kx, ky, kz = L.key_pos(press["key"])
    S.move(wide, wide_t, b["b2"], fps, loc=(kx + 0.12, ky - 0.25, kz + 0.16), look=(kx, ky, kz))

    follow, _ = follow_current(ctx, press, t_on, t_on + dur)

    lamp, lamp_t = S.camera("CAM_lamp", lens=50, fstop=4.0)
    S.move(lamp, lamp_t, 0.0, fps, loc=(0.0, -0.33, 0.44), look=(0.0, -0.012, L.LAMP_Z))
    pull, pull_t = S.camera("CAM_pullback", lens=35, fstop=6.3)
    S.move(pull, pull_t, b["b7"], fps, loc=(0.05, -0.30, 0.30), look=(0.0, 0.0, 0.09))
    S.move(pull, pull_t, ctx.duration, fps, loc=(0.30, -0.55, 0.45), look=(0.0, 0.0, 0.09))

    S.cut(scene, wide, 0.0, fps)
    S.cut(scene, follow, t_on + 0.4, fps)
    S.cut(scene, lamp, pins.get("lamp", t_on + dur) - 0.5, fps)
    S.cut(scene, pull, b["b7"], fps)

    caption_stages(ctx, press)
