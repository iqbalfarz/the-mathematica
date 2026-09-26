"""The script must agree with the simulator and the research ledger."""
import csv
import re

import yaml

from enigma_core import EnigmaMachine
from enigma_core.configuration import load_configs
from enigma_core.cli import resolve_shots, rotor_demo, rotor_wire_pairs
from enigma_core.reflector import Reflector
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
        if "reflector" in chk:
            pairs = {"".join(sorted(chr(65 + a) + chr(65 + b))) for a, b in Reflector.from_name(chk["reflector"]).pairs()}
            for pair in chk["pairs"].split():
                assert "".join(sorted(pair)) in pairs, f"{sc.id}: {pair} is not a reflector {chk['reflector']} pair"
            if "via" in chk:
                _, presses = RESOLVED[chk["shot"]]
                hop = next(h for h in presses[0].path if h.stage == "reflector")
                assert hop.in_letter + hop.out_letter == chk["via"], f"{sc.id}: current crosses {hop.in_letter}{hop.out_letter}"
        elif "shot" in chk:
            shot = SHOTS[chk["shot"]]
            assert shot["keys"] == chk["keys"]
            _, presses = RESOLVED[chk["shot"]]       # honours `continues`
            if "lamps" in chk:
                out = "".join(p.lamp for p in presses)
                assert out == chk["lamps"], f"{sc.id}: script says {chk['lamps']}, simulator gives {out}"
            if "positions" in chk:        # window letters before the first press, then after each
                chain = " ".join([presses[0].positions_before] + [p.positions_after for p in presses])
                assert chain == chk["positions"], f"{sc.id}: script says {chk['positions']}, simulator gives {chain}"
            for p, want in zip(presses, chk.get("pawls", [])):
                got = " ".join(str(n) for n in sorted({st.pawl for st in p.steps}))
                assert got == want, f"{sc.id}: pawls {want} in the script, the simulator engages {got}"
            for stage, io in (chk.get("stages") or {}).items():
                hop = next(h for h in presses[0].path if h.stage == stage)
                assert hop.in_letter + hop.out_letter == io, f"{sc.id} {stage}: script {io}, simulator {hop.in_letter}{hop.out_letter}"
        elif "machine" in chk:
            m = EnigmaMachine(CONFIGS[chk["machine"]])
            presses = m.press_keys(chk["keys"])
            chain = " ".join([presses[0].positions_before] + [p.positions_after for p in presses])
            assert chain == chk["positions"], f"{sc.id}: script says {chk['positions']}, simulator gives {chain}"
            if "period" in chk:
                m = EnigmaMachine(CONFIGS[chk["machine"]])
                start = m.positions
                n = next(i + 1 for i in range(20000) if m.press_keys("A")[0].positions_after == start)
                assert n == chk["period"], f"{sc.id}: period {chk['period']} in the script, simulator gives {n}"
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
    assert checked >= 8


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
        assert shot["scene"] in ids
        if shot.get("replay"):
            assert shot["replay"] in SHOTS and "keys" not in shot   # a replay never presses again
            continue
        assert shot["machine"] in CONFIGS
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


def test_act5_narration_letters_match_the_press():
    sc = {s.id: s for s in load_script()}
    _, presses = RESOLVED["s0501_three"]
    hops = {h.stage: h for h in presses[0].path}
    said = " ".join(b.spoken for s in ("s0501", "s0502", "s0503") for b in sc[s].beats)
    for stage in ("rotor_right_in", "rotor_middle_in", "rotor_left_in", "rotor_left_out",
                  "rotor_middle_out", "rotor_right_out"):
        h = hops[stage]
        assert re.search(rf"{h.in_letter} (?:into|becomes) {h.out_letter}\.", said), stage
    r = hops["reflector"]
    assert f"came in at {r.in_letter} leaves at its partner, {r.out_letter}" in said
    assert f"One lamp lights. {presses[0].lamp}." in said


def test_act6_narration_matches_the_steps():
    """Every 'X becomes Y' in Act VI is a rotor the simulator actually stepped, and
    the state table read aloud in s0604 is the simulator's."""
    sc = {s.id: s for s in load_script()}
    for scene, shot in (("s0601", "s0601_pawls"), ("s0602", "s0602_notch"), ("s0603", "s0603_double")):
        _, presses = RESOLVED[shot]
        said = " ".join(b.spoken for b in sc[scene].beats)
        claimed = re.findall(r"\b([A-Z]) becomes ([A-Z])\.", said)
        moved = {(st.from_letter, st.to_letter) for p in presses for st in p.steps}
        assert claimed and set(claimed) <= moved, (scene, claimed, moved)
    _, p3 = RESOLVED["s0603_double"]
    assert [st.reason for st in p3[0].steps].count("double_step") == 1
    spoken = " ".join(b.spoken for b in sc["s0604"].beats)
    table = sc["s0604"].sim_check["positions"].split()
    assert ". Press. ".join(" ".join(w) for w in table) + "." in spoken
    assert "16,900" in spoken and "17,576" in spoken and 26 ** 3 == 17576
