"""s0503 "The way back": the same press, back through the rotors to the lamp."""
from lib import api, player
from lib import layout as L
from lib import staging as S
from lib.follow import caption_stages, follow_current


def build(ctx):
    fps, scene, rig = ctx.fps, ctx.scene, ctx.rig
    b = {k: ctx.beat(k) for k in ("b1", "b2", "b3", "b4", "b5")}
    api.hide_casing(rig, 0.0, fps)
    api.show_wiring(rig, 0.0, fps)
    press = player.play_shot(ctx)[0]
    lamp_t = ctx.sc["signal_start"] + ctx.sc["signal_dur"]

    follow, _ = follow_current(ctx, press, 0.0, lamp_t)
    lamp, lamp_tgt = S.camera("CAM_lamp", lens=50, fstop=4.0)
    S.move(lamp, lamp_tgt, 0.0, fps, loc=(0.0, -0.33, 0.44), look=(0.0, -0.012, L.LAMP_Z))
    pull, pull_t = S.camera("CAM_pullback", lens=35, fstop=6.3)
    S.move(pull, pull_t, b["b5"], fps, loc=(0.05, -0.30, 0.30), look=(0.0, 0.0, 0.09))
    S.move(pull, pull_t, ctx.duration, fps, loc=(0.32, -0.56, 0.46), look=(0.0, 0.0, 0.09))

    S.cut(scene, follow, 0.0, fps)
    S.cut(scene, lamp, lamp_t - 0.5, fps)
    S.cut(scene, pull, b["b5"], fps)
    caption_stages(ctx, press)
