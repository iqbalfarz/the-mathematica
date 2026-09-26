"""s0402 "Twenty-six wires": glass core; wires light one by one, pairs from the stream."""
from lib import api
from lib import staging as S
from lib.rotor_demo import LIFT, lifted, rel


def build(ctx):
    fps, scene, rig = ctx.fps, ctx.scene, ctx.rig
    spec = ctx.stream["rotor_demo_spec"]
    slot = spec["slot"]
    b = {k: ctx.beat(k) for k in ("b1", "b2", "b3", "b4", "b5")}
    parts = lifted(ctx, slot, wires=True, glass=True)
    pairs = {w["pin"]: w["plate"] for w in spec["wires"]}

    first = list(spec.get("reveal", ""))
    times = [b["b2"] + 2.4, b["b3"] + 0.2, b["b3"] + 1.6]
    for pin, t in zip(first, times):
        api.glow_wire(rig, slot, pin, t, fps)
        ctx.labels.caption(t, f"PIN {pin} → PLATE {pairs[pin]}")
    rest = [p for p in sorted(pairs) if p not in first]
    t = b["b4"] + 0.4
    for pin in rest:
        api.glow_wire(rig, slot, pin, t, fps)
        t += 0.11
    ctx.labels.caption(b["b4"] + 0.4, "26 PINS · 26 WIRES · 26 PLATES")

    cam, tgt = S.camera("CAM_core", lens=50, fstop=8.0)
    S.move(cam, tgt, 0.0, fps, loc=rel((0.15, -0.26, 0.07)), look=rel((0.012, 0, 0)))
    S.move(cam, tgt, b["b4"], fps, loc=rel((0.13, -0.25, 0.06)), look=rel((0.012, 0, 0)))
    S.move(cam, tgt, b["b5"], fps, loc=rel((0.10, -0.26, 0.07)), look=rel((0.008, 0, 0)))
    S.move(cam, tgt, ctx.duration, fps, loc=rel((0.14, -0.20, 0.14)), look=LIFT)   # orbit up and over, on the pin side
    S.cut(scene, cam, 0.0, fps)
    return parts
