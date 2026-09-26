"""s0102 "Open the machine" — full reveal, rack focus, then the lid opens.

The rotor windows show the state after the four presses of s0101 (AFT), taken
from the event stream, not typed by hand.
"""
from lib import api
from lib import layout as L
from lib import staging as S


def build(ctx):
    fps, scene, rig = ctx.fps, ctx.scene, ctx.rig
    # The stream already starts where s0101 left the rotors (shots.yaml `continues`).
    api.set_rotor_positions(rig, ctx.stream["config"]["positions"], 0.0, fps)

    cam, tgt = S.camera("CAM_reveal", lens=50, fstop=5.6)
    b1, b2, b3, b4 = (ctx.beat(b) for b in ("b1", "b2", "b3", "b4"))
    # b1: slow 30-degree orbit around the machine.
    for i, p in enumerate(S.orbit_points((0, -0.01, 0.10), 0.62, 0.30, -35, -5, n=4)):
        S.move(cam, tgt, b1 + (b2 - b1) * i / 3, fps, loc=p, look=(0, -0.02, 0.10))
    # b2: settle in front, rack focus keyboard -> lampboard (move the focus target).
    front = (0.0, -0.52, 0.36)
    S.move(cam, tgt, b2, fps, loc=front, look=(0, -0.10, L.KEY_Z))
    S.move(cam, tgt, b2 + 1.6, fps, look=(0, -0.10, L.KEY_Z))
    S.move(cam, tgt, b2 + 3.0, fps, look=(0, -0.012, L.LAMP_Z))
    # b3: hold wide for the title card (overlay in Remotion).
    S.move(cam, tgt, b3, fps, loc=(0.0, -0.58, 0.40), look=(0, -0.01, 0.10))
    # b4: the lid swings open, camera dives toward the rotors.
    api.open_lid(rig, b4 + 0.4, 1.1, fps)
    S.move(cam, tgt, b4 + 0.6, fps, loc=(0.0, -0.58, 0.40), look=(0, -0.01, 0.10))
    S.move(cam, tgt, ctx.duration, fps, loc=(0.02, -0.10, 0.30), look=(0, L.ROTOR_AXIS_Y, L.ROTOR_AXIS_Z + 0.03))
    S.cut(scene, cam, 0.0, fps)
