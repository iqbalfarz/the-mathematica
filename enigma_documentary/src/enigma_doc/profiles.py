from __future__ import annotations

import os

import yaml

from .paths import CONFIG


def load_profiles() -> dict:
    return yaml.safe_load((CONFIG / "render_profiles.yaml").read_text())


def resolve(name: str | None = None) -> dict:
    cfg = load_profiles()
    name = name or os.environ.get("PROFILE") or cfg["default"]
    if name not in cfg["profiles"]:
        raise SystemExit(f"unknown profile {name!r}; choose from {list(cfg['profiles'])}")
    p = dict(cfg["profiles"][name])
    p.update(name=name, lead_in=cfg["lead_in"], tail=cfg["tail"])
    return p
