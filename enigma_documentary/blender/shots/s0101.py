"""s0101 Cold open — "Same key, different answer".

Two macro cameras: one on key L, one on the lampboard. Every press cuts from the
key to the lamp on the click. The machine state comes from build/events/s0101_keys.json
(presses of L on the hero_opening setting); lamps are whatever the simulator says.
The rotors turn on every press but stay hidden under the closed lid (sound only).
"""
from lib import api, player
from lib import layout as L
from lib import staging as S

def build(ctx):
    fps, scene, rig = ctx.fps, ctx.scene, ctx.rig
    times = ctx.sc["press_times"]          # from config/shots.yaml press_at, resolved by the timeline
    holds = ctx.sc["press_holds"]
    player.play_shot(ctx)

    kx, ky, kz = L.key_pos("L")
    key_cam, key_tgt = S.camera("CAM_key_macro", lens=100, fstop=2.2)
    lamp_cam, lamp_tgt = S.camera("CAM_lampboard", lens=50, fstop=4.0)
    wide_cam, wide_tgt = S.camera("CAM_pullback", lens=65, fstop=3.5)

    # Key: very close, slightly from the operator's side, slow push-in through the whole shot.
    S.move(key_cam, key_tgt, 0.0, fps, loc=(kx + 0.05, ky - 0.13, kz + 0.07), look=(kx, ky, kz))
    S.move(key_cam, key_tgt, ctx.duration, fps, loc=(kx + 0.035, ky - 0.095, kz + 0.05), look=(kx, ky, kz))
    # Lamps: frame the WHOLE lampboard (all 26 lamps), so the viewer sees a
    # different lamp light up in a different place each time.
    S.move(lamp_cam, lamp_tgt, 0.0, fps, loc=(0.0, -0.33, 0.44), look=(0.0, -0.012, L.LAMP_Z))
    S.move(lamp_cam, lamp_tgt, ctx.duration, fps, loc=(0.0, -0.30, 0.41), look=(0.0, -0.012, L.LAMP_Z))
    # Pull back: from the key into darkness (beat b5).
    t5 = ctx.beat("b5")
    S.move(wide_cam, wide_tgt, t5, fps, loc=(kx + 0.035, ky - 0.095, kz + 0.05), look=(kx, ky, kz))
    S.move(wide_cam, wide_tgt, ctx.duration, fps, loc=(kx + 0.25, ky - 0.55, kz + 0.35), look=(kx, ky, kz))

    S.cut(scene, key_cam, 0.0, fps)
    for i, t in enumerate(times):
        S.cut(scene, lamp_cam, t + api.KEY_DOWN, fps)
        nxt = times[i + 1] if i + 1 < len(times) else t5
        S.cut(scene, key_cam, min(nxt - 0.3, t + holds[i] + 0.25), fps)
    S.cut(scene, wide_cam, t5, fps)
    # Dim the room during the cold open: only the key and lamps are lit.
    ctx.lights["LIGHT_fill"].data.energy *= 0.3
    ctx.lights["LIGHT_top"].data.energy *= 0.4
