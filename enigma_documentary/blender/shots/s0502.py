"""s0502 "The mirror": the reflector's 13 wires, pairs from the simulator; the
current (still held from s0501) crosses its own pair and turns round."""
from enigma_model.build import reflector_wire_objects
from lib import api, player
from lib import layout as L
from lib import staging as S


def build(ctx):
    fps, scene, rig = ctx.fps, ctx.scene, ctx.rig
    b = {k: ctx.beat(k) for k in ("b1", "b2", "b3", "b4", "b5")}
    api.hide_casing(rig, 0.0, fps)
    api.show_wiring(rig, 0.0, fps)
    api.glass_reflector(rig)
    press = player.play_shot(ctx)[0]

    wires = reflector_wire_objects(rig)
    api.set_visible(list(wires.values()), True, b["b2"] + 0.8, fps)
    pairs = ctx.stream["reflector_pairs"]
    hop = next(h for h in press["path"] if h["stage"] == "reflector")
    via = api.reflector_pair(rig, hop["in_letter"], hop["out_letter"])

    shown = pairs[:3]
    for i, pair in enumerate(shown):
        t = b["b3"] + 0.1 + i * 1.0
        api.glow(wires[pair], t, fps, t_off=b["b3"] + 3.6)
        ctx.labels.caption(t, f"{pair[0]} ↔ {pair[1]}")
    for w in wires.values():                               # all thirteen, briefly
        if w not in [wires[p] for p in shown]:
            api.glow(w, b["b3"] + 3.1, fps, t_off=b["b4"])
    api.glow(via, b["b4"] + 0.2, fps, t_off=b["b5"])
    ctx.labels.caption(b["b4"] + 0.2, f"IN {hop['in_letter']} → OUT {hop['out_letter']}")
    for w in wires.values():
        api.glow(w, b["b5"] + 1.8, fps)
    ctx.labels.caption(b["b5"] + 1.8, "13 WIRES · NO CONTACT JOINED TO ITSELF")

    x = L.AXIS_X["reflector"]
    # High and to the left: looking down over the keys into the glass reflector.
    c = (x + 0.004, L.ROTOR_AXIS_Y, L.ROTOR_AXIS_Z)
    cam, tgt = S.camera("CAM_reflector", lens=55, fstop=6.3)
    S.move(cam, tgt, 0.0, fps, loc=(x - 0.12, -0.10, 0.33), look=c)
    S.move(cam, tgt, b["b3"], fps, loc=(x - 0.13, -0.06, 0.29), look=c)
    S.move(cam, tgt, b["b5"], fps, loc=(x - 0.14, -0.05, 0.28), look=c)
    S.move(cam, tgt, ctx.duration, fps, loc=(x - 0.10, -0.12, 0.34), look=c)
    S.cut(scene, cam, 0.0, fps)
