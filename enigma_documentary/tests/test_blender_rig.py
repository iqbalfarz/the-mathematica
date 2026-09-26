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


def test_rotor_demo_wires_and_lit_exit_follow_the_simulator():
    """Per-wire objects match the wiring table, and at each s0403-style step the pin
    under fixed contact A is the one the simulator names."""
    from enigma_core.cli import rotor_demo
    from enigma_model.build import rotor_wire_objects
    from lib import api

    U.reset_scene()
    cfg = load_configs(ROOT / "config" / "machines.yaml")["hero_opening"]
    rig = build_enigma(stream(cfg.to_dict(), [])["config"])
    wires = rotor_wire_objects(rig, "left")               # left rotor = rotor I, ring A
    w = L.ROTOR_W
    for pin, ob in wires.items():
        pts = ob.data.splines[0].points
        j, o = ord(pin) - 65, ord(ob["plate"]) - 65
        a, b = j * L.STEP, o * L.STEP
        assert abs(pts[0].co.x - w / 2) < 1e-6 and abs(pts[0].co.z - L.CONTACT_R * math.cos(a)) < 1e-6
        assert abs(pts[-1].co.x + w / 2) < 1e-6 and abs(pts[-1].co.z - L.CONTACT_R * math.cos(b)) < 1e-6

    api.set_rotor_positions(rig, "AAA", 0.0, FPS)
    steps = rotor_demo({"rotor": "I", "ring": "A", "positions": "ABCD", "key": "A"})
    scene = bpy.context.scene
    t = 1.0
    for prev, step in zip(steps, steps[1:]):
        api.rotate_rotor(rig, "left", prev["position"], t, 0.2, FPS)
        t += 1.0
    for i, step in enumerate(steps):
        scene.frame_set(int(U.sec(0.5 + i * 1.0, FPS)))
        core = rig.cores["left"]
        pin_ob = bpy.data.objects[f"ENIGMA_rotor_left_pin_{ord(step['in_pin']) - 65:02d}"]
        world = core.matrix_world @ pin_ob.location
        want = L.ring_point(0, 0.0, L.CONTACT_R)            # fixed contact A = angle 0
        assert abs(world.y - want[1]) < 1e-5 and abs(world.z - want[2]) < 1e-5, step


def test_reflector_wires_are_the_simulated_pairs():
    from enigma_core.reflector import Reflector
    from enigma_model.build import reflector_wire_objects
    U.reset_scene()
    cfg = load_configs(ROOT / "config" / "machines.yaml")["hero_opening"]
    rig = build_enigma(stream(cfg.to_dict(), [])["config"])
    wires = reflector_wire_objects(rig)
    want = {chr(65 + a) + chr(65 + b) for a, b in Reflector.from_name("B").pairs()}
    assert set(wires) == want and len(wires) == 13
    for pair, ob in wires.items():
        pts = ob.data.splines[0].points
        a, b = (ord(c) - 65 for c in pair)
        assert abs(pts[0].co.z - L.CONTACT_R * math.cos(a * L.STEP)) < 1e-6
        assert abs(pts[-1].co.z - L.CONTACT_R * math.cos(b * L.STEP)) < 1e-6


def test_replay_holds_the_key_and_keeps_the_stepped_rotors():
    from lib import player
    U.reset_scene()
    cfg = load_configs(ROOT / "config" / "machines.yaml")["hero_opening"]
    presses = EnigmaMachine(cfg).press_keys("W")
    s = stream(cfg.to_dict(), presses)
    rig = build_enigma(s["config"])

    class Ctx:
        pass
    ctx = Ctx()
    ctx.rig, ctx.fps, ctx.stream, ctx.duration = rig, FPS, s, 5.0
    ctx.shot = {"replay": "x", "signal": {"show": True}}
    ctx.sc = {"signal_start": -30.0, "signal_dur": 32.0, "signal_pins": {"reflector": -2.0, "turn": -1.0}}
    z0 = rig.keys["W"].location.z
    player.play_shot(ctx)
    scene = bpy.context.scene
    lamp_frame = int(U.sec(2.5, FPS))
    scene.frame_set(lamp_frame)
    assert abs(rig.keys["W"].location.z - (z0 - L.KEY_TRAVEL)) < 1e-6          # key still held down
    for slot, letter in zip(("left", "middle", "right"), presses[0].positions_after):
        d = (rig.rotors[slot].rotation_euler.x - L.rotor_angle(ord(letter) - 65) + math.pi) % (2 * math.pi) - math.pi
        assert abs(d) < 1e-6
    lit = [c for c, parts in rig.lamps.items() if parts[0].color[0] > 0.5]
    assert lit == [presses[0].lamp]                                            # lamp at the end of the current


