"""s0601 "Three pawls": the lid comes off and the camera goes under the rotors to the
three pawls. One key press in slow motion: every pawl moves, only pawl 1 catches
teeth, and the right rotor steps (ADU -> ADV). Which pawls catch and which rotors
move come from the event stream (player.play_shot -> api.step_press).

Side views look along the axle with the parts to the right cut away, so the
ratchet's teeth and the ring the next pawl rides on read like a diagram."""
from lib import layout as L
from lib import player
from lib import staging as S
from lib import stepping_view as V


def build(ctx):
    fps, scene = ctx.fps, ctx.scene
    b = {k: ctx.beat(k) for k in ("b1", "b2", "b3", "b4", "b5", "b6")}
    t_iso = b["b1"] + 2.2
    machine = V.wide_start(ctx, t_iso)
    player.play_shot(ctx)
    t_press = ctx.sc["press_times"][0]

    under, under_t = S.camera("CAM_under", lens=45, fstop=8.0)       # all three pawls from below
    S.move(under, under_t, t_iso, fps, loc=V.view(V.gap_x(2), 0.30, side=0.30), look=V.tip(2))
    S.move(under, under_t, b["b2"] + 1.0, fps, loc=V.view(V.gap_x(2), 0.24, side=0.30), look=V.tip(2))
    S.move(under, under_t, ctx.duration, fps, loc=V.view(V.gap_x(2), 0.20, side=0.40), look=V.tip(2))

    side1, side1_t = S.camera("CAM_side1", lens=60, fstop=11.0)       # along the axle at pawl 1
    S.move(side1, side1_t, 0.0, fps, loc=V.side_view(1, 0.15, mix=0.45), look=V.tip(1, out=-0.004))
    S.move(side1, side1_t, ctx.duration, fps, loc=V.side_view(1, 0.13, mix=0.40), look=V.tip(1, out=-0.004))
    side2, side2_t = S.camera("CAM_side2", lens=60, fstop=11.0)       # along the axle at pawl 2
    S.move(side2, side2_t, 0.0, fps, loc=V.side_view(2, 0.14, mix=0.40), look=V.tip(2, out=-0.004))
    S.move(side2, side2_t, ctx.duration, fps, loc=V.side_view(2, 0.13, mix=0.40), look=V.tip(2, out=-0.004))

    t_ratchet, t_three = b["b2"] + 1.0, b["b2"] + 7.2
    S.cut(scene, machine, 0.0, fps)
    S.cut(scene, under, t_iso, fps)
    S.cut(scene, side1, t_ratchet, fps)
    S.cut(scene, under, t_three, fps)
    S.cut(scene, side1, b["b3"], fps)
    S.cut(scene, side2, b["b5"], fps)
    S.cut(scene, under, b["b6"], fps)
    V.cut_away(ctx, 1, t_ratchet, show_again=t_three)
    V.cut_away(ctx, 1, b["b3"], show_again=b["b5"])
    V.cut_away(ctx, 2, b["b5"], show_again=b["b6"])

    lab = ctx.labels
    lab.track("RATCHET · 26 TEETH", _on_ratchet("right"), t_ratchet + 0.6, t_three - 0.2)
    for n in (1, 2, 3):
        lab.track(f"PAWL {n}", f"ENIGMA_pawl_{n}", t_three + 0.5 + 0.35 * (3 - n), b["b3"] - 0.1)
    lab.track("PAWL 1", "ENIGMA_pawl_1", b["b3"] + 0.3, t_press + 0.6)
    lab.track("RING HOLDS PAWL 2 UP", "ENIGMA_pawl_2", b["b5"] + 0.8, b["b5"] + 6.0)
    ctx.labels.caption(t_press, f"SLOW MOTION ×{ctx.sc['slow']:g}", until=t_press + 0.45 * ctx.sc["slow"])


def _on_ratchet(slot: str) -> tuple:
    """A world point on a rotor's ratchet teeth, a little ahead of its pawl."""
    x = L.AXIS_X[slot] + L.ROTOR_W / 2
    return L.ring_point(x, L.PAWL_ANGLE - 2.5 * L.STEP, L.RATCHET_TIP_R)
