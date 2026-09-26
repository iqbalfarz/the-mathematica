"""s0401 "One wheel": lift the left rotor (rotor I) out, explode it, name its parts."""
from lib import api
from lib import layout as L
from lib import staging as S
from lib.rotor_demo import LIFT, rel


def build(ctx):
    fps, scene, rig = ctx.fps, ctx.scene, ctx.rig
    slot = ctx.shot["rotor_demo"]["slot"]
    b = {k: ctx.beat(k) for k in ("b1", "b2", "b3", "b4", "b5", "b6")}
    api.set_rotor_positions(rig, ctx.stream["config"]["positions"], 0.0, fps)
    api.open_lid(rig, 0.0, 0.01, fps)

    # b1: lift the rotor out of the well; once it is clear, the machine goes dark.
    api.lift_rotor(rig, slot, LIFT, b["b1"] + 0.2, 1.8, fps)
    api.isolate(rig, [rig.rotors[slot]], b["b1"] + 2.3, fps)
    # b3: explode along the axle; b6: back together.
    api.explode_rotor(rig, slot, b["b3"] + 0.3, 1.2, fps, back_at=b["b6"] + 2.0)

    cam, tgt = S.camera("CAM_rotor", lens=50, fstop=6.3)
    axis = (L.AXIS_X[slot], L.ROTOR_AXIS_Y, L.ROTOR_AXIS_Z)
    shots = [
        (0.0, (0.03, -0.12, 0.30), axis),
        (b["b1"] + 0.2, (0.03, -0.12, 0.30), axis),
        (b["b1"] + 2.2, rel((0.08, -0.42, 0.08)), LIFT),
        (b["b2"] + 2.0, rel((0.04, -0.40, 0.07)), LIFT),
        (b["b3"] + 1.6, rel((0.00, -0.44, 0.09)), LIFT),
        (b["b4"] + 0.2, rel((0.00, -0.44, 0.09)), LIFT),
        (b["b4"] + 2.2, rel((0.28, -0.26, 0.08)), rel((0.02, 0, 0))),     # pin face
        (b["b4"] + 4.6, rel((-0.28, -0.26, 0.08)), rel((-0.02, 0, 0))),   # plate face
        (b["b5"] + 0.4, rel((-0.06, -0.36, 0.13)), rel((-0.012, 0, 0.012))),  # ring + notch
        (b["b6"] + 0.3, rel((0.20, -0.32, 0.07)), rel((0.035, 0, 0))),    # ratchet
        (ctx.duration, rel((0.02, -0.42, 0.08)), LIFT),
    ]
    for t, loc, look in shots:
        S.move(cam, tgt, t, fps, loc=loc, look=look)
    S.cut(scene, cam, 0.0, fps)

    lab = ctx.labels
    lab.track("26 SPRING PINS", f"ENIGMA_rotor_{slot}_pin_00", b["b4"] + 1.4, b["b4"] + 4.0, offset=(0, 0, 0.004))
    lab.track("26 FLAT PLATES", f"ENIGMA_rotor_{slot}_plate_00", b["b4"] + 4.4, b["b5"] - 0.2, offset=(0, 0, 0.004))
    lab.track("ALPHABET RING", f"ENIGMA_rotor_{slot}_ringletter_A", b["b5"] + 0.6, b["b6"] - 0.2, offset=(0, 0, 0.006))
    lab.track("NOTCH", f"ENIGMA_rotor_{slot}_notch", b["b5"] + 2.4, b["b6"] - 0.2, offset=(0, 0, 0.004))
    lab.track("RATCHET", f"ENIGMA_rotor_{slot}_ratchet", b["b6"] + 0.6, b["b6"] + 2.0, offset=(0, 0, 0.036))