def _wrap(a):
    return (a + math.pi) % (2 * math.pi) - math.pi


@pytest.mark.parametrize("rotor", ["I", "II", "III", "IV", "V"])
def test_notch_is_under_the_pawl_exactly_at_the_notch_letter(rotor):
    """The cut in the index ring must reach the pawl at the same window letter at
    which enigma_core says the rotor turns its neighbour over."""
    from enigma_core.rotor import Rotor
    U.reset_scene()
    cfg = load_configs(ROOT / "config" / "machines.yaml")["double_step_demo"].to_dict()
    cfg["rotors"] = [rotor, "II", "III"]
    rig = build_enigma(cfg)
    notch = bpy.data.objects["ENIGMA_rotor_left_notch"]
    for p in range(26):
        r = Rotor.from_name(rotor, ring=0, position=p)
        under = abs(_wrap(notch["angle"] + L.rotor_angle(p) - L.PAWL_ANGLE)) < L.NOTCH_HALF - L.PAWL_TIP_HALF
        assert under == r.at_notch(), (rotor, chr(65 + p))


def test_pawls_drop_only_into_real_notches_through_the_double_step():
    """Play ADU -> ADV -> AEW -> BFX and check, press by press, that a pawl drops in
    exactly when the ring beside it has its notch under the pawl tip, and that this
    is exactly the set of pawls the simulator says engaged."""
    rig, s, times = _rig_for("double_step_demo", "AAAA")
    notches = {slot: bpy.data.objects[f"ENIGMA_rotor_{slot}_notch"]["angle"] for slot in ("left", "middle", "right")}
    for press, t in zip(s["presses"], times):
        before = dict(zip(("left", "middle", "right"), press["positions_before"]))
        want = {st["pawl"] for st in press["steps"]}
        free = {1}
        for pawl, (_, ring_slot) in L.PAWL_GAP.items():
            if ring_slot == "entry":
                continue
            a = notches[ring_slot] + L.rotor_angle(ord(before[ring_slot]) - 65)
            if abs(_wrap(a - L.PAWL_ANGLE)) < L.NOTCH_HALF - L.PAWL_TIP_HALF:
                free.add(pawl)
        assert free == want, (press["positions_before"], free, want)
        f = U.sec(t + 0.9 * api.STEP_END, FPS)          # mid-push (between frames at real speed)
        for pawl in (1, 2, 3):
            body = rig.parts[f"ENIGMA_pawl_{pawl}_body"]
            fc = {c.array_index: c for c in U._fcurves(body) if c.data_path == "location"}
            r = math.hypot(fc[1].evaluate(f), fc[2].evaluate(f))
            assert (r < L.RATCHET_TIP_R) == (pawl in want), (pawl, r)
    assert [p["positions_after"] for p in s["presses"]] == ["ADV", "AEW", "BFX", "BFY"]


def test_hiding_later_keeps_the_object_visible_until_then():
    """Blender holds a first key backwards: an object hidden at t must still render before t."""
    U.reset_scene()
    cfg = load_configs(ROOT / "config" / "machines.yaml")["hero_opening"]
    rig = build_enigma(stream(cfg.to_dict(), [])["config"])
    lid = bpy.data.objects["ENIGMA_front_panel"]
    api.isolate(rig, [rig.rotors["left"]], 2.0, FPS)
    scene = bpy.context.scene
    scene.frame_set(int(U.sec(1.0, FPS)))
    assert not lid.hide_render
    scene.frame_set(int(U.sec(3.0, FPS)))
    assert lid.hide_render
