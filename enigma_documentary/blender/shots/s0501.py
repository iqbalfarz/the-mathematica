"""s0501 "Three in a row": rotor I goes back in and is turned to A; press W; the
current runs right to left through the three rotors and stops at the reflector
(the reflector pins in config/shots.yaml hold it there until s0502)."""
from lib import api, player
from lib import layout as L
from lib import staging as S
from lib.follow import caption_stages, follow_current
from lib.rotor_demo import LIFT


def build(ctx):
    fps, scene, rig = ctx.fps, ctx.scene, ctx.rig
    b = {k: ctx.beat(k) for k in ("b1", "b2", "b3", "b4", "b5")}
    api.hide_casing(rig, 0.0, fps)
    api.show_wiring(rig, 0.0, fps)
    player.play_shot(ctx)
    press = ctx.stream["presses"][0]

    # The rotor comes back showing the letter Act IV left it at, then is turned to
    # the letter the machine state says (both from event streams, never typed).
    returned = ctx.load_stream(ctx.shot["return_from"])
    demo, slot = returned["rotor_demo"], returned["rotor_demo_spec"]["slot"]
    want = ctx.stream["config"]["positions"][("left", "middle", "right").index(slot)]
    api.return_rotor(rig, slot, LIFT, b["b1"] + 0.3, 1.4, fps, showing=demo[-1]["position"], set_to=want)

    wide, wide_t = S.camera("CAM_wide", lens=40, fstop=5.6)
    S.move(wide, wide_t, 0.0, fps, loc=(0.24, -0.42, 0.44), look=(0.0, 0.03, 0.18))
    S.move(wide, wide_t, b["b2"], fps, loc=(0.20, -0.30, 0.34), look=(0.0, L.ROTOR_AXIS_Y, 0.12))
    S.move(wide, wide_t, b["b3"] - 0.3, fps, loc=(0.10, -0.12, 0.22), look=(-0.006, L.ROTOR_AXIS_Y, L.ROTOR_AXIS_Z))
    kx, ky, kz = L.key_pos(press["key"])
    key_cam, key_t = S.camera("CAM_key", lens=60, fstop=4.0)
    S.move(key_cam, key_t, 0.0, fps, loc=(kx + 0.08, ky - 0.20, kz + 0.14), look=(kx, ky, kz))

    t_ref = ctx.sc["signal_pins"]["reflector"]
    follow, _ = follow_current(ctx, press, ctx.sc["signal_start"], t_ref)
    hold, hold_t = S.camera("CAM_hold", lens=45, fstop=6.3)
    S.move(hold, hold_t, 0.0, fps, loc=(-0.02, -0.16, 0.30), look=(L.AXIS_X["reflector"], L.ROTOR_AXIS_Y, 0.12))

    S.cut(scene, wide, 0.0, fps)
    S.cut(scene, key_cam, b["b3"] - 0.2, fps)
    S.cut(scene, follow, ctx.sc["signal_start"] + 0.5, fps)
    S.cut(scene, hold, min(t_ref + 0.3, ctx.duration - 0.5), fps)
    # the reflector crossing is revealed in s0502, not here
    caption_stages(ctx, press, stages={"rotor_right_in", "rotor_middle_in", "rotor_left_in"})
