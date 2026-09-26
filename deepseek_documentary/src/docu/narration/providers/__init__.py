"""Voice providers. Select with VOICE_PROVIDER=kokoro|cloned (default from config/voice.yaml)."""
import os

import yaml

from ...paths import CONFIG


def load_voice_config() -> dict:
    return yaml.safe_load((CONFIG / "voice.yaml").read_text())


def get_provider():
    cfg = load_voice_config()
    name = os.environ.get("VOICE_PROVIDER", cfg.get("provider", "kokoro"))
    if name == "kokoro":
        from .kokoro import KokoroProvider
        return KokoroProvider(cfg)
    if name == "cloned":
        from .cloned import ClonedProvider
        return ClonedProvider(cfg)
    raise ValueError(f"unknown VOICE_PROVIDER {name!r}")
