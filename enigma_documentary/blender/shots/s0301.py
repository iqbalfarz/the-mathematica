"""s0301 "Inside the box": a guided tour of the parts, with tracked labels.

The lid is already open (s0102 ended by opening it). Each beat moves the camera
to the part being named; Remotion draws the labels at positions projected from
the named 3D objects (lib/labels.py), so they stay crisp and on target.
"""
from lib import api
from lib import layout as L
from lib import staging as S

TOP = L.ROTOR_AXIS_Z + L.ROTOR_R + 0.006


def build(ctx):
    fps, scene, rig = ctx.fps, ctx.scene, ctx.rig
    api.set_rotor_positions(rig, ctx.stream["config"]["positions"], 0.0, fps)
    api.open_lid(rig, 0.0, 0.01, fps)

    cam, tgt = S.camera("CAM_tour", lens=45, fstop=4.5)
    b = {k: ctx.beat(k) for k in ("b1", "b2", "b3", "b4", "b5", "b6")}
    shots = [  # (time, camera location, look-at)
        (0.0, (0.30, -0.52, 0.42), (0.0, -0.02, 0.10)),
        (b["b2"] - 0.3, (0.24, -0.47, 0.39), (0.0, -0.02, 0.10)),
        (b["b2"] + 1.5, (0.02, -0.34, 0.36), (0.0, -0.06, 0.12)),
        (b["b3"] - 0.2, (0.00, -0.31, 0.33), (0.0, -0.05, 0.12)),
        (b["b3"] + 1.4, (0.06, -0.44, 0.10), (0.0, -0.15, 0.06)),
        (b["b4"] - 0.2, (0.05, -0.42, 0.11), (0.0, -0.15, 0.06)),
        (b["b4"] + 1.6, (0.03, -0.12, 0.36), (0.0, L.ROTOR_AXIS_Y, 0.12)),
        (b["b5"] - 0.2, (0.02, -0.10, 0.35), (0.0, L.ROTOR_AXIS_Y, 0.12)),
        # Both ends of the stack in view: entry wheel on the right, reflector on the left.
        (b["b5"] + 1.8, (0.06, -0.17, 0.33), (0.0, L.ROTOR_AXIS_Y, 0.12)),
        (b["b6"] - 0.2, (0.05, -0.16, 0.32), (0.0, L.ROTOR_AXIS_Y, 0.12)),
        (ctx.duration, (0.32, -0.55, 0.45), (0.0, -0.01, 0.10)),
    ]
    for t, loc, look in shots:
        S.move(cam, tgt, t, fps, loc=loc, look=look)
    S.cut(scene, cam, 0.0, fps)

    lab = ctx.labels
    end = b["b6"] + 1.5
    lab.track("KEYBOARD", "ENIGMA_keycap_G", b["b2"] + 0.4, b["b3"] - 0.2, offset=(0, 0, 0.012))
    lab.track("LAMPBOARD", "ENIGMA_lampwindow_G", b["b2"] + 2.2, b["b3"] - 0.2, offset=(0, 0, 0.006))
    lab.track("PLUGBOARD", "ENIGMA_socket_G", b["b3"] + 1.8, b["b4"] - 0.2, offset=(0, -0.003, 0.012))
    for slot in ("left", "middle", "right"):
        lab.track(slot.upper(), (L.AXIS_X[slot], L.ROTOR_AXIS_Y, TOP), b["b4"] + 2.0, b["b5"] - 0.2)
    lab.track("ENTRY WHEEL", (L.AXIS_X["entry"], L.ROTOR_AXIS_Y, TOP - 0.004), b["b5"] + 1.6, end)
    lab.track("REFLECTOR", (L.AXIS_X["reflector"], L.ROTOR_AXIS_Y, TOP - 0.004), b["b5"] + 4.4, end)
