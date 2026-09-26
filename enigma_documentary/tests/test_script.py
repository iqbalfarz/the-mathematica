"""The script must agree with the simulator and the research ledger."""
import csv
import re

import yaml

from enigma_core import EnigmaMachine
from enigma_core.configuration import load_configs
from enigma_core.rotor import Rotor

from conftest import ROOT

import sys
sys.path.insert(0, str(ROOT / "src"))
from enigma_doc.script import load_script  # noqa: E402

CONFIGS = load_configs(ROOT / "config" / "machines.yaml")
SHOTS = yaml.safe_load((ROOT / "config" / "shots.yaml").read_text())["shots"]
LEDGER = {r["claim_id"] for r in csv.DictReader((ROOT / "research" / "claim_ledger.csv").open())}
LOOPS = yaml.safe_load((ROOT / "story" / "loop_map.yaml").read_text())


def test_sim_checks_match_the_simulator():
    checked = 0
    for sc in load_script():
        chk = sc.sim_check
        if not chk:
            continue
        if "shot" in chk:
            shot = SHOTS[chk["shot"]]
            assert shot["keys"] == chk["keys"]
            out = EnigmaMachine(CONFIGS[shot["machine"]]).encrypt(chk["keys"])
            assert out == chk["lamps"], f"{sc.id}: script says {chk['lamps']}, simulator gives {out}"
        else:
            r = Rotor.from_name(chk["rotor"])
            outs = ""
            for p in chk["positions"]:
                r.position = ord(p) - 65
                outs += chr(65 + r.forward(ord(chk["key"]) - 65)[0])
            assert outs == chk["outputs"], f"{sc.id}: script says {chk['outputs']}, simulator gives {outs}"
        checked += 1
    assert checked >= 2


def test_spoken_letters_match_sim_check():
    """Every lamp letter the narration of s0101 speaks appears in order."""
    sc = next(s for s in load_script() if s.id == "s0101")
    spoken = " ".join(b.spoken for b in sc.beats)
    found = re.findall(r"(?<![A-Za-z])([A-Z])\.", spoken)
    assert "".join(found) == sc.sim_check["lamps"]
    s3 = next(s for s in load_script() if s.id == "s0203")
    spoken = " ".join(b.spoken for b in s3.beats)
    letters = re.findall(r"(?:as|time,|Again\.|again\.)\s+([A-Z])\.", spoken)
    assert "".join(letters) == s3.sim_check["outputs"]


def test_every_claim_tag_is_in_the_ledger():
    for sc in load_script():
        for b in sc.beats:
            for tag in b.tags:
                assert tag in LEDGER, f"{sc.id}/{b.id}: unknown claim {tag}"


def test_sentences_with_numbers_carry_a_claim():
    for sc in load_script():
        for b in sc.beats:
            if re.search(r"\d", b.spoken):
                assert b.tags, f"{sc.id}/{b.id} states a number without a claim tag"


def test_loops_open_before_payoff_and_exist():
    order = [s.id for s in load_script()]
    for lid, loop in LOOPS.items():
        if loop["opened"] in order:
            assert any(lid in s.loops_open for s in load_script() if s.id == loop["opened"])
        if loop["opened"] in order and loop["payoff"] in order:
            assert order.index(loop["opened"]) < order.index(loop["payoff"])
    for s in load_script():
        for lid in s.loops_open:
            assert LOOPS[lid]["opened"] == s.id


def test_shots_reference_known_machines_and_scenes():
    ids = {s.id for s in load_script()}
    for name, shot in SHOTS.items():
        assert shot["machine"] in CONFIGS
        assert shot["scene"] in ids
