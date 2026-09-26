"""The Blender rig's geometry must agree with the simulator (pure Python, no bpy)."""
import math
import sys

from enigma_core import EnigmaMachine
from enigma_core.configuration import load_configs

from conftest import ROOT

sys.path.insert(0, str(ROOT / "blender"))
from lib import layout as L  # noqa: E402

CONFIGS = load_configs(ROOT / "config" / "machines.yaml")


def _close(a, b):
    return all(abs(x - y) < 1e-9 for x, y in zip(a, b))


def test_fixed_contact_meets_the_core_pin_the_simulator_says():
    m = EnigmaMachine(CONFIGS["barbarossa_1941"])
    rings = dict(zip(("left", "middle", "right"), m.config.rings))
    for p in m.press_keys("WETTERVORHERSAGE"):
        pos = dict(zip(("left", "middle", "right"), (ord(c) - 65 for c in p.positions_after)))
        for h in p.path:
            if not h.stage.startswith("rotor_"):
                continue
            part = h.stage.split("_")[1]
            in_fixed = ord(h.in_letter) - 65
            pin = (ord(h.in_pin) - 65 - rings[part]) % 26          # pin index in core frame
            ang = L.pin_world_angle(pin, pos[part], rings[part])
            diff = (ang - in_fixed * L.STEP) % (2 * math.pi)
            assert min(diff, 2 * math.pi - diff) < 1e-9


def test_window_shows_position_letter():
    # Letter k on the ring sits at local angle k*STEP; rotated by rotor_angle(p) it is at the top iff k == p.
    for p in range(26):
        assert math.isclose((p * L.STEP + L.rotor_angle(p)) % (2 * math.pi), 0, abs_tol=1e-9)


def test_signal_path_starts_at_key_and_ends_at_lamp():
    m = EnigmaMachine(CONFIGS["barbarossa_1941"])
    for p in m.press_keys("ABC"):
        fwd, back = L.signal_points(p.to_dict())
        kx, ky, _ = L.key_pos(p.key)
        lx, ly, _ = L.lamp_pos(p.lamp)
        assert _close(fwd[0][:2], (kx, ky)) and _close(back[-1][:2], (lx, ly))
        assert _close(fwd[-1], back[0])       # forward and return meet inside the reflector


def test_every_letter_has_a_key_lamp_and_socket():
    for c in L.ALPHA:
        L.key_pos(c), L.lamp_pos(c), L.socket_pos(c)
    assert sorted("".join(L.ROWS)) == list(L.ALPHA)


def test_signal_schedule_respects_pins_and_order():
    press = EnigmaMachine(CONFIGS["hero_opening"]).press_key("A").to_dict()
    pins = {"reflector": 5.0, "lamp": 9.0}
    sched = L.signal_schedule(press, 1.0, 8.0, pins)
    times = [a["t"] for a in sched]
    assert times == sorted(times) and times[0] == 1.0 and times[-1] == 9.0
    assert next(a["t"] for a in sched if a["stage"] == "reflector") == 5.0
    stops = L.signal_timeline(press, 1.0, 8.0, pins)
    assert stops[-1]["part"] == "lamp" and stops[-1]["out"] == press["lamp"]
    # The head starts at the key and ends at the lamp.
    kx, ky, _ = L.key_pos("A")
    lx, ly, _ = L.lamp_pos(press["lamp"])
    assert _close(L.head_position(press, 1.0, 8.0, 1.0, pins)[:2], (kx, ky))
    assert _close(L.head_position(press, 1.0, 8.0, 9.0, pins)[:2], (lx, ly))


def test_out_of_order_pins_are_rejected():
    import pytest
    press = EnigmaMachine(CONFIGS["hero_opening"]).press_key("A").to_dict()
    with pytest.raises(ValueError):
        L.signal_schedule(press, 0.0, 8.0, {"reflector": 6.0, "rotor_right_in": 7.0})
