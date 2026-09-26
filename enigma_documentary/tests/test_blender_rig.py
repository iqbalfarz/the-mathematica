"""Rig vs simulator: if the animation disagrees with enigma_core, STOP.

Needs the `bpy` module (pip install bpy==4.2.0, Python 3.11) — skipped otherwise.
Builds the rig from an event stream, plays it, then checks at the moment the
current flows for every press: each rotor's angle matches positions_after and
exactly the simulator's lamp is lit.
"""
import math
import sys

import pytest

from enigma_core import EnigmaMachine
from enigma_core.configuration import load_configs
from enigma_core.events import stream

from conftest import ROOT

bpy = pytest.importorskip("bpy")
sys.path.insert(0, str(ROOT / "blender"))

from enigma_model.build import build_enigma  # noqa: E402
from lib import api, player  # noqa: E402
from lib import layout as L  # noqa: E402
from lib import util as U  # noqa: E402

FPS = 24


def _rig_for(name, text, spacing=1.0):
    U.reset_scene()
    cfg = load_configs(ROOT / "config" / "machines.yaml")[name]
    presses = EnigmaMachine(cfg).press_keys(text)
    s = stream(cfg.to_dict(), presses)
    rig = build_enigma(s["config"])
    times = [0.5 + i * spacing for i in range(len(presses))]
    player.play(rig, s, times, FPS, show_signal=True, signal_dur=0.4, hold=0.6)
    return rig, s, times


@pytest.mark.parametrize("name,text", [("hero_opening", "LLLL"), ("double_step_demo", "AAAA"),
                                       ("barbarossa_1941", "ZZZZZZZZZZZZZZZZZZZZZZZZZZZZ")])
def test_rotor_angles_and_lamps_follow_the_simulator(name, text):
    rig, s, times = _rig_for(name, text)
    scene = bpy.context.scene
    for press, t in zip(s["presses"], times):
        f = U.sec(t + api.CURRENT_ON + 0.4 + 0.05, FPS)     # current on and lamp lit
        scene.frame_set(int(math.floor(f)), subframe=f - math.floor(f))
        for slot, letter in zip(("left", "middle", "right"), press["positions_after"]):
            got = rig.rotors[slot].rotation_euler.x
            want = L.rotor_angle(ord(letter) - 65)
            d = (got - want + math.pi) % (2 * math.pi) - math.pi
            assert abs(d) < 1e-4, f"{slot} rotor shows wrong letter at press {press['index']}"
        lit = [c for c, parts in rig.lamps.items() if parts[0].color[0] > 0.5]
        assert lit == [press["lamp"]], f"press {press['index']}: lit {lit}, simulator says {press['lamp']}"


def test_rotor_never_unwinds_backwards():
    rig, s, times = _rig_for("barbarossa_1941", "Z" * 30, spacing=0.8)
    scene = bpy.context.scene
    prev = None
    for f in range(1, int(U.sec(times[-1] + 1, FPS))):
        scene.frame_set(f)
        a = rig.rotors["right"].rotation_euler.x
        if prev is not None:
            assert a <= prev + 1e-6          # right rotor angle only ever decreases (turns forward)
        prev = a


def test_signal_curve_runs_from_key_to_simulated_lamp():
    rig, s, times = _rig_for("hero_opening", "A")
    press = s["presses"][0]
    curves = [o for o in bpy.data.objects if o.name.startswith("ENIGMA_signal_")]
    assert len(curves) == 2
    fwd = next(o for o in curves if o.name.endswith("_fwd")).data.splines[0].points
    ret = next(o for o in curves if o.name.endswith("_ret")).data.splines[0].points
    kx, ky, _ = L.key_pos(press["key"])
    lx, ly, _ = L.lamp_pos(press["lamp"])
    assert abs(fwd[0].co.x - kx) < 1e-6 and abs(fwd[0].co.y - ky) < 1e-6
    assert abs(ret[-1].co.x - lx) < 1e-6 and abs(ret[-1].co.y - ly) < 1e-6


def test_tracked_labels_project_into_the_frame():
    from lib import staging as S
    from lib.labels import Labels

    rig, s, times = _rig_for("hero_opening", "")
    scene = bpy.context.scene
    cam, tgt = S.camera("CAM_test", lens=40)
    S.move(cam, tgt, 0.0, FPS, loc=(0.3, -0.5, 0.4), look=(0.0, -0.02, 0.1))
    S.cut(scene, cam, 0.0, FPS)

    class Ctx:
        fps = FPS
    ctx = Ctx()
    ctx.scene = scene
    lab = Labels(ctx)
    lab.track("KEYBOARD", "ENIGMA_keycap_G", 0.0, 0.5)
    lab.track("BEHIND", (0.3, -2.0, 0.4), 0.0, 0.5)       # behind the camera
    data = lab.compute()
    kb, behind = data["labels"]
    assert all(p is not None and 0 <= p[0] <= 1 and 0 <= p[1] <= 1 for p in kb["track"])
    assert all(p is None for p in behind["track"])
