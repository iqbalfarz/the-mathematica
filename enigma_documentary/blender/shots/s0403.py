"""s0403 "Turn it once": current always enters at fixed contact A; the rotor turns
one step at a time. Which pin meets contact A, which wire lights and which exit
contact glows all come from the rotor_demo stream (enigma_core)."""
from lib import api
from lib import staging as S
from lib.rotor_demo import LIFT, lifted, rel


def build(ctx):
    fps, scene, rig = ctx.fps, ctx.scene, ctx.rig
    spec = ctx.stream["rotor_demo_spec"]
    steps = ctx.stream["rotor_demo"]
    slot = spec["slot"]
    b = {k: ctx.beat(k) for k in ("b1", "b2", "b3", "b4", "b5", "b6")}
    parts = lifted(ctx, slot, wires=True, stators=True, glass=True)
    st = parts["stators"]

    api.glow(st["in"][spec["key"]], b["b1"] + 1.0, fps)                  # contact A, lit throughout
    api.glow_label(st["in_label"][spec["key"]], b["b1"] + 1.0, fps)
    # (time the current is shown, time the rotor turns to this step)
    show = [b["b2"] + 1.4, b["b4"] + 0.6, b["b5"] + 0.4, b["b5"] + 1.7]
    turn = [None, b["b3"] + 0.4, b["b5"] + 0.1, b["b5"] + 1.4]
    for i, step in enumerate(steps):
        if turn[i] is not None:
            api.rotate_rotor(rig, slot, steps[i - 1]["position"], turn[i], 0.16, fps)
        off = (turn[i + 1] if i + 1 < len(steps) else b["b6"] + 2.5) - 0.02
        api.glow_wire(rig, slot, step["in_pin"], show[i], fps, t_off=off)
        api.glow(st["out"][step["out"]], show[i] + 0.3, fps, t_off=off)
        api.glow_label(st["out_label"][step["out"]], show[i] + 0.3, fps, t_off=off)
        ctx.labels.caption(show[i], f"POSITION {step['position']} · IN {step['in']} → "
                                    f"PIN {step['in_pin']} → PLATE {step['out_pin']} → OUT {step['out']}")
    ctx.labels.caption(b["b6"] + 0.2, "   ".join(f"{s['in']}→{s['out']}" for s in steps))

    cam, tgt = S.camera("CAM_turn", lens=50, fstop=8.0)
    S.move(cam, tgt, 0.0, fps, loc=rel((0.12, -0.30, 0.07)), look=LIFT)
    S.move(cam, tgt, b["b6"], fps, loc=rel((0.10, -0.30, 0.07)), look=LIFT)
    S.move(cam, tgt, ctx.duration, fps, loc=rel((0.02, -0.36, 0.09)), look=LIFT)
    S.cut(scene, cam, 0.0, fps)
