from enigma_core import EnigmaMachine
from enigma_core.configuration import load_configs
from enigma_core.events import STAGES, read_stream, write_stream

from conftest import ROOT

CONFIGS = load_configs(ROOT / "config" / "machines.yaml")


def test_path_is_a_continuous_chain_ending_at_the_lamp():
    m = EnigmaMachine(CONFIGS["barbarossa_1941"])
    for p in m.press_keys("AUFKLARUNGXVONXKURTINOWA"):
        assert [h.stage for h in p.path] == STAGES
        for a, b in zip(p.path, p.path[1:]):
            assert a.out_letter == b.in_letter
        assert p.path[0].in_letter == p.key
        assert p.path[-1].out_letter == p.lamp


def test_rotor_hops_record_core_pins():
    p = EnigmaMachine(CONFIGS["textbook_aaa"]).press_key("A")
    right = p.path[3]
    # Positions AAB, ring A: fixed contact A meets core pin B of rotor III.
    assert right.rotor == "III" and right.in_letter == "A" and right.in_pin == "B"


def test_stream_roundtrip(tmp_path):
    cfg = CONFIGS["hero_opening"]
    presses = EnigmaMachine(cfg).press_keys("LLLL")
    path = write_stream(tmp_path / "s.json", cfg.to_dict(), presses)
    data = read_stream(path)
    assert [p["lamp"] for p in data["presses"]] == [p.lamp for p in presses]
    assert data["config"]["positions"] == "AFP"
    assert data["presses"][0]["positions_after"] == "AFQ"


def test_continued_shots_start_where_their_parent_ended():
    from enigma_core.cli import resolve_shots
    shots = resolve_shots()
    end_of_s0101 = shots["s0101_keys"][1][-1].positions_after
    for sid in ("s0102_reveal", "s0301_tour", "s0302_circuit"):
        cfg, _ = shots[sid]
        assert "".join(chr(65 + p) for p in cfg.positions) == end_of_s0101 == "AFT"
    assert shots["s0302_circuit"][1][0].positions_before == "AFT"


def test_rotor_demo_follows_one_contact_through_the_turning_rotor():
    from enigma_core.cli import rotor_demo, rotor_wire_pairs
    from enigma_core.rotor import Rotor
    steps = rotor_demo({"rotor": "I", "ring": "A", "positions": "ABCD", "key": "A"})
    assert [s["position"] for s in steps] == list("ABCD")
    assert [s["in_pin"] for s in steps] == list("ABCD")        # contact A meets pin A, B, C, D
    wires = {w["pin"]: w["plate"] for w in rotor_wire_pairs("I")}
    for s in steps:
        assert wires[s["in_pin"]] == s["out_pin"]             # it rides that pin's own wire
        r = Rotor.from_name("I", position=ord(s["position"]) - 65)
        assert chr(65 + r.forward(0)[0]) == s["out"]
    assert "".join(s["out"] for s in steps) == "EJKC"


def test_replay_shots_reuse_the_same_press():
    from enigma_core.cli import resolve_shots
    shots = resolve_shots()
    cfg, presses = shots["s0501_three"]
    for sid in ("s0502_mirror", "s0503_return"):
        assert shots[sid][1] is presses                     # same press, not a new one
    assert presses[0].positions_before == "AFU" and presses[0].positions_after == "AFV"


def test_timeline_signal_pins_accept_seconds_and_start():
    import sys
    sys.path.insert(0, str(ROOT / "src"))
    from enigma_doc.timeline import _signal
    entry = {"beats": [{"id": "b1", "start": 1.0, "dur": 2.0}, {"id": "b2", "start": 4.0, "dur": 2.0}]}
    shot = {"signal": {"pins": {"start": -30, "reflector": -1, "turn": "b2+0.5", "lamp": 9999}}}
    out = _signal(entry, shot, [])
    assert out["signal_start"] == -30 and out["signal_dur"] == 9999 + 30
    assert out["signal_pins"] == {"reflector": -1.0, "turn": 4.5, "lamp": 9999.0}
    out = _signal(entry, {"signal": {"pins": {"lamp": "b2"}}}, [2.0])
    assert out["signal_start"] == 2.11 and abs(out["signal_dur"] - 1.89) < 1e-9
