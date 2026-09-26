"""Command line: produce event streams for shots, or just encrypt.

  python -m enigma_core.cli encrypt --config hero_opening --text LLLL
  python -m enigma_core.cli events  --config hero_opening --text LLLL -o build/events/s0101.json
  python -m enigma_core.cli shots   # every shot listed in config/shots.yaml
  python -m enigma_core.cli keyspace
"""
from __future__ import annotations

import argparse
import copy
from pathlib import Path

import yaml

from . import keyspace
from .configuration import MachineConfig, load_configs
from .alphabet import ch, idx
from .events import write_stream
from .rotor import Rotor
from .wiring import ROTORS
from .machine import EnigmaMachine

ROOT = Path(__file__).resolve().parents[2]
MACHINES = ROOT / "config" / "machines.yaml"
SHOTS = ROOT / "config" / "shots.yaml"
EVENTS = ROOT / "build" / "events"


def resolve_shots() -> dict[str, tuple[MachineConfig, list]]:
    """Run every shot in config/shots.yaml through the simulator.

    A shot with `continues: <other shot>` starts with its rotors where that shot
    left them (the machine on screen never jumps between scenes).
    """
    configs = load_configs(MACHINES)
    shots = yaml.safe_load(SHOTS.read_text())["shots"]
    done: dict[str, tuple[MachineConfig, list]] = {}

    def run(shot_id: str, stack=()):
        if shot_id in done:
            return done[shot_id]
        if shot_id in stack:
            raise ValueError(f"shot continuation loop: {' -> '.join(stack + (shot_id,))}")
        spec = shots[shot_id]
        cfg = copy.deepcopy(configs[spec["machine"]])
        if spec.get("continues"):
            parent_cfg, parent_presses = run(spec["continues"], stack + (shot_id,))
            end = parent_presses[-1].positions_after if parent_presses else parent_cfg.to_dict()["positions"]
            cfg.positions = [ord(c) - 65 for c in end]
        presses = EnigmaMachine(cfg).press_keys(spec.get("keys", "") or "")
        done[shot_id] = (cfg, presses)
        return done[shot_id]

    for sid in shots:
        run(sid)
    return done


def rotor_demo(spec: dict) -> list[dict]:
    """Follow one contact through a lone rotor at several positions.

    spec: {rotor: I, ring: A, positions: "ABCD", key: A}. For each position the
    fixed contact `key` meets core pin `in_pin`, whose wire leads to core plate
    `out_pin`, leaving at fixed contact `out`. Pins are named by the ring letter
    engraved next to them, as in the machine event stream.
    """
    r = Rotor.from_name(spec["rotor"], ring=idx(spec.get("ring", "A")))
    out = []
    for p in spec["positions"]:
        r.position = idx(p)
        o, pin, opin = r.forward(idx(spec["key"]))
        out.append({"position": p, "in": spec["key"], "in_pin": ch(pin + r.ring),
                    "out_pin": ch(opin + r.ring), "out": ch(o)})
    return out


def rotor_wire_pairs(name: str) -> list[dict]:
    """The 26 wires of a rotor in its own (core) frame: pin X -> plate wiring[X]."""
    w = ROTORS[name]["wiring"]
    return [{"pin": ch(i), "plate": w[i]} for i in range(26)]


def shot_streams() -> dict[str, Path]:
    out = {}
    shots = yaml.safe_load(SHOTS.read_text())["shots"]
    for sid, (cfg, presses) in resolve_shots().items():
        extra = None
        d = shots[sid].get("rotor_demo")
        if d:
            extra = {"rotor_demo_spec": dict(d, wires=rotor_wire_pairs(d["rotor"])),
                     "rotor_demo": rotor_demo(d) if d.get("positions") else []}
        out[sid] = write_stream(EVENTS / f"{sid}.json", cfg.to_dict(), presses, extra)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(prog="enigma_core")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("encrypt", "events"):
        p = sub.add_parser(name)
        p.add_argument("--config", default="hero_opening")
        p.add_argument("--text", required=True)
        if name == "events":
            p.add_argument("-o", "--out", required=True)
    sub.add_parser("shots")
    sub.add_parser("keyspace")
    a = ap.parse_args(argv)

    if a.cmd == "keyspace":
        for k, v in keyspace.summary().items():
            print(f"{k:36s} {keyspace.fmt(v)}")
        return
    if a.cmd == "shots":
        for sid, path in shot_streams().items():
            print(f"{sid}: {path.relative_to(ROOT)}")
        return
    cfg = load_configs(MACHINES)[a.config]
    m = EnigmaMachine(cfg)
    presses = m.press_keys(a.text)
    if a.cmd == "encrypt":
        for p in presses:
            print(f"{p.positions_before} -> {p.positions_after}  {p.key} -> {p.lamp}"
                  f"{'  (double step)' if p.double_step else ''}")
        print("".join(p.lamp for p in presses))
    else:
        print(write_stream(a.out, cfg.to_dict(), presses))


if __name__ == "__main__":
    main()
