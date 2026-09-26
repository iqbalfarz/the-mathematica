"""Command line: produce event streams for shots, or just encrypt.

  python -m enigma_core.cli encrypt --config hero_opening --text LLLL
  python -m enigma_core.cli events  --config hero_opening --text LLLL -o build/events/s0101.json
  python -m enigma_core.cli shots   # every shot listed in config/shots.yaml
  python -m enigma_core.cli keyspace
"""
from __future__ import annotations

import argparse
from pathlib import Path

import yaml

from . import keyspace
from .configuration import load_configs
from .events import write_stream
from .machine import EnigmaMachine

ROOT = Path(__file__).resolve().parents[2]
MACHINES = ROOT / "config" / "machines.yaml"
SHOTS = ROOT / "config" / "shots.yaml"
EVENTS = ROOT / "build" / "events"


def shot_streams() -> dict[str, Path]:
    configs = load_configs(MACHINES)
    shots = yaml.safe_load(SHOTS.read_text())["shots"]
    out = {}
    for shot_id, spec in shots.items():
        if "machine" not in spec:
            continue
        cfg = configs[spec["machine"]]
        m = EnigmaMachine(cfg)
        presses = m.press_keys(spec.get("keys", ""))
        out[shot_id] = write_stream(EVENTS / f"{shot_id}.json", cfg.to_dict(), presses)
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
