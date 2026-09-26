from __future__ import annotations

import os

import yaml

from ..paths import CONFIG


def load_video_config() -> dict:
    return yaml.safe_load((CONFIG / "video.yaml").read_text())


def resolve_quality(quality: str | None = None, resolution: str | None = None, fps: int | None = None) -> dict:
    """Quality preset, overridable by --resolution/--fps or RESOLUTION/FPS env vars."""
    cfg = load_video_config()
    quality = quality or os.environ.get("QUALITY") or cfg["default_preset"]
    if quality not in cfg["presets"]:
        raise SystemExit(f"unknown quality {quality!r}; choose from {list(cfg['presets'])}")
    p = dict(cfg["presets"][quality])
    p["name"] = quality
    resolution = resolution or os.environ.get("RESOLUTION")
    fps = fps or (int(os.environ["FPS"]) if os.environ.get("FPS") else None)
    if resolution:
        w, h = (int(v) for v in resolution.lower().split("x"))
        p.update(width=w, height=h)
        p["name"] = f"{w}x{h}"
    if fps:
        p["fps"] = int(fps)
        p["name"] = f"{p['name']}@{fps}"
    if resolution or fps:
        p["name"] = p["name"].replace("@", "_")
    p["background"] = cfg["background"]
    return p
