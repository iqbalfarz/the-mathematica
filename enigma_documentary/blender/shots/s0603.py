"""s0603 "The double step": the middle rotor shows E, so its own notch is under pawl 3.
Slow press: pawl 3 drops into that notch and pushes the left rotor's teeth and, by
the notch wall, the middle rotor too (AEW -> BFX). Motion from the event stream; the
rig test checks the notch geometry against enigma_core.

Side view along the axle at pawl 3 (the middle rotor cut away except its ring), then
the whole middle rotor comes back to show it turned as well."""
from lib import layout as L
from lib import player
from lib import staging as S
from lib import stepping_view as V


def build(ctx):
    fps, scene = ctx.fps, ctx.scene
    b = {k: ctx.beat(k) for k in ("b1", "b2", "b3", "b4", "b5", "b6")}
    V.isolate_stack(ctx, 0.0)
    player.play_shot(ctx)
    t_press = ctx.sc["press_times"][0]
    t_whole = b["b4"] + 3.0          # "the notch belongs to the middle rotor": show all of it

    wide, wide_t = S.camera("CAM_stack", lens=45, fstop=8.0)
    S.move(wide, wide_t, 0.0, fps, loc=V.view(V.gap_x(2), 0.22, side=0.35), look=V.tip(2))
    S.move(wide, wide_t, b["b1"] + 3.0, fps, loc=V.view(V.gap_x(3), 0.20, side=0.35), look=V.tip(3, dx=0.01))
    side, side_t = S.camera("CAM_side3", lens=60, fstop=11.0)
    S.move(side, side_t, 0.0, fps, loc=V.side_view(3, 0.15, mix=0.40), look=V.tip(3, out=-0.004))
    S.move(side, side_t, t_whole, fps, loc=V.side_view(3, 0.12, mix=0.35), look=V.tip(3, out=-0.004))
    both, both_t = S.camera("CAM_both", lens=50, fstop=8.0)
    S.move(both, both_t, t_whole, fps, loc=V.view(V.gap_x(3), 0.19, side=0.40), look=V.tip(3, dx=0.012))
    S.move(both, both_t, b["b5"] + 4.0, fps, loc=V.view(V.gap_x(2), 0.18, side=0.40), look=V.tip(2, dx=-0.008))
    S.move(both, both_t, ctx.duration, fps, loc=V.view(V.gap_x(2), 0.26, side=0.40, up=0.2), look=V.tip(2, out=-0.02))
    t_side = b["b1"] + 4.5
    S.cut(scene, wide, 0.0, fps)
    S.cut(scene, side, t_side, fps)
    S.cut(scene, both, t_whole, fps)
    V.cut_away(ctx, 3, t_side, show_again=t_whole)

    lab = ctx.labels
    lab.track("MIDDLE ROTOR'S NOTCH", "ENIGMA_rotor_middle_notch", t_side + 0.6, t_press + 0.2)
    lab.track("PAWL 3", "ENIGMA_pawl_3", t_side + 1.4, t_press + 0.2)
    lab.track("LEFT ROTOR'S TEETH", _teeth("left"), b["b3"] + 0.8, t_whole - 0.1)
    lab.track("MIDDLE ROTOR, DRAGGED BY ITS NOTCH", "ENIGMA_rotor_middle_notch", t_whole + 0.8, b["b4"] + 9.5)
    ctx.labels.caption(t_press, f"SLOW MOTION ×{ctx.sc['slow']:g}", until=t_press + 0.45 * ctx.sc["slow"] + ctx.sc["linger"])


def _teeth(slot):
    x = L.AXIS_X[slot] + L.ROTOR_W / 2
    return L.ring_point(x, L.PAWL_ANGLE - 2.0 * L.STEP, L.RATCHET_TIP_R)
