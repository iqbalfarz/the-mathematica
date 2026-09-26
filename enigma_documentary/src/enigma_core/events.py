"""The event stream: the contract between the simulator and every renderer.

One KeyPress per key. It says which pawls moved which rotors, and every hop the
current made, in both the fixed frame ("pos", the contact on the machine body
Blender draws a wire to) and, for rotors, the core frame ("pin").

JSON layout (schema_version 1):

{
  "schema_version": 1,
  "config": {...MachineConfig.to_dict()...},
  "presses": [
    {"index": 0, "key": "L", "lamp": "Y",
     "positions_before": "AAA", "positions_after": "AAB",
     "steps": [{"pawl": 1, "rotor": "right", ...}],
     "path": [{"stage": "plugboard", "direction": "in", "in": "L", "out": "L"}, ...]}
  ]
}
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

from .stepping import StepEvent

SCHEMA_VERSION = 1

# The order in which the current meets each part (right-to-left, then back).
STAGES = ["keyboard", "plugboard_in", "entry_in", "rotor_right_in", "rotor_middle_in",
          "rotor_left_in", "reflector", "rotor_left_out", "rotor_middle_out",
          "rotor_right_out", "entry_out", "plugboard_out", "lamp"]


@dataclass
class Hop:
    stage: str
    in_letter: str           # fixed-frame contact where the current arrives
    out_letter: str          # fixed-frame contact where it leaves
    in_pin: str | None = None    # rotor core contact (ring-alphabet letter at that pin), rotors only
    out_pin: str | None = None
    rotor: str | None = None     # rotor name, e.g. "III"

    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class KeyPress:
    index: int
    key: str
    lamp: str
    positions_before: str
    positions_after: str
    steps: list[StepEvent] = field(default_factory=list)
    path: list[Hop] = field(default_factory=list)

    @property
    def double_step(self) -> bool:
        return any(s.reason == "double_step" for s in self.steps)

    def to_dict(self) -> dict:
        return {"index": self.index, "key": self.key, "lamp": self.lamp,
                "positions_before": self.positions_before, "positions_after": self.positions_after,
                "double_step": self.double_step,
                "steps": [s.to_dict() for s in self.steps],
                "path": [h.to_dict() for h in self.path]}


def stream(config: dict, presses: list[KeyPress], extra: dict | None = None) -> dict:
    out = {"schema_version": SCHEMA_VERSION, "config": config, "presses": [p.to_dict() for p in presses]}
    out.update(extra or {})
    return out


def write_stream(path: str | Path, config: dict, presses: list[KeyPress], extra: dict | None = None) -> Path:
    """`extra` adds sections such as a single-rotor demo:
    "rotor_demo_spec": {...}, "rotor_demo": [{position, in, in_pin, out_pin, out}, ...]"""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(stream(config, presses, extra), indent=1))
    return path


def read_stream(path: str | Path) -> dict:
    data = json.loads(Path(path).read_text())
    if data.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(f"{path}: unsupported event schema {data.get('schema_version')}")
    return data
