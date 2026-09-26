"""s0602 "The notch": the right rotor shows V, so the notch in its index ring is under
pawl 2. Slow press: pawl 2 drops in and pushes the middle rotor's teeth while pawl 1
steps the right rotor as always (ADV -> AEW). All motion from the event stream.

Side view along the axle at pawl 2, with the right rotor cut away except its ring."""
from lib import player
from lib import staging as S
from lib import stepping_view as V


def build(ctx):
    fps, scene = ctx.fps, ctx.scene
    b = {k: ctx.beat(k) for k in ("b1", "b2", "b3", "b4", "b5")}
    V.isolate_stack(ctx, 0.0)
    player.play_shot(ctx)
    t_press = ctx.sc["press_times"][0]
    t_wide = b["b5"] + 3.5

    side, side_t = S.camera("CAM_side2", lens=60, fstop=11.0)
    S.move(side, side_t, 0.0, fps, loc=V.side_view(2, 0.17, mix=0.40), look=V.tip(2, out=-0.004))
    S.move(side, side_t, b["b2"] + 1.0, fps, loc=V.side_view(2, 0.13, mix=0.40), look=V.tip(2, out=-0.004))
    S.move(side, side_t, t_wide, fps, loc=V.side_view(2, 0.12, mix=0.35), look=V.tip(2, out=-0.004))
    wide, wide_t = S.camera("CAM_stack", lens=45, fstop=8.0)
    S.move(wide, wide_t, t_wide, fps, loc=V.view(V.gap_x(2), 0.22, side=0.40), look=V.tip(2, dx=0.01))
    S.move(wide, wide_t, ctx.duration, fps, loc=V.view(V.gap_x(2), 0.20, side=0.40), look=V.tip(2, dx=0.01))
    S.cut(scene, side, 0.0, fps)
    S.cut(scene, wide, t_wide, fps)
    V.cut_away(ctx, 2, 0.0, show_again=t_wide)

    lab = ctx.labels
    lab.track("NOTCH", "ENIGMA_rotor_right_notch", b["b2"] + 1.0, t_press + 0.2)
    lab.track("PAWL 2", "ENIGMA_pawl_2", b["b2"] + 2.0, t_press + 0.2)
    lab.track("MIDDLE ROTOR'S TEETH", _teeth("middle"), t_press + 3.2, b["b4"] + 8.0)
    ctx.labels.caption(t_press, f"SLOW MOTION ×{ctx.sc['slow']:g}", until=t_press + 0.45 * ctx.sc["slow"] + ctx.sc["linger"])


def _teeth(slot):
    from lib import layout as L
    x = L.AXIS_X[slot] + L.ROTOR_W / 2
    return L.ring_point(x, L.PAWL_ANGLE - 2.0 * L.STEP, L.RATCHET_TIP_R)
