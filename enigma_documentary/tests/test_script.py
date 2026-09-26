"""The script must agree with the simulator and the research ledger."""
import csv
import re

import yaml

from enigma_core import EnigmaMachine
from enigma_core.configuration import load_configs
from enigma_core.cli import resolve_shots, rotor_demo, rotor_wire_pairs
from enigma_core.rotor import Rotor

from conftest import ROOT

import sys
sys.path.insert(0, str(ROOT / "src"))
from enigma_doc.script import load_script  # noqa: E402

CONFIGS = load_configs(ROOT / "config" / "machines.yaml")
SHOTS = yaml.safe_load((ROOT / "config" / "shots.yaml").read_text())["shots"]
LEDGER = {r["claim_id"] for r in csv.DictReader((ROOT / "research" / "claim_ledger.csv").open())}
RESOLVED = resolve_shots()
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
            _, presses = RESOLVED[chk["shot"]]       # honours `continues`
            out = "".join(p.lamp for p in presses)
            assert out == chk["lamps"], f"{sc.id}: script says {chk['lamps']}, simulator gives {out}"
        elif "rotor_demo" in chk:
            spec = SHOTS[chk["rotor_demo"]]["rotor_demo"]
            outs = "".join(step["out"] for step in rotor_demo(spec))
            assert outs == chk["outputs"], f"{sc.id}: script says {chk['outputs']}, simulator gives {outs}"
        elif "wires" in chk:
            pairs = {w["pin"]: w["plate"] for w in rotor_wire_pairs(chk["rotor"])}
            plates = "".join(pairs[c] for c in chk["wires"])
            assert plates == chk["plates"], f"{sc.id}: script says {chk['plates']}, rotor wiring gives {plates}"
        else:
            r = Rotor.from_name(chk["rotor"])
            outs = ""
            for p in chk["positions"]:
                r.position = ord(p) - 65
                outs += chr(65 + r.forward(ord(chk["key"]) - 65)[0])
            assert outs == chk["outputs"], f"{sc.id}: script says {chk['outputs']}, simulator gives {outs}"
        checked += 1
    assert checked >= 5


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
        spec = shot.get("rotor_demo")
        if spec:
            # the demo rotor must be the rotor actually sitting in that slot of the machine
            cfg, _ = RESOLVED[name]
            slot = ("left", "middle", "right").index(spec["slot"])
            assert cfg.rotors[slot] == spec["rotor"]
            assert chr(65 + cfg.rings[slot]) == spec.get("ring", "A")


def test_s0302_narration_names_the_simulated_lamp():
    sc = next(s for s in load_script() if s.id == "s0302")
    spoken = " ".join(b.spoken for b in sc.beats)
    assert f"Press {sc.sim_check['keys']}." in spoken
    assert re.search(rf"lamp\. {sc.sim_check['lamps']}\.", spoken)


def test_every_sfx_cue_exists():
    import ast
    src = (ROOT / "src" / "enigma_doc" / "audio" / "sfx.py").read_text()
    tree = ast.parse(src)
    sfx = next(n for n in tree.body if isinstance(n, ast.Assign) and n.targets[0].id == "SFX")
    names = {k.value for k in sfx.value.keys}
    names |= {"clack", "click"}          # press sounds added by the timeline
    for sc in load_script():
        for b in sc.beats:
            if b.sfx:
                assert b.sfx in names, f"{sc.id}/{b.id}: no sound effect called {b.sfx!r}"


def test_act4_narration_letters_match_the_rotor():
    sc = {s.id: s for s in load_script()}
    spoken = " ".join(b.spoken for b in sc["s0402"].beats)
    for pin, plate in zip("ABC", sc["s0402"].sim_check["plates"]):
        assert re.search(rf"Pin {pin} goes to (plate )?{plate}\.", spoken), (pin, plate)
    spoken = " ".join(b.spoken for b in sc["s0403"].beats)
    outs = sc["s0403"].sim_check["outputs"]
    assert f"comes out at {outs[0]}." in spoken and f"comes out at {outs[1]}." in spoken
    assert f"it's {outs[2]}." in spoken and f"it's {outs[3]}." in spoken
    # the wire named in beat b4 is the one the simulator says contact A meets at position B
    step_b = rotor_demo(SHOTS["s0403_turn"]["rotor_demo"])[1]
    assert f"pin {step_b['in_pin']}. Its wire goes to {step_b['out_pin']}." in spoken
