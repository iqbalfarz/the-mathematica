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
